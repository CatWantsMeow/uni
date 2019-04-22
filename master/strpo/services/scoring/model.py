# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import wget
import pandas as pd
from pickle import dump
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingClassifier


pd.options.mode.chained_assignment = None
rate = 3.32 / 100

base_url = 'https://static.tcsbank.ru/documents/olymp/'
accounts_source = base_url + "SAMPLE_ACCOUNTS.csv"
customers_source = base_url + "SAMPLE_CUSTOMERS.csv"

accounts_filename = './data/accounts.csv'
customers_filename = './data/customers.csv'
processed_accounts_filename = './data/processed_accounts.csv'
model_filename = './data/model.pkl'


def fetch_data():
    wget.download(customers_source, out=customers_filename)
    wget.download(accounts_source, out=accounts_filename)


def process_data(customers, accounts):
    accounts['final_pmt_date'][accounts.final_pmt_date.isnull()] = accounts['fact_close_date'][accounts.final_pmt_date.isnull()]
    accounts['final_pmt_date'].fillna(0, inplace=True)

    latest_recourse = accounts.pivot_table(
        ['inf_confirm_date'],
        ['tcs_customer_id', 'open_date', 'final_pmt_date', 'credit_limit', 'currency'],
        aggfunc='max'
    )
    accounts = accounts.merge(
        latest_recourse,
        'left',
        left_on=['tcs_customer_id', 'open_date', 'final_pmt_date', 'credit_limit', 'currency'],
        right_index=True,
        suffixes=('', '_max'),
    )

    accounts = accounts.drop(
        ['pmt_string_84m', 'pmt_freq', 'type', 'relationship', 'bureau_cd', 'status'],
        axis=1
    )
    accounts.fact_close_date[accounts.fact_close_date.notnull()] = 1
    accounts.fact_close_date.fillna(0, inplace=True)

    accounts = accounts[accounts.inf_confirm_date == accounts.inf_confirm_date_max].drop_duplicates()
    accounts = accounts.groupby(
        ['tcs_customer_id', 'open_date', 'final_pmt_date', 'credit_limit', 'currency']
    ).max().reset_index()

    accounts = accounts.drop([
        'bki_request_date',
        'inf_confirm_date',
        'pmt_string_start',
        'interest_rate',
        'open_date',
        'final_pmt_date',
        'inf_confirm_date_max',
    ], axis=1)

    cols = [
        'credit_limit',
        'outstanding',
        'next_pmt',
        'delq_balance',
        'max_delq_balance',
        'curr_balance_amt'
    ]
    for col in cols:
        accounts[col] = accounts[col] * rate

    values = ['RUB', 'USD', 'EUR', 'CHF']
    currency_data = pd.DataFrame([
        {
            'currency_{}'.format(j): str(i).count(str(j))
            for j in values
        }
        for i in accounts['currency']
    ])
    accounts = accounts.join(currency_data).drop(['currency'], axis=1)

    accounts['credits_count'] = 1
    accounts.fillna(0, inplace=True)
    accounts = accounts.groupby('tcs_customer_id').sum()
    return customers, accounts


def train(customers, accounts):
    customers.set_index('tcs_customer_id', inplace=True)
    united_df = accounts.join(customers)
    train_df = united_df[united_df['sample_type'] == 'train'].drop(['sample_type'], axis=1)
    target = train_df['bad'].values

    corr_coeffs = train_df.corr()
    fields_to_drop = [
        i for i in corr_coeffs
        if corr_coeffs[i].isnull().drop_duplicates().values[0]
    ]

    most_corr = []
    for i in corr_coeffs:
        for j in corr_coeffs.index[corr_coeffs[i] > 0.9]:
            if i <> j and j not in most_corr and i not in most_corr:
                most_corr.append(j)
        for j in corr_coeffs.index[abs(corr_coeffs[i]) < -1e-5]:
            if i <> j and j not in most_corr and i not in most_corr:
                most_corr.append(j)
    fields_to_drop.extend(most_corr)
    train_df = train_df.drop(fields_to_drop + ['bad', 'fact_close_date', 'tcs_customer_id'], axis=1)
    print(train_df.keys())

    chunk = 5000
    model = GradientBoostingClassifier(max_depth=4)
    model.fit(train_df.values[:-chunk], target[:-chunk])
    with open(model_filename, 'w+') as f:
        dump(model, f)

    train = train_df.values[-chunk:]
    target = target[-chunk:]
    predicted = model.predict(train)
    print sum(1 if x == y else 0 for x, y in zip(predicted, target)) / float(len(train))


def main():
    if not os.path.exists(accounts_filename) or not os.path.exists(customers_filename):
        fetch_data()

    customers = pd.read_csv(customers_filename, ';')
    accounts = pd.read_csv(accounts_filename, ";", decimal=',', low_memory=False)

    if not os.path.exists(processed_accounts_filename):
        customers, accounts = process_data(customers, accounts)
        accounts.to_csv(processed_accounts_filename, ";", decimal=',')

    accounts = pd.read_csv(processed_accounts_filename, ";", decimal=',', )
    train(customers, accounts)


if __name__ == '__main__':
    main()