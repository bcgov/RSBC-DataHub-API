# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from python.vips_mock_svc.vips_mock_svc.v1.api import validate, require_basic_authentication
from python.vips_mock_svc.vips_mock_svc.validation_schema import impoundment

from . import Resource


class Impoundments(Resource):

    @require_basic_authentication
    def get(self, noticeNo, correlationId):
        data = self.get_json_data("impoundments")
        if noticeNo in data:
            return data[noticeNo], 200
        else:
            return {"message": "not found"}, 404

    @require_basic_authentication
    @validate(impoundment)
    def post(self, correlationId):
        return {"vipsImpoundmentId": 0, "dfId": 0, "respMsg": "string"}, 201
