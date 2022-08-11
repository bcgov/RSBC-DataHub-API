# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.impoundments import Impoundments
from .api.prohibitions import Prohibitions
from .api.documents import Document, DocumentsList
from .api.document_association import DocumentAssociation
from .api.digital_forms_document import DigitalFormsDocument
from .api.configuration import Configuration


routes = [
    dict(resource=Impoundments, urls=['/impoundments/<correlationId>'], endpoint='impoundments_correlationId'),
    dict(resource=Impoundments, urls=['/impoundments/<noticeNo>/<correlationId>'], endpoint='impoundments_impoundmentId_correlationId'),
    dict(resource=Prohibitions, urls=['/prohibitions/<correlationId>'], endpoint='prohibitions_correlationId'),
    dict(resource=Prohibitions, urls=['/prohibitions/<noticeNo>/<correlationId>'], endpoint='prohibitions_prohibitionId_correlationId'),
    dict(resource=Document, urls=['/documents/<documentId>/<correlationId>'], endpoint='documents_get'),
    dict(resource=DocumentsList, urls=['/documents/list/<correlationId>'], endpoint='documents_index'),
    dict(resource=DocumentAssociation, urls=['/documents/association/notice/<documentId>/<correlationId>'], endpoint='document_association'),
    dict(resource=DigitalFormsDocument, urls=['/dfDocument/<noticeNo>/<correlationId>'], endpoint='dfDocument_get'),
    dict(resource=Configuration, urls=['/configuration/<correlationId>'], endpoint='configuration_correlationId'),
]