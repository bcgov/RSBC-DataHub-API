# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from python.vips_mock_svc.vips_mock_svc.v1.api import validate, require_basic_authentication
from flask import request, g

from . import Resource
from .. import schemas


class DigitalFormsDocument(Resource):

    @require_basic_authentication
    def get(self, noticeNo, correlationId):
        data = self.get_json_data("df_payloads")
        if data:
            results = data.get(noticeNo)
            if results:
                return results
        return {"message": "not found"}, 404
