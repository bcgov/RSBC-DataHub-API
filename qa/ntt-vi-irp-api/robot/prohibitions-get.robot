# Robot Framework

*** Settings ***
Documentation    Prohibitions GET endpoint
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
${CORRELATION} =    robot-prohibitions-get-01
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

Prohibitions GET authenticated
    [Tags]           prohibitions  authenticated    GET    happy
    [Documentation]  Should return prohibition
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/prohibitions/${NOTICE_NUM}/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request to /v1/prohibitions/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response body is  {"responseMessage":{}}

Prohibitions OPTIONS authenticated
    [Tags]           prohibitions    authenticated    OPTIONS    happy
    [Documentation]  Should show supported headers
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/prohibitions/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated OPTIONS request to /v1/prohibitions/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  200
    And Response body is empty
    And Response allow header should contain value GET,HEAD,OPTIONS

Prohibitions HEAD authenticated
    [Tags]           prohibitions    authenticated    HEAD    happy
    [Documentation]  Should return headers, content
    ...
    ...              Example: ``$ https HEAD digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/prohibitions/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated HEAD request to /v1/prohibitions/${NOTICE_NUM}/${CORRELATION}
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

Prohibitions GET not logged in
    [Tags]           prohibitions  unauthenticated    GET    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/prohibitions/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated GET request expecting HTTP 401 from /v1/prohibitions/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Prohibitions OPTIONS not logged in
    [Tags]           prohibitions    unauthenticated    OPTIONS    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/prohibitions/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated OPTIONS request expecting HTTP 401 from /v1/prohibitions/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Prohibitions HEAD not logged in
    [Tags]           prohibitions    unauthenticated    HEAD    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/prohibitions/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated HEAD request expecting HTTP 401 from /v1/prohibitions/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is empty

Prohibitions DELETE authenticated
    [Tags]           prohibitions    authenticated    DELETE    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/prohibitions/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated DELETE request expecting HTTP 500 from /v1/prohibitions/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'DELETE' not supported"}

Prohibitions DELETE not logged in
    [Tags]           prohibitions    unauthenticated    DELETE    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/prohibitions/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated DELETE request expecting HTTP 401 from /v1/prohibitions/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Prohibitions PUT authenticated
    [Tags]           prohibitions    authenticated  PUT    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PUT digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/prohibitions/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PUT request expecting HTTP 500 from /v1/prohibitions/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PUT' not supported"}

Prohibitions PUT not logged in
    [Tags]           prohibitions    unauthenticated    PUT    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PUT digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/prohibitions/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated PUT request expecting HTTP 401 from /v1/prohibitions/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Prohibitions POST authenticated
    [Tags]           prohibitions    authenticated    POST    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/prohibitions/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/prohibitions/${NOTICE_NUM}/${CORRELATION} with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'POST' not supported"}

Prohibitions POST not logged in
    [Tags]           prohibitions    unauthenticated    POST    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/prohibitions/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated POST request expecting HTTP 401 from /v1/prohibitions/${NOTICE_NUM}/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Prohibitions PATCH authenticated
    [Tags]           prohibitions    authenticated    PATCH    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/prohibitions/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PATCH request expecting HTTP 500 from /v1/prohibitions/${NOTICE_NUM}/${CORRELATION} with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PATCH' not supported"}

Prohibitions PATCH not logged in
    [Tags]           prohibitions    unauthenticated    PATCH    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/prohibitions/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated PATCH request expecting HTTP 401 from /v1/prohibitions/${NOTICE_NUM}/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}