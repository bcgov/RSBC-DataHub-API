# Robot Framework regression test suite for the Digital Forms API
#
# For more information, see https://robotframework.org
# See Jira Zephyr tests: https://justice.gov.bc.ca/jirarsi/projects/DF?selectedItem=com.thed.zephyr.je%3Azephyr-tests-page#test-cycles-tab
#
# Notes:
# - To disable warnings about self-assigned certificates:
#   export PYTHONWARNINGS="ignore:Unverified HTTPS request"
# - To use the DFAPI, you must NOT be connected to the VPN.
# - To use the ORDS helper API, you MUST be connected to the VPN.
#
# Usage:
#  1. Install Python 3 and Robot Framework.
#  2. Log in to OpenShift/Kubernetes:
#     $ oc login --token=TOKEN --server=SERVER
#  3. Run Robot Framework script:
#     $ robot --loglevel DEBUG --debugfile dfapi.log --outputdir results --exitonfailure dfapi.robot


*** Settings ***
Library      RequestsLibrary  # https://github.com/MarketSquare/robotframework-requests
Library      Collections      # Used to check header response from RequestsLibrary
Library      String           # https://robotframework.org/robotframework/latest/libraries/String.html
Library      Process          # https://robotframework.org/robotframework/latest/libraries/Process.html
Library      OperatingSystem  # https://robotframework.org/robotframework/latest/libraries/OperatingSystem.html
Library      DateTime         # https://robotframework.org/robotframework/latest/libraries/DateTime.html

# Load URLs, credentials, and settings from a resource table. To create a resource table, copy the file
# env/template.resource to a new file, add the appropriate values. Files ending in .resource are ignored by git. See:
# http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#resource-and-variable-files
#Resource     env/dfapi-dev-ocp4.resource
Resource     env/dfapi-test-ocp4.resource

Suite Setup  Create DFAPI session


*** Variables ***
# See Resource file env/dfapi-*-ocp4.resource for variables.

*** Keywords ***
# See Resource file env/dfapi-*-ocp4.resource for keywords.



# =======================================================================================
#      _       _       _       _______        _                                   _       _       _    
#   /\| |/\ /\| |/\ /\| |/\   |__   __|      | |                               /\| |/\ /\| |/\ /\| |/\ 
#   \ ` ' / \ ` ' / \ ` ' /      | | ___  ___| |_    ___ __ _ ___  ___  ___    \ ` ' / \ ` ' / \ ` ' / 
#  |_     _|_     _|_     _|     | |/ _ \/ __| __|  / __/ _` / __|/ _ \/ __|  |_     _|_     _|_     _|
#   / , . \ / , . \ / , . \      | |  __/\__ \ |_  | (_| (_| \__ \  __/\__ \   / , . \ / , . \ / , . \ 
#   \/|_|\/ \/|_|\/ \/|_|\/      |_|\___||___/\__|  \___\__,_|___/\___||___/   \/|_|\/ \/|_|\/ \/|_|\/ 
#
# =======================================================================================
*** Test Cases ***


Swagger UI page is available
    [Tags]           Swagger
    [Documentation]  This is an HTML shell that loads and renders the OpenAPI specification with CSS and JavaScript.
    Given Swagger HTML page is available
    Then Response code is         200
    And Response content type is  text/html
    And Response body contains    <title>Swagger UI</title>

Swagger Specification is available
    [Tags]           Swagger
    [Documentation]  This is the OpenAPI specification for the DFAPI. Ensure it contains expected sections and version.
    Given Open API specification is available
    Then Response code is         200
    And Response content type is  application/json
    And Response body contains    "swagger":"2.0"
    And Response body contains    Digital Forms API
    And Response body contains    "version":"${DFAPI_API_VERSION}"
    And Response body contains    {"name":"Application Form","description":"Application Form Controller"}
    And Response body contains    {"name":"Disclosure","description":"Disclosure Controller"}
    And Response body contains    {"name":"Payment","description":"Payment Service Controller"}
    And Response body contains    {"name":"Query","description":"Query Service Controller"}
    And Response body contains    {"name":"Review Scheduling","description":"Schedule Review Controller"}
    And Response body contains    {"name":"Utilities","description":"Utility Controller"}

Unauthenticated requests are rejected
    [Tags]           Utilities
    [Documentation]  Ensure that authorisation is needed to access the API endpoint.
    Given Utility ping with no authentication
    Then Response code is         401
    And Response content type is  application/json
    And Response body contains    Unauthorized entry, please authenticate

Utility Ping is available
    [Tags]           Utilities
    [Documentation]  Ensure the "ping" healthcheck function responds.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/api/utility/ping``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"responseMessage":{"VIPS ORDS Health Status":"success","DIGITAL FORMS ORDS Health Status":"success"},"timeDt":"2021-07-21T23:10Z"}``
    Given Utility ping
    Then Response code is         200
    And Response content type is  application/json
    And Response body contains    "VIPS ORDS Health Status":"success"
    And Response body contains    "DIGITAL FORMS ORDS Health Status":"success"

Reset VIPS scheduled reviews using ORDS
    [Tags]           Utilities  ORDS
    [Documentation]  Delete application reviews times from previous testing. Uses back-end ORDS endpoint specifically built for testing in DEV and TEST.
    ...  \n\nExample request from API 1.1.0:\n\n ``DELETE https://ords.svc/ords/deva/vipsords/web/prohibition/21900104/review/schedule/ADP/182``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"status_code": "0","status_message": "Success" }``
    ...  Note: the review type (e.g. "ADP") MUST match the prohibition number type in the database (e.g. prohibition "21900104" in the datbase must be set to ADP) or you will get back an HTTP 400 error with no explanation of what went wrong.
    Given ORDS delete reviews     ${ADP_REC_PROHIBITION_NUM}  ADP  ${ADP_REC_PROHIBITION_ID}
    And ORDS delete reviews       ${IRP_REC_PROHIBITION_NUM}  IRP  ${IRP_REC_PROHIBITION_ID}
    And ORDS delete reviews       ${UL_REC_PROHIBITION_NUM}  UL  ${UL_REC_PROHIBITION_ID}
    Then Response code is         200

Reset VIPS applications using ORDS
    [Tags]           Utilities  ORDS
    [Documentation]  Delete applications from previous testing. Uses back-end ORDS endpoint specifically built for testing in DEV and TEST. This endpoint
    ...  always returns HTTP 200 and "success", so checking for that may not be useful.
    ...  \n\nExample request from API 1.1.0:\n\n ``DELETE https://ords.svc/ords/deva/rsdfrmords/web/digitalForm/prohibition/182/12345``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"status_code": "0","status_message": "Success" }``
    Given ORDS delete application  ${ADP_REC_PROHIBITION_ID}  ${ADP_REC_CORRELATION_ID}
    Then Response code is          200
    And ORDS delete application    ${IRP_REC_PROHIBITION_ID}  ${IRP_REC_CORRELATION_ID}
    Then Response code is          200
    And ORDS delete application    ${UL_REC_PROHIBITION_ID}  ${UL_REC_CORRELATION_ID}
    Then Response code is          200

Query application status for ADP before submission
    [Tags]           ADP  GET status
    [Documentation]  Queries prohibition before an application has been made. Should have been fully reset by ORDS call.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/21900104/status/123123``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"status":{"noticeTypeCd":"ADP","noticeServedDt":"2020-08-15 00:00:00 -08:00","reviewFormSubmittedYn":"N","reviewCreatedYn":"N","originalCause":"ADP09412","surnameNm":"Gordon","driverLicenceSeizedYn":"Y","disclosure":[],"reviews":[]}}} ``
    Given Query status for application  ${ADP_REC_PROHIBITION_NUM}  123123
    Then response code is                200
    And Response body contains          "resp":"success"
    And Response body contains          "reviewCreatedYn":"N"
    And Response body contains          "reviewFormSubmittedYn":"N"
    And Response body contains          "reviews":[]
    And Response body contains          "disclosure":[]
    And Response body does not contain  "reviewStatus"
    And Query response matches ADP record
 
Query application status for IRP before submission
    [Tags]           IRP  GET status
    [Documentation]  Queries prohibition before an application has been made. Should have been fully reset by ORDS call.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/21900051/status/123124``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"status":{"noticeTypeCd":"IRP","noticeServedDt":"2020-08-15 00:00:00 -08:00","reviewFormSubmittedYn":"N","reviewCreatedYn":"N","originalCause":"IRP90FAIL","surnameNm":"Gordon","driverLicenceSeizedYn":"N","disclosure":[],"reviews":[]}}} ``
    Given Query status for application  ${IRP_REC_PROHIBITION_NUM}  123124
    Then response code is               200
    And Response body contains          "resp":"success"
    And Response body contains          "reviewCreatedYn":"N"
    And Response body contains          "reviewFormSubmittedYn":"N"
    And Response body contains          "reviews":[]
    And Response body contains          "disclosure":[]
    And Response body does not contain  "reviewStatus"
    And Query response matches IRP record

Query application status for UL before submission
    [Tags]           UL  GET status
    [Documentation]  Queries prohibition before an application has been made. Should have been fully reset by ORDS call.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/21900308/status/123125``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"status":{"noticeTypeCd":"UL","noticeServedDt":"2020-08-15 00:00:00 -08:00","reviewFormSubmittedYn":"N","reviewCreatedYn":"N","originalCause":"IRPINDEF","surnameNm":"Gordon","driverLicenceSeizedYn":"N","disclosure":[],"reviews":[]}}} ``
    Given Query status for application  ${UL_REC_PROHIBITION_NUM}  123125
    Then response code is               200
    And Response body contains          "reviewCreatedYn":"N"
    And Response body contains          "reviewFormSubmittedYn":"N"
    And Response body contains          "reviews":[]
    And Response body contains          "disclosure":[]
    And Response body does not contain  "reviewStatus"
    And Query response matches UL record

Submit VIPS ADP application
    [Tags]           ADP  POST application
    [Documentation]  Submits an application. If you call the DFAPI endpoint multiple times without ORDS first, the DFAPI will reply with a new GUID applicationId, and the first applicationId will no longer exist in the system. This should not happen in production because the Digital Forms system checks to see if an application already exists. Just be aware that the DFAPI will let you submit an application multiple times.
    ...  \n\nExample request from API 1.1.0:\n\n ``POST http://dfapi.svc/digitalforms/ADP/21900104/application/2301``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"applicationInfo":{"applicationId":"c7aa2b33-f52f-4aaa-e054-00144ffbc109","createdTime":"2021-07-21 16:10:33 -08:00"}}}``
    Given POST new application  ADP  ${ADP_REC_PROHIBITION_NUM}  ${ADP_REC_CORRELATION_ID}  ${ADP_REC_JSON}
    Then Response code is       201
    And Response body contains  "resp":"success"
    And response body contains  applicationId
    And response body contains  createdTime
    And Set suite variable      ${ADP_APPLICATION_RESPONSE}  ${test_response.json()}
    And set suite variable      ${ADP_APPLICATION_GUID}  ${test_response.json()['data']['applicationInfo']['applicationId']}

Submit VIPS IRP application
    [Tags]           IRP  POST application
    [Documentation]  Submits an application. If you call the DFAPI endpoint multiple times without ORDS first, the DFAPI will reply with a new GUID applicationId, and the first applicationId will no longer exist in the system. This should not happen in production because the Digital Forms system checks to see if an application already exists. Just be aware that the DFAPI will let you submit an application multiple times.
    ...  \n\nExample request from API 1.1.0:\n\n ``POST http://dfapi.svc/digitalforms/IRP/21900051/application/2401``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"applicationInfo":{"applicationId":"c7aa2b33-f530-4aaa-e054-00144ffbc109","createdTime":"2021-07-21 16:10:33 -08:00"}}} ``
    Given POST new application  IRP  ${IRP_REC_PROHIBITION_NUM}  ${IRP_REC_CORRELATION_ID}  ${IRP_REC_JSON}
    Then Response code is       201
    And Response body contains  "resp":"success"
    And response body contains  applicationId
    And response body contains  createdTime
    And set suite variable      ${IRP_APPLICATION_RESPONSE}  ${test_response.json()}
    And set suite variable      ${IRP_APPLICATION_GUID}  ${test_response.json()['data']['applicationInfo']['applicationId']}

Submit VIPS UL application
    [Tags]           UL  POST application
    [Documentation]  Submits an application. If you call the DFAPI endpoint multiple times without ORDS first, the DFAPI will reply with a new GUID applicationId, and the first applicationId will no longer exist in the system. This should not happen in production because the Digital Forms system checks to see if an application already exists. Just be aware that the DFAPI will let you submit an application multiple times.
    ...  \n\nExample request from API 1.1.0:\n\n ``POST http://dfapi.svc/digitalforms/UL/21900308/application/2501``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"applicationInfo":{"applicationId":"c7aa2b33-f531-4aaa-e054-00144ffbc109","createdTime":"2021-07-21 16:10:33 -08:00"}}} ``
    Given POST new application  UL  ${UL_REC_PROHIBITION_NUM}  ${UL_REC_CORRELATION_ID}  ${UL_REC_JSON}
    Then Response code is       201
    And Response body contains  "resp":"success"
    And response body contains  applicationId
    And response body contains  createdTime
    And set suite variable      ${UL_APPLICATION_RESPONSE}  ${test_response.json()}
    And set suite variable      ${UL_APPLICATION_GUID}  ${test_response.json()['data']['applicationInfo']['applicationId']}

Get submitted ADP VIPS record
    [Tags]           ADP  GET application
    [Documentation]  Retrieves information about the application. 
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/c7aa2b33-f52f-4aaa-e054-00144ffbc109/application/2301``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"applicationInfo":{"prohibitionNoticeNo":"21900104","noticeTypeCd":"ADP","reviewApplnTypeCd":"ADP","noticeSubjectCd":"PERS","presentationTypeCd":"WRIT","reviewRoleTypeCd":"APPNT","firstGivenNm":"Larry","secondGivenNm":"ADP","surnameNm":"Lungpayne","phoneNo":"2501113333","faxNo":"2501112222","email":"user@gov.bc.ca","manualEntryYN":"N","formData":"PD94...="}}}``
    Given GET application       ${ADP_APPLICATION_GUID}  ${ADP_REC_CORRELATION_ID}
    Then response code is       200
    And Response body contains  "resp":"success"
    And Application GET response matches expected ADP record

Get submitted IRP VIPS record
    [Tags]           IRP  GET application
    [Documentation]  Retrieves information about the application.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/c7aa2b33-f530-4aaa-e054-00144ffbc109/application/2401``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"applicationInfo":{"prohibitionNoticeNo":"21900051","noticeTypeCd":"IRP","reviewApplnTypeCd":"IRP","noticeSubjectCd":"PERS","presentationTypeCd":"WRIT","reviewRoleTypeCd":"APPNT","firstGivenNm":"Billy","secondGivenNm":"IRP","surnameNm":"Backpayne","phoneNo":"2501113333","faxNo":"2501112222","email":"user@gov.bc.ca","manualEntryYN":"N","formData":"PD94...="}}} ``
    Given GET application       ${IRP_APPLICATION_GUID}  ${IRP_REC_CORRELATION_ID}
    Then response code is       200
    And Response body contains  "resp":"success"
    And Application GET response matches expected IRP record

Get submitted UL VIPS record
    [Tags]           UL  GET application
    [Documentation]  Retrieves information about the application.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/c7aa2b33-f531-4aaa-e054-00144ffbc109/application/2501``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"applicationInfo":{"prohibitionNoticeNo":"21900308","noticeTypeCd":"UL","reviewApplnTypeCd":"UL","noticeSubjectCd":"PERS","presentationTypeCd":"WRIT","reviewRoleTypeCd":"APPNT","firstGivenNm":"Harry","secondGivenNm":"UL","surnameNm":"Hairpayne","phoneNo":"2501113333","faxNo":"2501112222","email":"user@gov.bc.ca","manualEntryYN":"N","formData":"PD94...="}}} ``
    Given GET application       ${UL_APPLICATION_GUID}  ${UL_REC_CORRELATION_ID}
    Then response code is       200
    And Response body contains  "resp":"success"
    And Application GET response matches expected UL record

Patch submitted ADP application fields
    [Tags]           ADP  PATCH application
    [Documentation]  Updates fields in the application.
    ...  \n\nExample request from API 1.1.0:\n\n ``PATCH http://dfapi.svc/digitalforms/ADP/c7aa2b33-f52f-4aaa-e054-00144ffbc109/application/``\n\n2345
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"applicationInfo":{"applicationId":"c7aa2b33-f52f-4aaa-e054-00144ffbc109","updatedTime":"2021-07-21 16:10:34 -08:00"}}} ``
    Given PATCH application     ADP  ${ADP_APPLICATION_GUID}  2345  ${ADP_REC_JSON_UPDATED}
    Then response code is       200
    And Response body contains  "resp":"success"

Patch submitted IRP application fields
    [Tags]           IRP  PATCH application
    [Documentation]  Updates fields in the application.
    ...  \n\nExample request from API 1.1.0:\n\n ``PATCH http://dfapi.svc/digitalforms/IRP/c7aa2b33-f530-4aaa-e054-00144ffbc109/application/``\n\n2345
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"applicationInfo":{"applicationId":"c7aa2b33-f530-4aaa-e054-00144ffbc109","updatedTime":"2021-07-21 16:10:34 -08:00"}}}``
    Given PATCH application     IRP  ${IRP_APPLICATION_GUID}  2345  ${IRP_REC_JSON_UPDATED}
    Then response code is       200
    And Response body contains  "resp":"success"

Patch submitted UL application fields
    [Tags]           UL  PATCH application
    [Documentation]  Updates fields in the application.
    ...  \n\nExample request from API 1.1.0:\n\n ``PATCH http://dfapi.svc/digitalforms/UL/c7aa2b33-f531-4aaa-e054-00144ffbc109/application/``\n\n2345
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"applicationInfo":{"applicationId":"c7aa2b33-f531-4aaa-e054-00144ffbc109","updatedTime":"2021-07-21 16:10:34 -08:00"}}} ``
    Given PATCH application     UL  ${UL_APPLICATION_GUID}  2345  ${UL_REC_JSON_UPDATED}
    Then response code is       200
    And Response body contains  "resp":"success"

Get updated ADP VIPS record
    [Tags]           ADP  GET application
    [Documentation]  Retrieves the updated application information.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/c7aa2b33-f52f-4aaa-e054-00144ffbc109/application/2301``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"prohibitionNoticeNo":"21900104","noticeTypeCd":"ADP","reviewApplnTypeCd":"ADP","noticeSubjectCd":"PERS","presentationTypeCd":"ORAL","reviewRoleTypeCd":"LWYR","firstGivenNm":"Lenny","secondGivenNm":"Updated","surnameNm":"Legpayne","phoneNo":"8888888888","faxNo":"9999999999","email":"user@gov.bc.ca","manualEntryYN":"Y","formData":"PD94bW="}}} ``
    Given GET application       ${ADP_APPLICATION_GUID}  ${ADP_REC_CORRELATION_ID}
    Then response code is       200
    And Response body contains  "resp":"success"
    And Application GET response matches updated ADP record

Get updated IRP VIPS record
    [Tags]           IRP  GET application
    [Documentation]  Retrieves the updated application information.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/c7aa2b33-f530-4aaa-e054-00144ffbc109/application/2401``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"applicationInfo":{"prohibitionNoticeNo":"21900051","noticeTypeCd":"IRP","reviewApplnTypeCd":"IRP","noticeSubjectCd":"PERS","presentationTypeCd":"ORAL","reviewRoleTypeCd":"LWYR","firstGivenNm":"Bobby","secondGivenNm":"B.","surnameNm":"Brainpayne","phoneNo":"5555555555","faxNo":"4444444444","email":"user@gov.bc.ca","manualEntryYN":"N","formData":"PDF93="}}} ``
    Given GET application       ${IRP_APPLICATION_GUID}  ${IRP_REC_CORRELATION_ID}
    Then response code is       200
    And Response body contains  "resp":"success"
    And Application GET response matches updated IRP record

Get updated UL VIPS record
    [Tags]  UL  GET application
    [Documentation]  Retrieves the updated application information.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/c7aa2b33-f531-4aaa-e054-00144ffbc109/application/2501``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"applicationInfo":{"prohibitionNoticeNo":"21900308","noticeTypeCd":"UL","reviewApplnTypeCd":"UL","noticeSubjectCd":"PERS","presentationTypeCd":"WRIT","reviewRoleTypeCd":"AUTHPERS","firstGivenNm":"Harold","secondGivenNm":"H.","surnameNm":"Headpayne","phoneNo":"2222222222","faxNo":"1111111111","email":"user@gov.bc.ca","manualEntryYN":"N","formData":"PD94="}}} ``
    Given GET application       ${UL_APPLICATION_GUID}  ${UL_REC_CORRELATION_ID}
    Then response code is       200
    And Response body contains  "resp":"success"
    And Application GET response matches updated UL record

Query application status for ADP after submission
    [Tags]           ADP  GET status
    [Documentation]  Retrieves the prohibition status after updates were made.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/21900104/status/123123``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"status":{"noticeTypeCd":"ADP","noticeServedDt":"2020-08-15 00:00:00 -08:00","reviewFormSubmittedYn":"Y","reviewCreatedYn":"N","originalCause":"ADP09412","surnameNm":"Gordon","driverLicenceSeizedYn":"Y","disclosure":[],"reviews":[{},{"applicationId":"c7aa2b33-f52f-4aaa-e054-00144ffbc109"}]}}} ``
    Given Query status for application  ${ADP_REC_PROHIBITION_NUM}  123123
    Then response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "reviewCreatedYn":"N"
    And Response body contains  "originalCause":"ADP09412"
    And Response body contains  "reviews":[{"applicationId":"${ADP_APPLICATION_GUID}"}]
    And Query response matches ADP record
 
Query application status for IRP after submission
    [Tags]           IRP  GET status
    [Documentation]  Retrieves the prohibition status after updates were made.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/21900051/status/123124 ``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"status":{"noticeTypeCd":"IRP","noticeServedDt":"2020-08-15 00:00:00 -08:00","reviewFormSubmittedYn":"Y","reviewCreatedYn":"N","originalCause":"IRP90FAIL","surnameNm":"Gordon","driverLicenceSeizedYn":"N","disclosure":[],"reviews":[{},{"applicationId":"c7aa2b33-f530-4aaa-e054-00144ffbc109"}]}}} ``
    Given Query status for application  ${IRP_REC_PROHIBITION_NUM}  123124
    Then response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "reviewCreatedYn":"N"
    And Response body contains  "originalCause":"IRP90FAIL"
    And Response body contains  "reviews":[{"applicationId":"${IRP_APPLICATION_GUID}"}]
    And Query response matches IRP record

Query application status for UL after submission
    [Tags]           UL  GET status
    [Documentation]  Retrieves the prohibition status after updates were made.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/21900308/status/123125 ``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"status":{"noticeTypeCd":"UL","noticeServedDt":"2020-08-15 00:00:00 -08:00","reviewFormSubmittedYn":"Y","reviewCreatedYn":"N","originalCause":"IRPINDEF","surnameNm":"Gordon","driverLicenceSeizedYn":"N","disclosure":[],"reviews":[{},{"applicationId":"c7aa2b33-f531-4aaa-e054-00144ffbc109"}]}}} ``
    Given Query status for application  ${UL_REC_PROHIBITION_NUM}  123125
    Then response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "reviewCreatedYn":"N"
    And Response body contains  "originalCause":"IRPINDEF"
    And Response body contains  "reviews":[{"applicationId":"${UL_APPLICATION_GUID}"}]
    And Query response matches UL record

Get disclosure for ADP
    [Tags]           ADP  GET disclosure
    [Documentation]  Retrieve base64-encoded PDF disclosure document.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/15/disclosure/12445``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"document":{"mimeType":"application/pdf","document":"..."}}}``
    Given Get disclosure document  ${ADP_REC_DOCUMENT_ID}  12445
    Then Response code is  200
    And Disclosure document should be a PDF file

Get disclosure for IRP
    [Tags]           IRP  GET disclosure
    [Documentation]  Retrieve base64-encoded PDF disclosure document.
    ...  \n\nExample request from API 1.1.0:\n\n ``http://dfapi.svc/digitalforms/19/disclosure/12446``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"document":{"mimeType":"application/pdf","document":"..."}}}``
    Given Get disclosure document  ${IRP_REC_DOCUMENT_ID}  12446
    Then Response code is          200
    And Disclosure document should be a PDF file

Get disclosure for UL
    [Tags]           UL  GET disclosure
    [Documentation]  Retrieve base64-encoded PDF disclosure document.
    ...  \n\nExample request from API 1.1.0:\n\n ``http://dfapi.svc/digitalforms/20/disclosure/12447``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"document":{"mimeType":"application/pdf","document":"..."}}}``
    Given Get disclosure document  ${UL_REC_DOCUMENT_ID}  12447
    Then Response code is          200
    And Disclosure document should be a PDF file

Set disclosure sent for ADP
    [Tags]           ADP  PATCH disclosure
    [Documentation]  Confirm that the disclosure documents have been sent to the applicant.
    ...  \n\nExample request from API 1.1.0:\n\n ``PATCH http://dfapi.svc/digitalforms/disclosure/14566``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":true}``
    Given PATCH disclosure status as sent  ${ADP_DISCLOSURE_PAYLOAD}  14566
    Then Response code is                  200
    And Response body contains             "resp":"success"

Set disclosure sent for IRP
    [Tags]           IRP  PATCH disclosure
    [Documentation]  Confirm that the disclosure documents have been sent to the applicant.
    ...  \n\nExample request from API 1.1.0:\n\n ``PATCH http://dfapi.svc/digitalforms/disclosure/14567 ``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":true}``
    Given PATCH disclosure status as sent  ${IRP_DISCLOSURE_PAYLOAD}  14567
    Then Response code is                  200
    And Response body contains             "resp":"success"

Set disclosure sent for UL
    [Tags]           UL  PATCH disclosure
    [Documentation]  Confirm that the disclosure documents have been sent to the applicant.
    ...  \n\nExample request from API 1.1.0:\n\n ``PATCH http://dfapi.svc/digitalforms/disclosure/14568 ``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":true} ``
    Given PATCH disclosure status as sent  ${UL_DISCLOSURE_PAYLOAD}  14568
    Then Response code is                  200
    And Response body contains             "resp":"success"

Confirm disclosure date is set for ADP
    [Tags]           ADP 
    [Documentation]  After setting disclosure, the status should show a date in the "disclosure" element.
    Given Query status for application  ${ADP_REC_PROHIBITION_NUM}  14569
    Then response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "disclosure":[{"documentId":"
    And Response body contains  "disclosedDtm":"20

Confirm disclosure date is set for IRP
    [Tags]           IRP 
    [Documentation]  After setting disclosure, the status should show a date in the "disclosure" element.
    Given Query status for application  ${IRP_REC_PROHIBITION_NUM}  14570
    Then response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "disclosure":[{"documentId":"
    And Response body contains  "disclosedDtm":"20

Confirm disclosure date is set for UL
    [Tags]           UL 
    [Documentation]  After setting disclosure, the status should show a date in the "disclosure" element.
    Given Query status for application  ${UL_REC_PROHIBITION_NUM}  14571
    Then response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "disclosure":[{"documentId":"
    And Response body contains  "disclosedDtm":"20

Get payment payment status for ADP
    [Tags]           ADP  GET payment
    [Documentation]  Retrieve payment information for an application.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/c7aa2b33-f52f-4aaa-e054-00144ffbc109/payment/status/``\n\n33445
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"transactionInfo":{}}}``
    Given GET payment information  ${ADP_APPLICATION_GUID}  33445
    Then Response code is          200
    And Response body contains     {"resp":"success","data":{"transactionInfo":{}}}

Get payment payment status for IRP
    [Tags]           IRP  GET payment
    [Documentation]  Retrieve payment information for an application.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/c7aa2b33-f530-4aaa-e054-00144ffbc109/payment/status/``\n\n33446
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"transactionInfo":{}}} ``
    Given GET payment information  ${IRP_APPLICATION_GUID}  33446
    Then Response code is          200
    And Response body contains     {"resp":"success","data":{"transactionInfo":{}}}

Get payment payment status for UL
    [Tags]           UL  GET payment
    [Documentation]  Retrieve payment information for an application.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET /digitalforms/c7aa2b33-f531-4aaa-e054-00144ffbc109/payment/status/33447``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"transactionInfo":{}}} ``
    Given GET payment information  ${UL_APPLICATION_GUID}  33447
    Then Response code is          200
    And Response body contains     {"resp":"success","data":{"transactionInfo":{}}}

PATCH payments for 1.0 API endpoint no longer function
    [Tags]  1.0  GET payment
    [Documentation]  The payment PATCH endpoint used the prohibition number for payments. That should no longer work.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET /digitalforms/21900104/payment/status/33447``\n\n
    ...  Example response from API 1.1.0:\n\n ``?``
    Given PATCH Payment         ${ADP_REC_PROHIBITION_NUM}  ${ADP_PAYMENT_AMOUNT}  ${ADP_PAYMENT_DATE}  ${ADP_PAYMENT_CARD}  ${ADP_PAYMENT_RECEIPT}  11766
    Then Response code is       500
    And Response body contains  "resp":"fail"

Make payment for ADP
    [Tags]           ADP  PATCH payment
    [Documentation]  Make a payment for an application.
    ...  \n\nExample request from API 1.1.0:\n\n ``PATCH http://dfapi.svc/digitalforms/c7aa2b33-f52f-4aaa-e054-00144ffbc109/payment/11776``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":true} ``
    Given PATCH Payment  ${ADP_APPLICATION_GUID}  ${ADP_PAYMENT_AMOUNT}  ${ADP_PAYMENT_DATE}  ${ADP_PAYMENT_CARD}  ${ADP_PAYMENT_RECEIPT}  11776
    Then Response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "data":true

Make payment for IRP
    [Tags]           IRP  PATCH payment
    [Documentation]  Make a payment for an application.
    ...  \n\nExample request from API 1.1.0:\n\n ``PATCH http://dfapi.svc/digitalforms/c7aa2b33-f530-4aaa-e054-00144ffbc109/payment/11777``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":true} ``
    Given PATCH Payment  ${IRP_APPLICATION_GUID}  ${IRP_PAYMENT_AMOUNT}  ${IRP_PAYMENT_DATE}  ${IRP_PAYMENT_CARD}  ${IRP_PAYMENT_RECEIPT}  11777
    Then Response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "data":true

Make payment for UL
    [Tags]           UL  PATCH payment
    [Documentation]  Make a payment for an application.
    ...  \n\nExample request from API 1.1.0:\n\n ``PATCH http://dfapi.svc/digitalforms/c7aa2b33-f531-4aaa-e054-00144ffbc109/payment/11777``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":true} ``
    Given PATCH Payment  ${UL_APPLICATION_GUID}  ${UL_PAYMENT_AMOUNT}  ${UL_PAYMENT_DATE}  ${UL_PAYMENT_CARD}  ${UL_PAYMENT_RECEIPT}  11777
    Then Response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "data":true

ADP payments are shown correctly by payment API
    [Tags]           ADP  GET payment
    [Documentation]  Retrieve payment information for an application. The payment just made should be shown in the response body.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/c7aa2b33-f52f-4aaa-e054-00144ffbc109/payment/status/``\n\n33447
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"transactionInfo":{"paymentCardType":"VISA","paymentAmount":"200.00","receiptNumberTxt":"92626582","paymentDate":"2021-07-20 09:00:00 -08:00"}}} ``
    Given GET payment information  ${ADP_APPLICATION_GUID}  33447
    Then Response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "paymentCardType":"${ADP_PAYMENT_CARD}"
    And Response body contains  "paymentAmount":"${ADP_PAYMENT_AMOUNT}"
    And Response body contains  "receiptNumberTxt":"${ADP_PAYMENT_RECEIPT}"
    And Response body contains  "paymentDate":"${ADP_PAYMENT_DATE}"

IRP payments are shown correctly by payment API
    [Tags]           IRP  GET payment
    [Documentation]  Retrieve payment information for an application. The payment just made should be shown in the response body.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/c7aa2b33-f530-4aaa-e054-00144ffbc109/payment/status/``\n\n33448
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"transactionInfo":{"paymentCardType":"VISA","paymentAmount":"200.00","receiptNumberTxt":"95363881","paymentDate":"2021-07-20 09:00:00 -08:00"}}}``
    Given GET payment information  ${IRP_APPLICATION_GUID}  33448
    Then Response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "paymentCardType":"${IRP_PAYMENT_CARD}"
    And Response body contains  "paymentAmount":"${IRP_PAYMENT_AMOUNT}"
    And Response body contains  "receiptNumberTxt":"${IRP_PAYMENT_RECEIPT}"
    And Response body contains  "paymentDate":"${IRP_PAYMENT_DATE}"

UL payments are shown correctly by payment API
    [Tags]           UL  GET payment
    [Documentation]  Retrieve payment information for an application. The payment just made should be shown in the response body.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/c7aa2b33-f531-4aaa-e054-00144ffbc109/payment/status/``\n\n33449
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"transactionInfo":{"paymentCardType":"VISA","paymentAmount":"200.00","receiptNumberTxt":"97705975","paymentDate":"2021-07-20 09:00:00 -08:00"}}}``
    Given GET payment information  ${UL_APPLICATION_GUID}  33449
    Then Response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "paymentCardType":"${UL_PAYMENT_CARD}"
    And Response body contains  "paymentAmount":"${UL_PAYMENT_AMOUNT}"
    And Response body contains  "receiptNumberTxt":"${UL_PAYMENT_RECEIPT}"
    And Response body contains  "paymentDate":"${UL_PAYMENT_DATE}"

Application query for ADP after payment shows receipt number
    [Tags]           ADP  GET status
    [Documentation]  Retrieve prohibition information. It should now show the payment receipt number in the "reviews" JSON element.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/21900104/status/123123``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"status":{"noticeTypeCd":"ADP","noticeServedDt":"2020-08-15 00:00:00 -08:00","reviewFormSubmittedYn":"Y","reviewCreatedYn":"N","originalCause":"ADP09412","surnameNm":"Gordon","driverLicenceSeizedYn":"Y","disclosure":[],"reviews":[{},{"applicationId":"c7aa2b33-f52f-4aaa-e054-00144ffbc109","receiptNumberTxt":"92626582"}]}}}``
    Given Query status for application  ${ADP_REC_PROHIBITION_NUM}  123123
    Then response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "reviewCreatedYn":"N"
    And Response body contains  "originalCause":"ADP09412"
    #And Response body contains  "applicationId":"${ADP_APPLICATION_GUID}"
    #And Response body contains  "receiptNumberTxt":"${ADP_PAYMENT_RECEIPT}"
    And Response body contains  "reviews":[{"applicationId":"${ADP_APPLICATION_GUID}","receiptNumberTxt":"${ADP_PAYMENT_RECEIPT}"}]
    And Response body does not contain  "status":"unknown"

Application query for IRP after payment shows receipt number
    [Tags]           IRP  GET status
    [Documentation]  Retrieve prohibition information. It should now show the payment receipt number in the "reviews" JSON element.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/21900051/status/123123``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"status":{"noticeTypeCd":"IRP","noticeServedDt":"2020-08-15 00:00:00 -08:00","reviewFormSubmittedYn":"Y","reviewCreatedYn":"N","originalCause":"IRP90FAIL","surnameNm":"Gordon","driverLicenceSeizedYn":"N","disclosure":[],"reviews":[{},{"applicationId":"c7aa2b33-f530-4aaa-e054-00144ffbc109","receiptNumberTxt":"95363881"}]}}} ``
    Given Query status for application  ${IRP_REC_PROHIBITION_NUM}  123123
    Then response code is  200
    And Response body contains  "resp":"success"
    And Response body contains  "reviewCreatedYn":"N"
    And Response body contains  "originalCause":"IRP90FAIL"
    #And Response body contains  "applicationId":"${IRP_APPLICATION_GUID}"
    #And Response body contains  "receiptNumberTxt":"${IRP_PAYMENT_RECEIPT}"
    And Response body contains  "reviews":[{"applicationId":"${IRP_APPLICATION_GUID}","receiptNumberTxt":"${IRP_PAYMENT_RECEIPT}"}]
    And Response body does not contain  "status":"unknown"

Application query for UL after payment shown receipt number
    [Tags]           UL  GET status
    [Documentation]  Retrieve prohibition information. It should now show the payment receipt number in the "reviews" JSON element.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/21900308/status/123123``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"status":{"noticeTypeCd":"UL","noticeServedDt":"2020-08-15 00:00:00 -08:00","reviewFormSubmittedYn":"Y","reviewCreatedYn":"N","originalCause":"IRPINDEF","surnameNm":"Gordon","driverLicenceSeizedYn":"N","disclosure":[],"reviews":[{},{"applicationId":"c7aa2b33-f531-4aaa-e054-00144ffbc109","receiptNumberTxt":"97705975"}]}}} ``
    Given Query status for application  ${UL_REC_PROHIBITION_NUM}  123123
    Then response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "reviewCreatedYn":"N"
    And Response body contains  "originalCause":"IRPINDEF"
    #And Response body contains  "applicationId":"${UL_APPLICATION_GUID}"
    #And Response body contains  "receiptNumberTxt":"${UL_PAYMENT_RECEIPT}"
    And Response body contains  "reviews":[{"applicationId":"${UL_APPLICATION_GUID}","receiptNumberTxt":"${UL_PAYMENT_RECEIPT}"}]
    And Response body does not contain  "status":"unknown"

Retrieve review schedule for ADP
    [Tags]           ADP  GET schedule
    [Documentation]  Request a list of review times for a date. There are usually fewer reviews for UL available than for ADP or IRP.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/ADP/ORAL/2021-08-03/review/availableTimeSlot/87677``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"timeSlots":[{"reviewStartDtm":"2021-08-03 09:00:00 -08:00","reviewEndDtm":"2021-08-03 09:30:00 -08:00"},{"reviewStartDtm":"2021-08-03 10:00:00 -08:00","reviewEndDtm":"2021-08-03 10:30:00 -08:00"},{"reviewStartDtm":"2021-08-03 11:00:00 -08:00","reviewEndDtm":"2021-08-03 11:30:00 -08:00"},{"reviewStartDtm":"2021-08-03 12:00:00 -08:00","reviewEndDtm":"2021-08-03 12:30:00 -08:00"},{"reviewStartDtm":"2021-08-03 13:00:00 -08:00","reviewEndDtm":"2021-08-03 13:30:00 -08:00"}]}} ``
    ...  Note: Reviews are only available on weekdays, so if you put in a date that falls on a weekend, you won't get any dates. National holidays are not accounted for in the DEV or TEST environments, but they are in PROD. So if you request a date that falls on a national holiday (e.g. 1st January) in DEV or TEST, you will get back an appointment time, even though it's not really valid.
    Given GET review schedule   ADP  ${ADP_REC_PRESENT_TYPE2}  ${REVIEW_FUTURE_DATE}  87677
    Then Response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "data":{"timeSlots":[{"reviewStartDtm":
    Set suite variable          ${ADP_REVIEW_START_TIME}  ${test_response.json()['data']['timeSlots'][0]['reviewStartDtm']}
    Set suite variable          ${ADP_REVIEW_STOP_TIME}  ${test_response.json()['data']['timeSlots'][0]['reviewEndDtm']}

Retrieve review schedule for IRP
    [Tags]           IRP  GET schedule
    [Documentation]  Request a list of review times for a date. There are usually fewer reviews for UL available than for ADP or IRP.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/IRP/ORAL/2021-08-03/review/availableTimeSlot/87678``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"timeSlots":[{"reviewStartDtm":"2021-08-03 09:00:00 -08:00","reviewEndDtm":"2021-08-03 09:30:00 -08:00"},{"reviewStartDtm":"2021-08-03 10:00:00 -08:00","reviewEndDtm":"2021-08-03 10:30:00 -08:00"},{"reviewStartDtm":"2021-08-03 11:00:00 -08:00","reviewEndDtm":"2021-08-03 11:30:00 -08:00"},{"reviewStartDtm":"2021-08-03 12:00:00 -08:00","reviewEndDtm":"2021-08-03 12:30:00 -08:00"},{"reviewStartDtm":"2021-08-03 13:00:00 -08:00","reviewEndDtm":"2021-08-03 13:30:00 -08:00"}]}} ...  Note: Reviews are only available on weekdays, so if you put in a date that falls on a weekend, you won't get any dates. National holidays are not accounted for in the DEV or TEST environments, but they are in PROD. So if you request a date that falls on a national holiday (e.g. 1st January) in DEV or TEST, you will get back an appointment time, even though it's not really valid.``
    Given GET review schedule   IRP  ${IRP_REC_PRESENT_TYPE2}  ${REVIEW_FUTURE_DATE}  87678
    Then Response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "data":{"timeSlots":[{"reviewStartDtm":
    Set suite variable          ${IRP_REVIEW_START_TIME}  ${test_response.json()['data']['timeSlots'][0]['reviewStartDtm']}
    Set suite variable          ${IRP_REVIEW_STOP_TIME}  ${test_response.json()['data']['timeSlots'][0]['reviewEndDtm']}

Retrieve review schedule for UL
    [Tags]           UL  GET schedule
    [Documentation]  Request a list of review times for a date. There are usually fewer reviews for UL available than for ADP or IRP.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/UL/WRIT/2021-08-03/review/availableTimeSlot/87679 ``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"timeSlots":[{"reviewStartDtm":"2021-08-03 09:30:00 -08:00","reviewEndDtm":"2021-08-03 10:00:00 -08:00"}]}} ``
    ...  Note: Reviews are only available on weekdays, so if you put in a date that falls on a weekend, you won't get any dates. National holidays are not accounted for in the DEV or TEST environments, but they are in PROD. So if you request a date that falls on a national holiday (e.g. 1st January) in DEV or TEST, you will get back an appointment time, even though it's not really valid.
    Given GET review schedule   UL  ${UL_REC_PRESENT_TYPE2}  ${REVIEW_FUTURE_DATE}  87679
    Then Response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "data":{"timeSlots":[{"reviewStartDtm":
    Set suite variable          ${UL_REVIEW_START_TIME}  ${test_response.json()['data']['timeSlots'][0]['reviewStartDtm']}
    Set suite variable          ${UL_REVIEW_STOP_TIME}  ${test_response.json()['data']['timeSlots'][0]['reviewEndDtm']}

Book review time for ADP
    [Tags]           ADP  POST schedule
    [Documentation]  Reserve a review time for an application review. The payload will return a reviewId number.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/c7aa2b33-f52f-4aaa-e054-00144ffbc109/review/schedule/``\n\na98788
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"reviewInfo":{"reviewId":"2697","reviewStartDtm":"2021-08-03 09:00:00 -08:00","reviewEndDtm":"2021-08-03 09:30:00 -08:00"}}} ``
    Given POST review time      ${ADP_APPLICATION_GUID}  ${ADP_REVIEW_START_TIME}  ${ADP_REVIEW_STOP_TIME}  a98788
    Then Response code is       200
    And Response body contains  "resp":"success"
    Set suite variable          ${ADP_REVIEW_ID}  ${test_response.json()['data']['reviewInfo']['reviewId']}

Book review time for IRP
    [Tags]           IRP  POST schedule
    [Documentation]  Reserve a review time for an application review. The payload will return a reviewId number.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/c7aa2b33-f530-4aaa-e054-00144ffbc109/review/schedule/``\n\na98788
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"reviewInfo":{"reviewId":"2698","reviewStartDtm":"2021-08-03 09:00:00 -08:00","reviewEndDtm":"2021-08-03 09:30:00 -08:00"}}} ``
    Given POST review time      ${IRP_APPLICATION_GUID}  ${IRP_REVIEW_START_TIME}  ${IRP_REVIEW_STOP_TIME}  a98788
    Then Response code is       200
    And Response body contains  "resp":"success"
    Set suite variable          ${IRP_REVIEW_ID}  ${test_response.json()['data']['reviewInfo']['reviewId']}

Book review time for UL
    [Tags]           UL  POST schedule
    [Documentation]  Reserve a review time for an application review. The payload will return a reviewId number.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/c7aa2b33-f531-4aaa-e054-00144ffbc109/review/schedule/``\n\na98788
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"reviewInfo":{"reviewId":"2699","reviewStartDtm":"2021-08-03 09:30:00 -08:00","reviewEndDtm":"2021-08-03 10:00:00 -08:00"}}} ``
    Given POST review time      ${UL_APPLICATION_GUID}  ${UL_REVIEW_START_TIME}  ${UL_REVIEW_STOP_TIME}  a98788
    Then Response code is       200
    And Response body contains  "resp":"success"
    Set suite variable          ${UL_REVIEW_ID}  ${test_response.json()['data']['reviewInfo']['reviewId']}

Application query for ADP after booking review shown as in_progress
    [Tags]           ADP  GET status
    [Documentation]  Retrieve prohibition status, and you should be able to see the payment, review start and end times, review id, receipt number, status, and reviewCreated.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/21900104/status/123123``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"status":{"noticeTypeCd":"ADP","noticeServedDt":"2020-08-15 00:00:00 -08:00","reviewFormSubmittedYn":"Y","reviewCreatedYn":"Y","originalCause":"ADP09412","surnameNm":"Gordon","driverLicenceSeizedYn":"Y","disclosure":[],"reviews":[{"applicationId":"c7aa2b33-f52f-4aaa-e054-00144ffbc109","status":"in_progress","reviewStartDtm":"2021-08-03 09:00:00 -08:00","reviewEndDtm":"2021-08-03 09:30:00 -08:00","receiptNumberTxt":"92626582","reviewId":"2697"}]}}} ``
    Given Query status for application  ${ADP_REC_PROHIBITION_NUM}  123123
    Then response code is               200
    And Response body contains          "resp":"success"
    And Response body contains          "status":"in_progress"
    And Response body contains          "reviews":[{"applicationId":"${ADP_APPLICATION_GUID}"
    And Response body contains          "reviewStartDtm":"${ADP_REVIEW_START_TIME}"
    And Response body contains          "reviewEndDtm":"${ADP_REVIEW_STOP_TIME}"
    And Response body contains          "reviewCreatedYn":"Y"
    And Response body contains          "originalCause":"ADP09412"    
    And Response body contains          "reviewId":"${ADP_REVIEW_ID}"
    And Response body contains          "receiptNumberTxt":"${ADP_PAYMENT_RECEIPT}"
 
Application query for IRP after booking review shown as in_progress
    [Tags]           IRP  GET status
    [Documentation]  Retrieve prohibition status, and you should be able to see the payment, review start and end times, review id, receipt number, status, and reviewCreated.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/21900051/status/123124``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"status":{"noticeTypeCd":"IRP","noticeServedDt":"2020-08-15 00:00:00 -08:00","reviewFormSubmittedYn":"Y","reviewCreatedYn":"Y","originalCause":"IRP90FAIL","surnameNm":"Gordon","driverLicenceSeizedYn":"N","disclosure":[],"reviews":[{"applicationId":"c7aa2b33-f530-4aaa-e054-00144ffbc109","status":"in_progress","reviewStartDtm":"2021-08-03 09:00:00 -08:00","reviewEndDtm":"2021-08-03 09:30:00 -08:00","receiptNumberTxt":"95363881","reviewId":"2698"}]}}}``
    Given Query status for application  ${IRP_REC_PROHIBITION_NUM}  123124
    Then response code is               200
    And Response body contains          "resp":"success"
    And Response body contains          "status":"in_progress"
    And Response body contains          "reviews":[{"applicationId":"${IRP_APPLICATION_GUID}"
    And Response body contains          "reviewStartDtm":"${IRP_REVIEW_START_TIME}"
    And Response body contains          "reviewEndDtm":"${IRP_REVIEW_STOP_TIME}"
    And Response body contains          "reviewCreatedYn":"Y"
    And Response body contains          "originalCause":"IRP90FAIL"
    And Response body contains          "reviewId":"${IRP_REVIEW_ID}"
    And Response body contains          "receiptNumberTxt":"${IRP_PAYMENT_RECEIPT}"

Application query for UL after booking review shown as in_progress
    [Tags]           UL  GET status
    [Documentation]  Retrieve prohibition status, and you should be able to see the payment, review start and end times, review id, receipt number, status, and reviewCreated.
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/21900308/status/123125``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"success","data":{"status":{"noticeTypeCd":"UL","noticeServedDt":"2020-08-15 00:00:00 -08:00","reviewFormSubmittedYn":"Y","reviewCreatedYn":"Y","originalCause":"IRPINDEF","surnameNm":"Gordon","driverLicenceSeizedYn":"N","disclosure":[],"reviews":[{"applicationId":"c7aa2b33-f531-4aaa-e054-00144ffbc109","status":"in_progress","reviewStartDtm":"2021-08-03 09:30:00 -08:00","reviewEndDtm":"2021-08-03 10:00:00 -08:00","receiptNumberTxt":"97705975","reviewId":"2699"}]}}} ``
    Given Query status for application  ${UL_REC_PROHIBITION_NUM}  123125
    Then response code is               200
    And Response body contains          "resp":"success"
    And Response body contains          "status":"in_progress"
    And Response body contains          "reviews":[{"applicationId":"${UL_APPLICATION_GUID}"
    And Response body contains          "reviewStartDtm":"${UL_REVIEW_START_TIME}"
    And Response body contains          "reviewEndDtm":"${UL_REVIEW_STOP_TIME}"
    And Response body contains          "reviewCreatedYn":"Y"
    And Response body contains          "originalCause":"IRPINDEF"
    And Response body contains          "reviewId":"${UL_REVIEW_ID}"
    And Response body contains          "receiptNumberTxt":"${UL_PAYMENT_RECEIPT}"

A second VIPS ADP application fails when status is in_progress
    [Tags]           ADP  POST application
    [Documentation]  Submit a second application while the first is in the in_progress state. This call should fail. New applications can only be submitted for UL prohibitions where no application state is "in_progress" or "successful". In other words, you can only create second reviews for UL applications where applications are in these states: "unknown", "cancelled", "unsuccesful".
    ...  \n\nExample request from API 1.1.0:\n\n ``POST http://dfapi.svc/digitalforms/ADP/21900104/application/2301``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"fail","error":{"message":"Request cannot be processed","httpStatus":400}}``
    Given POST new application  ADP  ${ADP_REC_PROHIBITION_NUM}  ${ADP_REC_CORRELATION_ID}  ${ADP_REC_JSON}
    Then Response code is       400
    And Response body contains  "resp":"fail"

A second VIPS IRP application fails when status is in_progress
    [Tags]            IRP  POST application
    [Documentation]  Submit a second application while the first is in the in_progress state. This call should fail. New applications can only be submitted for UL prohibitions where no application state is "in_progress" or "successful". In other words, you can only create second reviews for UL applications where applications are in these states: "unknown", "cancelled", "unsuccesful".
    ...  \n\nExample request from API 1.1.0:\n\n ``POST http://dfapi.svc/digitalforms/IRP/21900051/application/2401``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"fail","error":{"message":"Request cannot be processed","httpStatus":400}}``
    Given POST new application  IRP  ${IRP_REC_PROHIBITION_NUM}  ${IRP_REC_CORRELATION_ID}  ${IRP_REC_JSON}
    Then Response code is       400
    And Response body contains  "resp":"fail"

A second VIPS UL application fails when status is in_progress
    [Tags]           UL  POST application
    [Documentation]  Submit a second application while the first is in the in_progress state. This call should fail. New applications can only be submitted for UL prohibitions where no application state is "in_progress" or "successful". In other words, you can only create second reviews for UL applications where applications are in these states: "unknown", "cancelled", "unsuccessful".
    ...  \n\nExample request from API 1.1.0:\n\n ``POST http://dfapi.svc/digitalforms/UL/21900308/application/2501``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"fail","error":{"message":"Request cannot be processed","httpStatus":400}}``
    Given POST new application  UL  ${UL_REC_PROHIBITION_NUM}  ${UL_REC_CORRELATION_ID}  ${UL_REC_JSON}
    Then Response code is       400
    And Response body contains  "resp":"fail"

# ==================================================================================================
# ==================================================================================================
# ==================================================================================================
# ==================================================================================================
# ==================================================================================================
# ==================================================================================================

Transition application state from in_progress to completed
    [Tags]           PLACEHOLDER
    [Documentation]  **PLACEHOLDER.** WE'RE WAITING FOR A WAY TO CHANGE THE APPLICATION STATE TO "COMPLETED".
    ...  \n\nExample request from API 1.1.0:\n\n ``?``\n\n
    ...  Example response from API 1.1.0:\n\n ``?``
    Log  Here we find a way to transition the application state from in_complete to completed.
    Should be equal as strings  Not yet  integrated

A second VIPS ADP application fails when status is in_progress
    [Tags]           ADP 2ADP
    [Documentation]  Attempt to create a second ADP application. This should fail. Only UL prohibitions can have more than one application.
    ...  \n\nExample request from API 1.1.0:\n\n ``POST http://dfapi.svc/digitalforms/ADP/21900104/application/2301``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"fail","error":{"message":"Request cannot be processed","httpStatus":400}}``
    Given POST new application  ADP  ${ADP_REC_PROHIBITION_NUM}  ${ADP_REC_CORRELATION_ID}  ${ADP_REC_JSON}
    Then Response code is       400
    And Response body contains  "resp":"fail"

A second VIPS IRP application fails when status is completed
    [Tags]           IRP 2IRP
    [Documentation]  Attempt to create a second ADP application. This should fail. Only UL prohibitions can have more than one application.
    ...  \n\nExample request from API 1.1.0:\n\n ``POST http://dfapi.svc/digitalforms/IRP/21900051/application/2401``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"fail","error":{"message":"Request cannot be processed","httpStatus":400}}``
    Given POST new application  IRP  ${IRP_REC_PROHIBITION_NUM}  ${IRP_REC_CORRELATION_ID}  ${IRP_REC_JSON}
    Then Response code is       400
    And Response body contains  "resp":"fail"

A second VIPS UL application succeeds when status is completed
    [Tags]  UL 2UL
    [Documentation]  
    ...  \n\nExample request from API 1.1.0:\n\n ``POST http://dfapi.svc/digitalforms/IRP/21900051/application/2401``\n\n
    ...  Example response from API 1.1.0:\n\n ``?``
    Given POST new application  UL  ${UL_REC_PROHIBITION_NUM}  ${UL_REC_CORRELATION_ID}  ${UL_REC_JSON}
    Then Response code is       201
    And Response body contains  "resp":"success"
    And response body contains  applicationId
    And response body contains  createdTime
    And There are two reviews found
    # TODO: ensure GUId is captured correctly
    And set suite variable      ${UL_SECOND_APPLICATION_RESPONSE}  ${test_response.json()}
    And set suite variable      ${UL_SECOND_APPLICATION_GUID}  ${test_response.json()['data']['applicationInfo']['applicationId']}
    # TODO: Ensure that there are two reviews, and first review is in the second element.

A third VIPS UL application fails when status is in_progress
    [Tags]  UL
    [Documentation]  
    ...  \n\nExample request from API 1.1.0:\n\n ``http://dfapi.svc/digitalforms/UL/21900308/application/2501``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"resp":"fail","error":{"message":"Request cannot be processed","httpStatus":400}}``
    Given POST new application  UL  ${UL_REC_PROHIBITION_NUM}  ${UL_REC_CORRELATION_ID}  ${UL_REC_JSON}
    Then Response code is       400
    And Response body contains  "resp":"fail"

Query the second application status for UL after submission
    [Tags]  UL 2UL
    [Documentation]  
    ...  \n\nExample request from API 1.1.0:\n\n ``GET http://dfapi.svc/digitalforms/UL/21900308/application/2501``\n\n
    ...  Example response from API 1.1.0:\n\n ``?``
    Given Query status for application  ${UL_REC_PROHIBITION_NUM}  123125
    Then response code is  200
    And Response body contains  "resp":"success"
    And Response body contains  "reviewCreatedYn":"Y"
    And Response body contains  "originalCause":"IRPINDEF"
    And Response body contains  "reviews":[{{"applicationId":"${UL_SECOND_APPLICATION_GUID}},{"applicationId":"${UL_APPLICATION_GUID},"
    And Query response matches UL record

Patch second submitted UL application fields
    [Tags]  UL 2UL
    [Documentation]  
    ...  \n\nExample request from API 1.1.0:\n\n ``PATCH http://dfapi.svc/digitalforms/UL/c7ccd308-88ea-5760-e054-00144ffbc109/application/2345``\n\n
    ...  Example response from API 1.1.0:\n\n ``{"applicationInfo":{"applicationId":"c7ccd308-88ea-5760-e054-00144ffbc109","updatedTime":"2021-07-23 10:19:07 -08:00"}}}``
    Given PATCH application  UL  ${UL_SECOND_APPLICATION_GUID}  2345  ${UL_REC_JSON_UPDATED}
    Then response code is    200
    And Response body contains  "resp":"success"
    And Response body contains  {"applicationInfo":{"applicationId":"${UL_SECOND_APPLICATION_GUID}"

Application query should show updated second application after patch
    [Tags]  UL 2UL
    [Documentation]  
    ...  \n\nExample request from API 1.1.0:\n\n ``http://dfapi.svc/digitalforms/21900308/status/123125``\n\n
    ...  Example response from API 1.1.0:\n\n ``?``
    Given Query status for application  ${UL_REC_PROHIBITION_NUM}  123125
    Then response code is  200
    And Response body contains  "resp":"success"
    And Response body contains  "reviewCreatedYn":"N"
    And Response body contains  "originalCause":"IRPINDEF"
    And Response body contains  "reviews":[{{"applicationId":"${UL_SECOND_APPLICATION_GUID}},{"applicationId":"${UL_APPLICATION_GUID},"
    And Query response matches UL record

Get payment payment status for UL second application
    [Tags]  UL 2UL
    [Documentation]  
    ...  \n\nExample request from API 1.1.0:\n\n ````\n\n
    ...  Example response from API 1.1.0:\n\n ``?``
    Given GET payment information  ${UL_SECOND_APPLICATION_GUID}  33447
    Then Response code is  200
    And Response body contains  {"resp":"success","data":{"transactionInfo":{}}}

Make payment for second UL application
    [Tags]  UL 2UL
    [Documentation]  
    ...  \n\nExample request from API 1.1.0:\n\n ````\n\n
    ...  Example response from API 1.1.0:\n\n ``?``
    Given PATCH Payment  ${UL_SECOND_APPLICATION_GUID}  ${UL_PAYMENT_AMOUNT}  ${UL_PAYMENT_DATE}  ${UL_PAYMENT_CARD}  ${UL_SECOND_PAYMENT_RECEIPT}  11777
    Then Response code is  200
    And Response body contains  {"resp":"success","data":true} 

Payments for second UL application is shown correctly by payment API
    [Tags]  UL 2UL
    [Documentation]  
    ...  \n\nExample request from API 1.1.0:\n\n ````\n\n
    ...  Example response from API 1.1.0:\n\n ``?``
    Given GET payment information  ${UL_APPLICATION_GUID}  33449
    Then Response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "paymentCardType":"${UL_PAYMENT_CARD}"
    And Response body contains  "paymentAmount":"${UL_PAYMENT_AMOUNT}"
    And Response body contains  "receiptNumberTxt":"${UL_PAYMENT_RECEIPT}"
    And Response body contains  "paymentDate":"${UL_PAYMENT_DATE}"

Application query for second UL application after payment shown receipt number
    [Tags]  UL 2UL
    [Documentation]  
    ...  \n\nExample request from API 1.1.0:\n\n ````\n\n
    ...  Example response from API 1.1.0:\n\n ``?``
    Given Query status for application  ${UL_REC_PROHIBITION_NUM}  123123
    Then response code is  200
    And Response body contains  "resp":"success"
    And Response body contains  "reviewCreatedYn":"N"
    And Response body contains  "originalCause":"IRPINDEF"
    And Response body contains  "reviews":[{"applicationId":"${UL_SECOND_APPLICATION_GUID},"receiptNumberTxt":"${UL_SECOND_PAYMENT_RECEIPT}"},{"applicationId":"${UL__APPLICATION_GUID}"
    And Response body does not contain  "status":"unknown"

Retrieve review schedule for second UL
    [Tags]  UL 2UL
    [Documentation]  
    ...  \n\nExample request from API 1.1.0:\n\n ````\n\n
    ...  Example response from API 1.1.0:\n\n ``?``
    Given GET review schedule  UL  ${UL_REC_PRESENT_TYPE2}  ${REVIEW_FUTURE_DATE}  87679
    Then Response code is       200
    And Response body contains  "resp":"success"
    And Response body contains  "data":{"timeSlots":[{"reviewStartDtm":
    Set suite variable  ${UL_REVIEW_START_TIME}  ${test_response.json()['data']['timeSlots'][0]['reviewStartDtm']}
    Set suite variable  ${UL_REVIEW_STOP_TIME}  ${test_response.json()['data']['timeSlots'][0]['reviewEndDtm']}


Book review time for second UL
    [Tags]  UL 2UL
    [Documentation]  
    ...  \n\nExample request from API 1.1.0:\n\n ````\n\n
    ...  Example response from API 1.1.0:\n\n ``?``
    Given POST review time  ${UL_SECOND_APPLICATION_GUID}  ${UL_REVIEW_START_TIME}  ${UL_REVIEW_STOP_TIME}  a98788
    Then Response code is       200
    And Response body contains  "resp":"success"
    Set suite variable  ${UL_REVIEW_ID}  ${test_response.json()['data']['reviewInfo']['reviewId']}

Set disclosure sent for second UL
    [Tags]  UL 2UL
    [Documentation]  
    ...  \n\nExample request from API 1.1.0:\n\n ````\n\n
    ...  Example response from API 1.1.0:\n\n ``?``
    Given PATCH disclosure status as sent  ${UL_DISCLOSURE_PAYLOAD}  14568
    Then Response code is  200
    And Response body contains  "resp":"success"






Extract JSON value
    [Tags]  SAF
    # ${raw} =  Evaluate  ${SAF_JSON.json()}
    ${raw} =  Evaluate  json.loads($SAF_JSON)  json
    Log  ${raw['data']['applicationInfo']['applicationId']}

