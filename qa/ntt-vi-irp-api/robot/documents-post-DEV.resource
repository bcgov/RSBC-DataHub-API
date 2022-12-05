*** Variables ***

# Small PDF
${PDF_BASE64} =  JVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJFICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgNSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdCi9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyCjw8Ci9Sb290IDMgMCBSCj4+CiUlRU9G

${DOCUMENT_POST_PAYLOAD_ADP} =  {
...  "type_code": "MV2721",
...  "mime_sub_type": "pdf",
...  "mime_type":"application",
...  "file_object": "${PDF_BASE64}",
...  "notice_type_code": "ADP",
...  "notice_subject_code": "PERS",
...  "pageCount": 1
...  }

${DOCUMENT_POST_PAYLOAD_IRP} =  {
...  "type_code": "MV2723",
...  "mime_sub_type": "pdf",
...  "mime_type":"application",
...  "file_object": "${PDF_BASE64}",
...  "notice_type_code": "IRP",
...  "notice_subject_code": "PERS",
...  "pageCount": 11
...  }

${DOCUMENT_POST_PAYLOAD_UL} =  {
...  "type_code": "MV2722",
...  "mime_sub_type": "pdf",
...  "mime_type":"application",
...  "file_object": "${PDF_BASE64}",
...  "notice_type_code": "UL",
...  "notice_subject_code": "PERS",
...  "pageCount": 65
...  }

${DOCUMENT_POST_PAYLOAD_IMP} =  {
...  "type_code": "VTICKET",
...  "mime_sub_type": "pdf",
...  "mime_type":"application",
...  "file_object": "${PDF_BASE64}",
...  "notice_type_code": "IMP",
...  "notice_subject_code": "VEHI",
...  "pageCount": 99
...  }

${DOCUMENT_POST_PAYLOAD_INVALID_NOTICE_SUBJECT} =  {
...  "type_code": "VTICKET",
...  "mime_sub_type": "pdf",
...  "mime_type":"application",
...  "file_object": "${PDF_BASE64}",
...  "notice_type_code": "IMP",
...  "notice_subject_code": "FINGERPRINTS",
...  "pageCount": 99
...  }

${DOCUMENT_POST_PAYLOAD_INVALID_NOTICE_TYPE} =  {
...  "type_code": "VTICKET",
...  "mime_sub_type": "pdf",
...  "mime_type":"application",
...  "file_object": "${PDF_BASE64}",
...  "notice_type_code": "GOODNESS_GRACIOUS",
...  "notice_subject_code": "VEHI",
...  "pageCount": 99
...  }

${DOCUMENT_POST_PAYLOAD_EMPTY_FILE_OBJECT} =  {
...  "type_code": "MV2721",
...  "mime_sub_type": "pdf",
...  "mime_type":"application",
...  "file_object": "",
...  "notice_type_code": "ADP",
...  "notice_subject_code": "PERS",
...  "pageCount": 1
...  }

${DOCUMENT_POST_PAYLOAD_MISSING_FILE_OBJECT} =  {
...  "type_code": "MV2721",
...  "mime_sub_type": "pdf",
...  "mime_type":"application",
...  "notice_type_code": "ADP",
...  "notice_subject_code": "PERS",
...  "pageCount": 1
...  }

${DOCUMENT_POST_PAYLOAD_EMPTY_TYPE_CODE} =  {
...  "type_code": "",
...  "mime_sub_type": "pdf",
...  "mime_type":"application",
...  "file_object": "${PDF_BASE64}",
...  "notice_type_code": "ADP",
...  "notice_subject_code": "PERS",
...  "pageCount": 1
...  }

${DOCUMENT_POST_PAYLOAD_MISSING_TYPE_CODE} =  {
...  "mime_sub_type": "pdf",
...  "mime_type":"application",
...  "file_object": "${PDF_BASE64}",
...  "notice_type_code": "ADP",
...  "notice_subject_code": "PERS",
...  "pageCount": 1
...  }