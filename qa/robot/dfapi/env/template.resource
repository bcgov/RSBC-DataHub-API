[Documentation]  Credentials and URLs for the DFAPI DEV enviroment, when run on a pod itself.

*** Variables ***
${ORDS_USER}            username
${ORDS_PASS}            password
${ORDS_ENDPOINT}        https://url

${DFAPI_SERVER_HOST}    server
${DFAPI_VERIFY_CERTS}   False
${DFAPI_SERVER_PATH}    digitalforms
${DFAPI_API_VERSION}    1.1.0
${DFAPI_AUTH_USER}      user
${DFAPI_AUTH_PASS}      password

# ADP test record
${ADP_REC_PROHIBITION_NUM}  00000000
${ADP_REC_PROHIBITION_ID}   1234
${ADP_REC_CORRELATION_ID}   9999
${ADP_REC_DOCUMENT_ID}      1000
${ADP_REC_JSON} =  {
...    "applicationInfo": {
...      "email": "",
...      "faxNo": "",
...      "firstGivenNm": "",
...      "formData": "",
...      "manualEntryYN": "",
...      "noticeSubjectCd": "",
...      "phoneNo": "",
...      "presentationTypeCd": "",
...      "reviewRoleTypeCd": "",
...      "secondGivenNm": "",
...      "surnameNm": ""
...    }
...  }

# IRP test record
${IRP_REC_PROHIBITION_NUM}  11111111
${IRP_REC_PROHIBITION_ID}   1235
${IRP_REC_CORRELATION_ID}   9998
${IRP_REC_DOCUMENT_ID}      2000
${IRP_REC_JSON} =  {
...    "applicationInfo": {
...      "email": "",
...      "faxNo": "",
...      "firstGivenNm": "",
...      "formData": "",
...      "manualEntryYN": "",
...      "noticeSubjectCd": "",
...      "phoneNo": "",
...      "presentationTypeCd": "",
...      "reviewRoleTypeCd": "",
...      "secondGivenNm": "",
...      "surnameNm": ""
...    }
...  }

# UL test record
${UL_REC_PROHIBITION_NUM} 22222222
${UL_REC_PROHIBITION_ID}  1236
${UL_REC_CORRELATION_ID}  9997
${UL_REC_DOCUMENT_ID}     30009
${UL_REC_JSON} =  {
...    "applicationInfo": {
...      "email": "",
...      "faxNo": "",
...      "firstGivenNm": "",
...      "formData": "",
...      "manualEntryYN": "",
...      "noticeSubjectCd": "",
...      "phoneNo": "",
...      "presentationTypeCd": "",
...      "reviewRoleTypeCd": "",
...      "secondGivenNm": "",
...      "surnameNm": ""
...    }
...  }
