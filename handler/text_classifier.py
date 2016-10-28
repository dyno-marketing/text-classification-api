__author__ = 'tuanvu'
__create_time__ = '19/06/2015 11:14 AM'

import datetime
from flask import make_response, request
from flask.ext import restful
import json
import logging
from report.shop_report import get_view_item_mongo, get_click_item_mongo


class ShopReportHandler(restful.Resource):
    def __init__(self, *argc, **argkw):
        self.logger = logging.getLogger(__name__)

    def get(self, project):
        result = {}
        try:
            owner_id = request.args.get('owner_id', 0)
            start_time = request.args.get('start_time', "")
            end_time = request.args.get('end_time', "")
            type = request.args.get('type', "")
        except Exception:
            result['result'] = []
            result['msg'] = "can not get atttribute"
            self.logger.info(str(datetime.datetime.now()) + ": " + "can not get parameters!")

        if type == "click":
            result['result'] = get_click_item_mongo(int(owner_id), start_time, end_time, project)
            result['msg'] = "click successful"
        elif type == "view":
            result['result'] = get_view_item_mongo(int(owner_id), start_time, end_time, project)
            result['msg'] = "view successful"
        else:
            result['result'] = []
            result['msg'] = "type failure"

        response = make_response(json.dumps(result))
        response.headers['Content-type'] = 'application/json'
        return response
