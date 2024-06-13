# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from python.vips_mock_svc.vips_mock_svc.validation_schema import document
from python.vips_mock_svc.vips_mock_svc.v1.api import require_basic_authentication, validate
import logging
from flask import request

from . import Resource


class Document(Resource):
    """
    Single Document Object
    """

    @require_basic_authentication
    def get(self, documentId, correlationId):
        """
        Returns either a base64 encoded PDF or URL
        depending on the query parameter submitted
        """
        b64 = request.args.get("b64")
        url = request.args.get("url")
        if url:
            return {"document_id": "string"}, 200
        elif b64:
            return {"document_id": "base64-string"}, 200
        else:
            return {"message": "bad request"}, 400


class DocumentsList(Resource):
    """
    List of Document Objects
    """

    @require_basic_authentication
    def get(self, correlationId):
        logging.warning("inside get()")
        data = self.get_json_data("documents")
        if data:
            document_list = []
            for document_id in data:
                document_list.append(data[document_id])
            return document_list, 200
        else:
            return {"message": "not found"}, 404

    @require_basic_authentication
    @validate(document)
    def post(self, correlationId):

        return {"document_id": "000"}, 201, None
