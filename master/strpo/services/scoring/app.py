#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from os import path
from flask import Flask
from flask import json
from flask import request
from pickle import load
from pandas import DataFrame
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
scoring_obj = None
model_filename = './data/model.pkl'


cols = [
    'credit_limit',
    'credits_residue',
    'monthly_payment',
    'totally_paid',
    'current_delay',
    'delayed_count_5',
    'delayed_count_5_29',
    'delayed_count_30_59',
    'delayed_count_60_89',
    'delayed_count_90_+',
    'delayed_balance',
    'currency_CHF',
    'currency_EUR',
    'currency_RUB',
    'currency_USD',
]
default_data = {
    c: 0
    for c in cols
}


def get_score(data):
    pd_data = default_data.copy()
    for key in pd_data:
        if key in data:
            pd_data[key] = data[key]

    pd_data = DataFrame(pd_data, index=[1,])
    score = scoring_obj.predict_proba(pd_data[cols])
    return score[0][0]


@app.route('/api/credits/scoring/', methods=['POST'])
def scoring():
    try:
        return json.dumps({"scoring_result": get_score(request.json)})
    except Exception as e:
        raise BadRequest("Scoring counting failed. Details: {}".format(e))


def main():
    with open(model_filename) as f:
        global scoring_obj
        scoring_obj = load(f)
    app.run('0.0.0.0', port=8001)


if __name__ == '__main__':
    main()
