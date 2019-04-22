#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


if __name__ == '__main__':
    data = pd.read_csv('data/initial.csv.gz', compression='gzip', low_memory=True)
    data = data.loc[data['loan_status'].isin(['Fully Paid', 'Charged Off'])]
    data['loan_status'] = data['loan_status'].apply(lambda v: np.float(v == 'Charged Off'))

    drop_list = []
    for col in data.columns:
        if data[col].nunique() == 1:
            drop_list.append(col)


    print(data.info())