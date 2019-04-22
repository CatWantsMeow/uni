# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime
import logging
import random
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models

from finance.bank_system_proxy import BankSystemProxy
from finance.utils import money_field, percentage_field

logger = logging.getLogger('jupiter')


class Product(models.Model):
    is_active = models.BooleanField(default=False)
    client = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        permissions = (
            ('view_product', 'Can view product'),
        )


class Transaction(models.Model):
    TYPE_CREDIT_CREATE = 101
    TYPE_CREDIT_PAY = 102
    TYPE_CREDIT_CLOSE = 103
    TYPE_CREDIT_FINED = 104
    TYPE_CREDIT_REQUEST = 105
    TYPE_CREDIT_CONFIRM = 106
    TYPE_CREDIT_REJECT = 107
    TYPE_CREDIT_OPENED = 108

    TYPE_ACCOUNT_ASSIGNED = 201
    TYPE_ACCOUNT_CREATED = 202
    TYPE_ACCOUNT_REQUEST_CREATE = 203
    TYPE_ACCOUNT_CONFIRM_CREATE = 204
    TYPE_ACCOUNT_REJECT_CREATE = 207
    TYPE_ACCOUNT_REQUEST_CLOSE = 205
    TYPE_ACCOUNT_CONFIRM_CLOSE = 206
    TYPE_ACCOUNT_REJECT_CLOSE = 208
    TYPE_ACCOUNT_GET_MONEY = 209
    TYPE_ACCOUNT_PUT_MONEY = 210

    TYPE_DUMMY = 666

    TYPES = [
        (TYPE_CREDIT_CREATE, ''),
        (TYPE_CREDIT_PAY, ''),
        (TYPE_CREDIT_CLOSE, ''),
        (TYPE_CREDIT_FINED, ''),
        (TYPE_CREDIT_REQUEST, ''),
        (TYPE_CREDIT_CONFIRM, ''),
        (TYPE_CREDIT_REJECT, ''),
        (TYPE_CREDIT_OPENED, ''),
        (TYPE_ACCOUNT_ASSIGNED, ''),
        (TYPE_ACCOUNT_CREATED, ''),
        (TYPE_ACCOUNT_REQUEST_CREATE, ''),
        (TYPE_ACCOUNT_CONFIRM_CREATE, ''),
        (TYPE_ACCOUNT_REQUEST_CLOSE, ''),
        (TYPE_ACCOUNT_CONFIRM_CLOSE, ''),
        (TYPE_ACCOUNT_REJECT_CREATE, ''),
        (TYPE_ACCOUNT_REJECT_CLOSE, ''),
        (TYPE_ACCOUNT_GET_MONEY, ''),
        (TYPE_ACCOUNT_PUT_MONEY, ''),
        (TYPE_DUMMY, '')
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL)
    product = models.ForeignKey(Product)
    info = models.CharField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(choices=TYPES, default=TYPE_DUMMY)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        permissions = (
            ('view_transaction', 'Can view transaction'),
        )


class Contract(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL)
    product = models.ForeignKey(Product)
    signed_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Contract'
        verbose_name_plural = 'Contracts'
        permissions = (
            ('view_contract', 'Can view contract'),
        )


class Account(Product):
    STATUS_ACTIVE = 0
    STATUS_CLOSED = 1
    STATUS_DISABLED = 2
    STATUS_REJECTED = 3
    STATUS_REQUESTED_CREATING = 4
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_CLOSED, 'Closed'),
        (STATUS_DISABLED, 'Disabled'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_REQUESTED_CREATING, 'Create claim leaved'),
    ]

    INOPERABLE_STATUSES = [
        STATUS_DISABLED,
        STATUS_REJECTED,
        STATUS_CLOSED,
        STATUS_REQUESTED_CREATING,
    ]

    number = models.CharField(max_length=30, default='0' * 13)
    residue = money_field()
    status = models.IntegerField(choices=STATUS_CHOICES)
    close_claim = models.BooleanField(default=False)
    target_account_id = models.IntegerField(default=-1)

    class Meta:
        verbose_name = 'Checking account'
        verbose_name_plural = 'Checking accounts'
        permissions = (
            ('view_account', 'Can view account'),
            ('leave_create_claim_account', 'Can leave create claim'),
            ('confirm_create_claim_account', 'Can confirm create claim'),
            ('reject_create_claim_account', 'Can reject create claim'),
            ('unassign_account', 'Can unassign account'),
            ('assign_account', 'Can assign account')
        )

    @classmethod
    def get_last_digit(cls, digits):
        weight_coefs = [713, 371, 371, 371, 371, 3]
        number = '111' + digits + '0'
        sum = 0
        for i in range(0, len(number), 3):
            piece = int(number[i: min(i + 3, len(number))])
            sum += (piece * weight_coefs[i / 3]) % 10
        return str((sum * 3) % 10)

    @classmethod
    def _create_new_number(cls):
        new_number = '3014' + str(random.randrange(10000000, 99999999))
        new_number += cls.get_last_digit(new_number)
        while cls.objects.filter(number=new_number):
            new_number = '3014' + str(random.randrange(10000000, 99999999))
            new_number += cls.get_last_digit(new_number)
        return new_number

    @classmethod
    def create(cls, is_active, client, first_contribution):
        """
        account created already with money - dummy
        Also, if credit opened, then money can be puted into created account
        """
        status = Account.STATUS_ACTIVE if is_active else Account.STATUS_REQUESTED_CREATING
        account = Account.objects.create(
            is_active=is_active,
            number=cls._create_new_number(),
            residue=first_contribution,
            status=status,
            client=client
        )
        account.save()
        info_text = 'Создан счет' if is_active else 'Подана заявка на создание счета'
        t_type = Transaction.TYPE_ACCOUNT_CREATED if is_active else \
            Transaction.TYPE_ACCOUNT_REQUEST_CREATE
        Transaction.objects.create(client=client,
                                   product=account,
                                   info=info_text,
                                   type=t_type)
        return account

    @classmethod
    def assign(cls, client, account_number):
        """
        assign account by account_number to client
        """
        if Account.objects.filter(number=account_number):
            account = Account.objects.filter(number=account_number).first()
            if account.status == Account.STATUS_CLOSED:
                account.status = Account.STATUS_ACTIVE
                account.save()
            else:
                return False, 'Этот счет уже используется.'
        else:
            res, money_amount = BankSystemProxy.account_assign_to_user(client, account_number)
            if not res:
                return False, 'Отказано банком. Проверте счет.'

            account = Account.objects.create(
                number=account_number,
                is_active=True,
                residue=money_amount,
                status=Account.STATUS_ACTIVE,
                client=client
            )
            account.save()

        info_text = 'Счет успешно привязан.'
        Transaction.objects.create(
            client=client,
            product=account,
            info=info_text,
            type=Transaction.TYPE_ACCOUNT_ASSIGNED
        )
        return True, info_text

    def confirm(self):
        """
        Confirm account
        """
        if self.status != self.STATUS_REQUESTED_CREATING:
            return False

        bank_confirmation = BankSystemProxy.account_creation(self.number,
                                                             self.client.id,
                                                             float(self.residue.amount))
        if not bank_confirmation:
            self.reject('Отклонено банком')
            return False

        self.is_active = True
        self.status = Account.STATUS_ACTIVE
        self.save()
        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Счет подтвержден.',
                                   type=Transaction.TYPE_ACCOUNT_CONFIRM_CREATE)
        Contract.objects.create(client=self.client,
                                product=self)
        return True

    def reject(self, cause):
        if self.status != self.STATUS_REQUESTED_CREATING:
            return False
        self.status = Account.STATUS_REJECTED
        self.save()
        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Заявка на создание счета отклонена. Причина: {}'.format(
                                       cause),
                                   type=Transaction.TYPE_ACCOUNT_REJECT_CREATE)
        return True

    def put_money(self, contribution):
        """
        In BYN only
        """
        if self.status in Account.INOPERABLE_STATUSES:
            return False

        bank_confirmation = BankSystemProxy.account_put_money(self.id, float(contribution))
        if not bank_confirmation:
            return False

        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Зачисление в размере {} BYN'.format(contribution),
                                   type=Transaction.TYPE_ACCOUNT_PUT_MONEY)
        self.residue.amount += Decimal(contribution)
        self.save()
        return True

    def get_money(self, required_quantity):
        """
        In BYN only
        """
        if self.status in Account.INOPERABLE_STATUSES:
            return False

        if self.residue.amount >= Decimal(required_quantity):
            self.residue.amount -= Decimal(required_quantity)
            self.save()

            bank_confirmation = BankSystemProxy.account_get_money(self.id,
                                                                  required_quantity)
            if not bank_confirmation:
                return False

            Transaction.objects.create(client=self.client,
                                       product=self,
                                       info='Снятие в размере {} BYN'.format(required_quantity),
                                       type=Transaction.TYPE_ACCOUNT_PUT_MONEY)
            return True
        return False

    def unassign(self):
        """
        :param target_account_id:
        account_id, where money will be sent
        """
        if self.status in Account.INOPERABLE_STATUSES:
            return False
        self.close_claim = True
        self.status = Account.STATUS_CLOSED
        self.save()
        return True


class CreditTemplate(models.Model):
    ENSURING_FINE = 0
    ENSURING_PLEDGE = 1
    ENSURING_SURETY = 2
    ENSURING_CHOICES = [
        (ENSURING_FINE, "Fine"),
        (ENSURING_PLEDGE, "Plegde"),
        (ENSURING_SURETY, "Surety"),
    ]

    TYPE_CONSUMER = 0
    TYPE_SELLER = 1
    TYPE_CHOICES = [
        (TYPE_CONSUMER, 'For own needs'),
        (TYPE_SELLER, "On the seller's account"),
    ]

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    annual_percentage_rate = percentage_field()
    max_amount = JSONField()
    min_amount = JSONField()
    max_duration = models.IntegerField(default=12)
    fine_percentage = percentage_field()
    issue_online = models.BooleanField(default=False)
    allowed_ensuring = ArrayField(models.IntegerField(choices=ENSURING_CHOICES))
    detailed_info = models.TextField()
    type = models.IntegerField(choices=TYPE_CHOICES, default=TYPE_CONSUMER)

    class Meta:
        verbose_name = 'Credit templates'
        verbose_name_plural = 'Credit templates'
        permissions = (
            ('view_credittemplate', 'Can view credit template'),
        )


class Credit(Product):
    STATUS_OPENED = 0
    STATUS_FINED = 1
    STATUS_PAID_OFF = 2
    STATUS_CLOSED = 3
    STATUS_REJECTED = 4
    STATUS_REQUESTED = 5
    STATUS_CHOICES = [
        (STATUS_OPENED, 'Opened'),
        (STATUS_FINED, 'Fined'),
        (STATUS_PAID_OFF, 'Paid off'),
        (STATUS_CLOSED, 'Closed'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_REQUESTED, 'Requested'),
    ]

    INOPERABLE_STATUSES = [
        STATUS_CLOSED,
        STATUS_REJECTED,
        STATUS_REQUESTED,
    ]

    INTO_ACCOUNT = 0  # Your account or seller account
    IN_CASH = 1

    MONEY_DESTINATION = [
        (INTO_ACCOUNT, 'Into account'),
        (IN_CASH, 'In cash'),
    ]

    total_sum = money_field()
    residue = money_field()
    current_penalty = money_field()
    start_date = models.DateField()
    duration = models.IntegerField()  # in months
    next_payment_term = models.DateField(null=True)
    template = models.ForeignKey(CreditTemplate)
    status = models.IntegerField(choices=STATUS_CHOICES)
    annual_percentage_rate = percentage_field()
    fine_percentage = percentage_field()
    minimum_monthly_pay = money_field(null=True)
    current_month_pay = money_field(null=True)
    current_month_percents = money_field(
        null=True)  # money amount, should be payed, to avoid penalty
    method_of_ensuring = models.IntegerField(choices=CreditTemplate.ENSURING_CHOICES)
    money_destination = models.IntegerField(choices=MONEY_DESTINATION)
    target_account_id = models.IntegerField(default=-1)  # where money will be placed

    class Meta:
        verbose_name = 'Credit'
        verbose_name_plural = 'Credits'
        permissions = (
            ('view_credit', 'Can view credit'),
            ('make_payment_credit', 'Can make payment'),
            ('open_online_credit', 'Can open online'),
            ('leave_create_claim_credit', 'Can leave craate claim'),
            ('confirm_create_claim_credit', 'Can confirm create claim'),
            ('reject_create_claim_credit', 'Can reject create claim'),
            ('close_credit', 'Can close credit')
        )

    def close(self):
        """
        User can close credit without confirmation, if credit is paid_off
        Attempts to close the credit. Throws exceptions if the attempt fails
        """
        if self.status != Credit.STATUS_PAID_OFF:
            return False

        bank_confirmation = BankSystemProxy.credit_close(self.id)
        if not bank_confirmation:
            return False

        self.status = Credit.STATUS_CLOSED
        self.save()

        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Кредит закрыт.',
                                   type=Transaction.TYPE_CREDIT_CLOSE)

        return True

    def current_percents(self):
        return Credit._get_current_percentage(self.residue.amount, self.annual_percentage_rate)

    def daily_update(self):
        """
        Updates the state of the model. Should be called daily
        """
        if self.status in Credit.INOPERABLE_STATUSES:
            return
        self._check_overdue()
        if self.status == Credit.STATUS_FINED:
            self._update_penalty()
            Transaction.objects.create(client=self.client,
                                       product=self,
                                       info='Начислен штраф. Текущий штраф: {}.'.format(
                                           self.current_penalty),
                                       type=Transaction.TYPE_CREDIT_FINED)
        self.save()

    def pay(self, payment):
        """
        Processes the payment for the credit.
        Steps:
            0. assert credit != CLOSED
            1. If credit FINED, then
                a. Try to pay penalty
                b. If penalty payed, then change credit status to OPENED, then continue
            2. If credit OPENED or PAYED_OFF(client should explicitly close credit), then
                Every payment goes to pay for current credit percents and for decrease residue, so
                a. Pay for percents
                b. Decrease residue
                c. Inc current_month_pay
        We can multiple payments during one month.
        """
        if self.status in Credit.INOPERABLE_STATUSES:
            return False

        bank_confirmation = BankSystemProxy.credit_pay(self.id, float(payment))
        if not bank_confirmation:
            return False

        payment = Decimal(payment)
        self.total_sum.amount += payment
        if self.status == Credit.STATUS_FINED:
            if self.current_penalty.amount <= payment:
                days_late = (datetime.date.today() - self.next_payment_term).days
                profile = self.client.profile
                profile.treat_days_late(days_late)
                payment, self.current_penalty.amount = payment - self.current_penalty.amount, 0
                self.status = Credit.STATUS_OPENED
            else:
                self.current_penalty.amount -= payment
                payment = 0
        self.current_month_pay.amount += payment  # inc current_month_pay
        cur_percents = self.current_month_percents.amount
        cur_percents, payment = max(0, cur_percents - payment), max(0, payment - cur_percents)
        self.current_month_percents = cur_percents
        self.residue.amount -= payment  # can be < 0
        if self.residue.amount <= 0:
            self.status = Credit.STATUS_PAID_OFF
        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Внесен платеж по кредиту в размере: {}.'.format(payment),
                                   type=Transaction.TYPE_CREDIT_PAY)
        self.save()
        return True

    def _check_overdue(self):
        """
        Checks for overdue and updates accordingly. Should be called daily
        """
        cur_date = datetime.date.today()
        end_date = self.start_date + relativedelta(months=self.duration)
        if end_date <= cur_date:
            self.status = Credit.STATUS_FINED
        elif self.next_payment_term <= cur_date:
            if self.current_month_percents != 0:
                self.status = Credit.STATUS_FINED
            else:
                self.next_payment_term += relativedelta(months=1)
                self.current_month_percents = self.current_percents() + 0.1
                self.current_month_pay.amount = 0
        self.save()

    def _update_penalty(self):
        """
        Recalculates the penalty. Should be called daily
        """
        if self.status == Credit.STATUS_FINED:
            total = self.residue.amount + self.current_penalty.amount
            self.current_penalty = self.current_penalty.amount + \
                                   total * self.fine_percentage / Decimal(100.0)
        self.save()

    @classmethod
    def _credit_scoring(cls):
        return True

    @classmethod
    def create_online(cls, client, template, money_amount, duration, account_id=None):
        bank_confirmation = BankSystemProxy.credit_create(
            client.id,
            template.id,
            money_amount,
            duration,
            float(template.annual_percentage_rate)
        )
        if not bank_confirmation:
            return False, 'Отказано банком'

        success, scoring_result = client.get_scoring()
        if not success:
            return False, scoring_result
        elif scoring_result['level'] != 'success':
            return False, 'Ваша заявка отклонена кредитным скорингом. ' \
                          'У вас недостаточная платежеспособность'

        monthly_pay = cls._min_monthly_pay(money_amount, template.annual_percentage_rate, duration)
        if account_id is None:
            account = Account.create(True, client, 0)
            account_id = account.id

        credit = cls.objects.create(
            is_active=True,
            client=client,
            template=template,
            total_sum=0,
            residue=money_amount,
            current_penalty=0,
            start_date=datetime.date.today() + relativedelta(days=1),
            duration=duration,
            next_payment_term=datetime.date.today() + relativedelta(months=1),
            status=cls.STATUS_OPENED,
            annual_percentage_rate=template.annual_percentage_rate,
            fine_percentage=template.fine_percentage,
            minimum_monthly_pay=monthly_pay,
            current_month_pay=0,
            current_month_percents=0,
            method_of_ensuring=CreditTemplate.ENSURING_FINE,
            money_destination=cls.INTO_ACCOUNT,
            target_account_id=account_id
        )
        credit.save()

        target_account = Account.objects.get(pk=account_id)
        target_account.put_money(money_amount)
        target_account.save()

        info_text = 'Открыт онлайн кредит кредит.'
        Transaction.objects.create(client=client,
                                   product=credit,
                                   info=info_text,
                                   type=Transaction.TYPE_CREDIT_OPENED)
        return True, credit

    @classmethod
    def create_claim(cls, client, template, money_amount, duration, ensuring_method,
                     money_destination=INTO_ACCOUNT, account_id=None):
        """
        if Template.issue_online, then credit will be created as active
        Creates a credit with default parameters.
        Client gets 1 month, as buffered - no payment, then begin loan payments.
        """
        monthly_pay = cls._min_monthly_pay(money_amount, template.annual_percentage_rate, duration)
        # create account, if need
        if account_id is None and money_destination == cls.INTO_ACCOUNT:
            account = Account.create(False, client, 0)
            account_id = account.id
        if account_id is None:
            account_id = -1
        credit = cls.objects.create(
            is_active=False,
            client=client,
            template=template,
            total_sum=0,
            residue=money_amount,
            current_penalty=0,
            start_date=datetime.date.today() + relativedelta(days=1),
            duration=duration,
            next_payment_term=datetime.date.today() + relativedelta(months=1),
            status=cls.STATUS_REQUESTED,
            annual_percentage_rate=template.annual_percentage_rate,
            fine_percentage=template.fine_percentage,
            minimum_monthly_pay=monthly_pay,
            current_month_pay=0,
            current_month_percents=0,
            method_of_ensuring=ensuring_method,
            money_destination=money_destination,
            target_account_id=account_id
        )

        info_text = 'Подана заявка на кредит.'
        Transaction.objects.create(client=client,
                                   product=credit,
                                   info=info_text,
                                   type=Transaction.TYPE_CREDIT_REQUEST)
        return credit

    def confirm(self):
        if self.status != self.STATUS_REQUESTED:
            return False
        bank_confirmation = BankSystemProxy.credit_create(self.client.id,
                                                          self.template.id,
                                                          float(self.residue.amount),
                                                          self.duration,
                                                          float(self.annual_percentage_rate))
        if not bank_confirmation:
            self.reject('Отказано банком')
            return False

        if self.money_destination == Credit.INTO_ACCOUNT:
            account = Account.objects.get(pk=self.target_account_id)
            account.confirm()
            account.put_money(self.residue.amount)
            account.save()

        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Заявка на кредит одобрена.',
                                   type=Transaction.TYPE_CREDIT_CONFIRM)

        Contract.objects.create(client=self.client,
                                product=self)
        self.is_active = True
        self.status = Credit.STATUS_OPENED
        self.save()
        return True

    def reject(self, cause):
        if self.status != self.STATUS_REQUESTED:
            return False
        self.status = Credit.STATUS_REJECTED
        self.save()
        account = Account.objects.get(pk=self.target_account_id)
        if not account.is_active:
            account.reject(cause)
        Transaction.objects.create(client=self.client,
                                   product=self,
                                   info='Заявка на кредит отклонена. Причина: {}'.format(cause),
                                   type=Transaction.TYPE_CREDIT_REJECT)
        return True

    @staticmethod
    def _get_current_percentage(residue, percentage):
        """
        Percents for current residue from last month
        """
        # TODO: 30 days in a month and 365 in a year? #Yes!
        r = Decimal(residue)
        p = Decimal(percentage)
        return r * (p / Decimal(100.0)) * Decimal(30) / Decimal(365)

    @staticmethod
    def _min_monthly_pay(payment, percentage, duration):
        """
        This work in that way - func return value, allow you to payed credit till credit term,
        if you are not fall into the penalty
        The less each payment - the greater the overpayment.
        (yes, it can be sum of geom progression)
        """
        coef = Decimal(1.0) + percentage / Decimal(100.0) / Decimal(12.0)
        mult = Decimal(1.0) / coef
        for _ in range(duration):
            mult = (mult + Decimal(1.0)) / coef
        return payment / mult


class FinanceSettings(models.Model):
    SCORING_DEFAULT = {
        "warning_level": 0.85,
        "danger_level": 0.7,
    }

    CURRENCIES_DEFAULT = [
        'BYN',
        'USD',
        'EUR',
        'RUB',
    ]

    EXCHANGE_RATES_DEFAULT = {
        'BYN': 1.0,
        'USD': 1.9519,
        'EUR': 2.043,
        'RUB': 3.2182,
    }

    scoring = JSONField(null=False, default=SCORING_DEFAULT)
    currencies = ArrayField(models.CharField(max_length=3), default=CURRENCIES_DEFAULT)
    exchange_rates = JSONField(null=False, default=EXCHANGE_RATES_DEFAULT)

    @classmethod
    def get_instance(cls):
        instance = FinanceSettings.objects.first()
        if not instance:
            instance = cls.objects.create()
        return instance

    def update_exchange_rates(self):
        rates = BankSystemProxy.get_currency_rates()
        if not rates:
            logger.info('Error while updating currency info')
        else:
            rates['BYN'] = 1.0
            self.exchange_rates = rates
            self.currencies = rates.keys()
            self.save()

    class Meta:
        verbose_name = 'Finance settings'
        verbose_name_plural = 'Finance settings'
        permissions = (
            ('view_financesettings', 'Can view finance settings'),
        )
