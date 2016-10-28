__author__ = 'tuanvu'
__create_time__ = '19/06/2015 11:14 AM'

import json
import logging

import flask_restful
from flask import make_response, request
from sklearn.externals import joblib
import pandas as pd

tfidf = joblib.load('model/tfidf_model.pkl')
model = joblib.load('model/prediction_model.pkl')


class TextClassifier(flask_restful.Resource):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def post(self):
        json_data = request.get_json(force=True)
        id = json_data['id']
        name = json_data['name']

        df = pd.DataFrame(columns=('id', 'name'))

        row = dict(zip(['id', 'name'], [id, name]))
        row_s = pd.Series(row)
        row_s.name = 1
        df = df.append(row_s)

        print(df["name"])

        print(tfidf.transform(df["name"]).toarray())

        class_name = model.predict(tfidf.transform(df["name"]).toarray())[0]

        result = {"class_name": class_name}

        response = make_response(json.dumps(result))
        response.headers['Content-type'] = 'application/json'
        return response
