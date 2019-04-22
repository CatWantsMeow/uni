# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from finance.api.accounts.views import AccountView
from finance.api.contracts.views import ContractView
from finance.api.credits.views import CreditTemplateView, CreditView
from finance.api.settings.views import FinanceSettingsView
from finance.api.transactions.views import TransactionView

router = DefaultRouter()
router.register('contracts', ContractView, base_name='contracts')
router.register('transactions', TransactionView, base_name='transactions')
router.register('accounts', AccountView, base_name='accounts')
router.register('credits/templates', CreditTemplateView, base_name='credit-templates')
router.register('credits', CreditView, base_name='credits')
router.register('settings', FinanceSettingsView, base_name='finance-settings')

urlpatterns = [
    url(r'^api/', include(router.urls))
]
