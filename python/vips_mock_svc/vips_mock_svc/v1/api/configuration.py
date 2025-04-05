# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from python.vips_mock_svc.vips_mock_svc.v1.api import require_basic_authentication

from . import Resource


class Configuration(Resource):

    @require_basic_authentication
    def get(self, correlationId):
        data = self.get_json_data("configuration")
        if data:
            return data, 200
        return {}