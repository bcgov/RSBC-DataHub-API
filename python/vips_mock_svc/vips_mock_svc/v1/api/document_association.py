# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from python.vips_mock_svc.vips_mock_svc.v1.api import require_basic_authentication, validate
from python.vips_mock_svc.vips_mock_svc.validation_schema import document_association
from . import Resource
from .. import schemas


class DocumentAssociation(Resource):

    @validate(document_association)
    @require_basic_authentication
    def post(self, documentId, correlationId):

        return {"respCd": 0, "respMsg": "string"}, 201
