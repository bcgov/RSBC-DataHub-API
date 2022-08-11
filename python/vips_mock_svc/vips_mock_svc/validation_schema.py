impoundment = {
    "respMsg": {
        "type": "string",
        "required": True
    },
    "driverLicenceNo": {
        "type": "string",
    },
    "icbcTransmissionCd": {
        "type": "string"
    },
    "impoundLotOperatorId": {
        "type": "integer"
    },
    "result": {
        "type": "dict",
        "required": True,
        "schema": {
            "dfId": {
                "type": "integer"
            },
            "cancelled": {
                "type": "boolean"
            },
            "dlJurisdictionCd": {
                "type": "string"
            },
            "documents": {
                "type": "list",
                "schema": {
                    "type": "dict",
                    "schema": {
                        "documentId": {
                            "type": "integer"
                        }
                    }
                }
            }
        }
    }
}

document = {
    "type_code": {
        "type": "string",
        "required": True
    },
    "mime_type": {
        "type": "string",
        "required": True
    },
    "mime_sub_type": {
        "type": "string",
        "required": True
    },
    "auth_guid": {
        "type": "string",
        "required": True
    },
    "file_object": {
        "type": "string",
        "required": True
    },
    "pageCount": {
        "type": "integer",
        "required": True
    },
}


prohibition = {
    "respMsg": {
        "type": "string",
        "required": True
    },
    "driverLicenceNo": {
        "type": "string",
    },
    "icbcTransmissionCd": {
        "type": "string"
    },
    "impoundLotOperatorId": {
        "type": "integer"
    },
    "result": {
        "type": "dict",
        "required": True,
        "schema": {
            "dfId": {
                "type": "integer"
            },
            "cancelled": {
                "type": "boolean"
            },
            "dlJurisdictionCd": {
                "type": "string"
            },
            "documents": {
                "type": "list",
                "schema": {
                    "type": "dict",
                    "schema": {
                        "documentId": {
                            "type": "integer"
                        }
                    }
                }
            }
        }
    }
}

document_association = {
    "noticeNo": {
        "type": "string",
        "required": True
    },
    "noticeTypeCd": {
        "type": "string",
        "required": True
    }
}
