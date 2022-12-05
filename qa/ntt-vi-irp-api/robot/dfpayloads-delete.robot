# Robot Framework

*** Settings ***
Documentation    DfPayloads POST endpoint
Library    JSONLibrary
Library      RequestsLibrary  # https://github.com/MarketSquare/robotframework-requests
Library      Collections      # Used to check header response from RequestsLibrary
Library      String           # https://robotframework.org/robotframework/latest/libraries/String.html
Library      Process          # https://robotframework.org/robotframework/latest/libraries/Process.html
Library      OperatingSystem  # https://robotframework.org/robotframework/latest/libraries/OperatingSystem.html
Library      DateTime         # https://robotframework.org/robotframework/latest/libraries/DateTime.html

# Settings for the DEV environment
#Variables   dev.Variables              # Environment settings

Resource   lib/kw-requests.resource     # Keywords for server requests
Resource   lib/kw-responses.resource    # Keywords for server responses

*** Variables ***
# See env.py
${CORRELATION} =    robot-prohibition-delete-01
${NOTICE_NUM} =     20100155

*** Keywords ***
# See lib/*.robot

*** Test Cases ***

#     _   _
#    | | | | __ _ _ __  _ __  _   _
#    | |_| |/ _` | '_ \| '_ \| | | |
#    |  _  | (_| | |_) | |_) | |_| |
#    |_| |_|\__,_| .__/| .__/ \__, |
#                |_|   |_|    |___/

DfPayloads DELETE authenticated
    [Tags]           dfpayloads    authenticated    DELETE    happy
    [Documentation]  Should delete a payload
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/dfpayloads/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PUT request to /v1/dfpayloads/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  200
    And Response body is  {"status_message":"Successful"}

DfPayloads OPTIONS authenticated
    [Tags]           dfpayloads    authenticated    OPTIONS    happy
    [Documentation]  Should show supported headers
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/dfpayloads/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated OPTIONS request to /v1/dfpayloads/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  200
    And Response body is empty
    And Response allow header should contain value GET,PUT,POST,DELETE,HEAD,OPTIONS

DfPayloads HEAD authenticated
    [Tags]           dfpayloads    authenticated    HEAD    happy
    [Documentation]  Should return headers, content
    ...
    ...              Example: ``$ https HEAD digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/dfpayloads/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated HEAD request to /v1/dfpayloads/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  200
    And Response body is empty
    And Response content type is  application/json
    And Response pragma header should contain value no-cache
    And Response cache-control header should contain value no-cache, no-store, max-age=0, must-revalidate
    And Response x-content-type-options header should contain value nosniff
    And Response x-frame-options header should contain value DENY
    And Response x-xss-protection header should contain value 1; mode=block


#     _   _       _
#    | | | |_ __ | |__   __ _ _ __  _ __  _   _
#    | | | | '_ \| '_ \ / _` | '_ \| '_ \| | | |
#    | |_| | | | | | | | (_| | |_) | |_) | |_| |
#     \___/|_| |_|_| |_|\__,_| .__/| .__/ \__, |
#                            |_|   |_|    |___/

DfPayloads GET not logged in
    [Tags]           dfpayloads  unauthenticated    GET    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/dfpayloads/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated GET request expecting HTTP 401 from /v1/dfpayloads/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}


DfPayloads OPTIONS not logged in
    [Tags]           dfpayloads    unauthenticated    OPTIONS    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/dfpayloads/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated OPTIONS request expecting HTTP 401 from /v1/dfpayloads/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

DfPayloads HEAD not logged in
    [Tags]           dfpayloads    unauthenticated    HEAD    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/dfpayloads/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated HEAD request expecting HTTP 401 from /v1/dfpayloads/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is empty

DfPayloads DELETE not logged in
    [Tags]           dfpayloads    unauthenticated    DELETE    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/dfpayloads/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated DELETE request expecting HTTP 401 from /v1/dfpayloads/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

DfPayloads PUT not logged in
    [Tags]           dfpayloads    unauthenticated    PUT    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PUT digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/dfpayloads/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated PUT request expecting HTTP 401 from /v1/dfpayloads/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

DfPayloads POST not logged in
    [Tags]           dfpayloads    unauthenticated    POST    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/dfpayloads/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated POST request expecting HTTP 401 from /v1/dfpayloads/${NOTICE_NUM}/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

DfPayloads PATCH authenticated
    [Tags]           dfpayloads    authenticated    PATCH    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/dfpayloads/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PATCH request expecting HTTP 500 from /v1/dfpayloads/${NOTICE_NUM}/${CORRELATION} with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PATCH' not supported"}

DfPayloads PATCH not logged in
    [Tags]           dfpayloads    unauthenticated    PATCH    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/dfpayloads/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated PATCH request expecting HTTP 401 from /v1/dfpayloads/${NOTICE_NUM}/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}