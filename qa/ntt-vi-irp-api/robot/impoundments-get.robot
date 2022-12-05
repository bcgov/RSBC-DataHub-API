# Robot Framework

*** Settings ***
Documentation    Impoundments GET endpoint
Library      JSONLibrary
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
${CORRELATION} =    robot-prohibition-post-01
${NOTICE_NUM} =     22900838

*** Keywords ***
# See lib/*.robot

*** Test Cases ***

#     _   _
#    | | | | __ _ _ __  _ __  _   _
#    | |_| |/ _` | '_ \| '_ \| | | |
#    |  _  | (_| | |_) | |_) | |_| |
#    |_| |_|\__,_| .__/| .__/ \__, |
#                |_|   |_|    |___/

Impoundments GET authenticated succeeds
    [Tags]           impoundments  authenticated    GET    happy
    [Documentation]  Should return impoundment
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${NOTICE_NUM}/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request to /v1/impoundments/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response body contains  {"result":


Impoundments OPTIONS authenticated succeeds
    [Tags]           impoundments    authenticated    OPTIONS    happy
    [Documentation]  Should show supported headers
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated OPTIONS request to /v1/impoundments/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  200
    And Response body is empty
    And Response allow header should contain value GET,HEAD,OPTIONS

Impoundments HEAD authenticated succeeds
    [Tags]           impoundments    authenticated    HEAD    happy
    [Documentation]  Should return headers, content
    ...
    ...              Example: ``$ https HEAD digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated HEAD request to /v1/impoundments/${NOTICE_NUM}/${CORRELATION}
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

Impoundments GET not logged in returns error
    [Tags]           impoundments  unauthenticated    GET    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated GET request expecting HTTP 401 from /v1/impoundments/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Impoundments GET non-existent impoundment returns error
    [Tags]           impoundments  authenticated    GET    unhappy
    [Documentation]  Should return impoundment
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${NOTICE_NUM}/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request expecting HTTP 404 from /v1/impoundments/00199912}/${CORRELATION}
    Then Response code is HTTP  404
    And Response content type is  application/json
    And Response body contains  Not Found

Impoundments OPTIONS not logged in returns error
    [Tags]           impoundments    unauthenticated    OPTIONS    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated OPTIONS request expecting HTTP 401 from /v1/impoundments/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Impoundments HEAD not logged in returns error
    [Tags]           impoundments    unauthenticated    HEAD    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated HEAD request expecting HTTP 401 from /v1/impoundments/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is empty

Impoundments DELETE authenticated returns error
    [Tags]           impoundments    authenticated    DELETE    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated DELETE request expecting HTTP 500 from /v1/impoundments/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'DELETE' not supported"}

Impoundments DELETE not logged in returns error
    [Tags]           impoundments    unauthenticated    DELETE    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated DELETE request expecting HTTP 401 from /v1/impoundments/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Impoundments PUT authenticated returns error
    [Tags]           impoundments    authenticated  PUT    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PUT digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PUT request expecting HTTP 500 from /v1/impoundments/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PUT' not supported"}

Impoundments PUT not logged in returns error
    [Tags]           impoundments    unauthenticated    PUT    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PUT digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated PUT request expecting HTTP 401 from /v1/impoundments/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Impoundments POST authenticated returns error
    [Tags]           impoundments    authenticated    POST    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/impoundments/${NOTICE_NUM}/${CORRELATION} with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'POST' not supported"}

Impoundments POST not logged in returns error
    [Tags]           impoundments    unauthenticated    POST    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated POST request expecting HTTP 401 from /v1/impoundments/${NOTICE_NUM}/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Impoundments PATCH authenticated returns error
    [Tags]           impoundments    authenticated    PATCH    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PATCH request expecting HTTP 500 from /v1/impoundments/${NOTICE_NUM}/${CORRELATION} with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PATCH' not supported"}

Impoundments PATCH not logged in returns error
    [Tags]           impoundments    unauthenticated    PATCH    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated PATCH request expecting HTTP 401 from /v1/impoundments/${NOTICE_NUM}/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}