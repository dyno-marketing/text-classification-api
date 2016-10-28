# -*- coding: utf-8 -*-
__author__ = 'daotuanvu'
create_date = '2/6/2015'

import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')
import os
import logging.config
import logging
import yaml
from flask import Flask
import flask_restful
# from flask_restful.representations.json import output_json

# output_json.func_globals['settings'] = {'ensure_ascii': False, 'encoding': 'utf8'}
app = Flask(__name__)
api = flask_restful.Api(app)

from handler.text_classifier import TextClassifier

api.add_resource(TextClassifier, r"/text_classifier")


# Setup logging configuration
def setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
