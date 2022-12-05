# Robot Framework

*** Settings ***
Documentation    Impoundments POST endpoint
Library      JSONLibrary
Library      RequestsLibrary  # https://github.com/MarketSquare/robotframework-requests
Library      Collections      # Used to check header response from RequestsLibrary
Library      String           # https://robotframework.org/robotframework/latest/libraries/String.html
Library      Process          # https://robotframework.org/robotframework/latest/libraries/Process.html
Library      OperatingSystem  # https://robotframework.org/robotframework/latest/libraries/OperatingSystem.html
Library      DateTime         # https://robotframework.org/robotframework/latest/libraries/DateTime.html

# Settings for the DEV environment
#Variables   dev.Variables              # Environment settings

Resource   lib/Keywords.resource
Resource   lib/kw-requests.resource     # Keywords for server requests
Resource   lib/kw-responses.resource    # Keywords for server responses
Resource   ./impoundments-post-DEV.resource

*** Variables ***
# See env.py
${CORRELATION} =    robot-impoundments-post-01
${VI_PROHIBITION_ID} =  22900844

*** Keywords ***
# See lib/*.robot

Generate random code table
    [Tags]  randomtest
    ${val} =  Random ${TABLE_POLICEDETACHMENTS} value
    Log  ${val}

*** Test Cases ***

#     _   _                                        _   _
#    | | | | __ _ _ __  _ __  _   _    _ __   __ _| |_| |__
#    | |_| |/ _` | '_ \| '_ \| | | |  | '_ \ / _` | __| '_ \
#    |  _  | (_| | |_) | |_) | |_| |  | |_) | (_| | |_| | | |
#    |_| |_|\__,_| .__/| .__/ \__, |  | .__/ \__,_|\__|_| |_|
#                |_|   |_|    |___/   |_|

Basic Impoundment should succeed
    [Tags]           impoundments    authenticated    POST    happy
    [Documentation]  Should create new impoundment record
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request to /v1/impoundments/${CORRELATION} with payload ${body}
    Then Response code is HTTP  200
    And Response body is  {"respMsg":"success"}

Random payload with valid values should succeed
    [Tags]  impoundments    authenticated    POST    happy  randomtest
    [Documentation]  Valid payload with random values.
    Given A random impoundment payload
    When A POST request to /v1/impoundments/${CORRELATION} with JSON payload ${new_payload}
    Then Response code is HTTP  200
    And Response body is  {"respMsg":"success"}

Random payload with future impoundment date should succeed
    [Tags]  impoundments    authenticated    POST    happy  randomtest
    [Documentation]  Future-dated impoundments are allowed by the API, and must be gated by the calling application.
    Given A random impoundment payload
    And A future impountment impoundmentDt date
    When A POST request to /v1/impoundments/${CORRELATION} with JSON payload ${new_payload}
    Then Response code is HTTP  200
    And Response body is  {"respMsg":"success"}

Random payload with many originalCauseCds should succeed
    [Tags]  impoundments    authenticated    POST    happy  randomtest
    [Documentation]  Impoundment with all original causes
    Given A random impoundment payload
    And Select all impoundment originalCauseCds
    When A POST request to /v1/impoundments/${CORRELATION} with JSON payload ${new_payload}
    Then Response code is HTTP  200
    And Response body is  {"respMsg":"success"}

Random payload with many invalid originalCauseCds should suceed
    [Tags]  impoundments    authenticated    POST    happy  randomtest
    [Documentation]  Impoundment with all original causes for ADP (should be error?)
    Given A random impoundment payload
    And Select incorrect originalCauseCds
    When A POST request to /v1/impoundments/${CORRELATION} with JSON payload ${new_payload}
    Then Response code is HTTP  200
    And Response body is  {"respMsg":"success"}

Random payload with no VIPS document should suceeed
    [Tags]  impoundments    authenticated    POST    happy  randomtest
    [Documentation]  Impoundment with all original causes for ADP (should be error?)
    Given A random impoundment payload
    And Impoundment vipsDocumentIdArray is empty
    When A POST request to /v1/impoundments/${CORRELATION} with JSON payload ${new_payload}
    Then Response code is HTTP  200
    And Response body is  {"respMsg":"success"}

Impoundments OPTIONS request should return supported options
    [Tags]           impoundments    authenticated    OPTIONS    happy
    [Documentation]  Should show supported headers
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated OPTIONS request to /v1/impoundments/${CORRELATION}
    Then Response code is HTTP  200
    And Response body is empty
    And Response allow header should contain value POST,OPTIONS

Impoundments HEAD request should return supported headers
    [Tags]           impoundments    authenticated    HEAD    happy
    [Documentation]  Should return headers, no content
    ...
    ...              Example: ``$ https HEAD digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated HEAD request to /v1/impoundments/${CORRELATION}
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response pragma header should contain value no-cache
    And Response cache-control header should contain value no-cache, no-store, max-age=0, must-revalidate
    And Response x-content-type-options header should contain value nosniff
    And Response x-frame-options header should contain value DENY
    And Response x-xss-protection header should contain value 1; mode=block



#     _   _       _                                            _   _
#    | | | |_ __ | |__   __ _ _ __  _ __  _   _    _ __   __ _| |_| |__
#    | | | | '_ \| '_ \ / _` | '_ \| '_ \| | | |  | '_ \ / _` | __| '_ \
#    | |_| | | | | | | | (_| | |_) | |_) | |_| |  | |_) | (_| | |_| | | |
#     \___/|_| |_|_| |_|\__,_| .__/| .__/ \__, |  | .__/ \__,_|\__|_| |_|
#                            |_|   |_|    |___/   |_|


Malformatted dates in impoundments POST return error
    [Tags]           impoundments    authenticated    POST    unhappy
    [Documentation]  Should return an error.
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/impoundments/${CORRELATION} with payload ${body_with_bad_dates}
    Then Response code is HTTP  500
    And Response should include text  Field error in object 'createImpoundment' on field 'vipsImpoundCreate.impoundmentDt': rejected value
    And Response should include text  Field error in object 'createImpoundment' on field 'vipsRegistrationCreateArray[0].vipsLicenceCreateObj.birthDt': rejected value
    
Overlong field value in impoundments POST returns error
    [Tags]           impoundments    authenticated    POST    unhappy
    [Documentation]  Should return an error.
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/impoundments/${CORRELATION} with payload ${body_long_values}
    Then Response code is HTTP  500
    And Response should include text  Validation failed for argument
    And Response should include text  Field error in object 'createImpoundment' on field 'vipsImpoundCreate.policeFileNo': rejected value [THIS IS A VERY LONG FILE NUMBER]
    And Response should include text  size must be between 0 and 15

Missing required field impoundments POST returns error
    [Tags]           impoundments    authenticated    POST    unhappy
    [Documentation]  Should return an error.
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/impoundments/${CORRELATION} with payload ${body_with_missing_impoundmentNoticeNo}
    Then Response code is HTTP  500
    And Response should include text  Validation failed for argument
    And Response should include text  Field error in object 'createImpoundment' on field 'vipsImpoundCreate.impoundmentNoticeNo': rejected value [null]

Missing required section impoundments POST returns error
    [Tags]           impoundments    authenticated    POST    unhappy
    [Documentation]  Should return an error.
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/impoundments/${CORRELATION} with payload ${body_with_missing_vipsImpoundCreate}
    Then Response code is HTTP  500
    And Response should include text  Validation failed for argument
    And Response should include text  Field error in object 'createImpoundment' on field 'vipsImpoundCreate': rejected value [null]

Impoundment with invalid policeDetatchmentId
    [Tags]  impoundments    authenticated    POST    unhappy  randomtest
    [Documentation]  Impoundment with all original causes for ADP (should be error?)
    Given An authenticated POST request expecting HTTP 500 from /v1/impoundments/${CORRELATION} with payload ${body_with_invalid_policeDetachmentId}
    Then Response code is HTTP  500
    And Response should include text  Failed to created impoundment for Notice Number

Impoundment with invalid vipsDocumentIdArray returns error
    [Tags]  impoundments    authenticated    POST    unhappy  randomtest
    [Documentation]  Impoundment with all original causes for ADP (should be error?)
    Given An authenticated POST request expecting HTTP 500 from /v1/impoundments/${CORRELATION} with payload ${body_with_non_existent_document}
    Then Response code is HTTP  500
    And Response should include text  Failed to created impoundment for Notice Number

Impoundment with invalid vipsImpoundmentArray returns error
    [Tags]  impoundments    authenticated    POST    unhappy  randomtest
    [Documentation]  Impoundment with all original causes for ADP (should be error?)
    Given An authenticated POST request expecting HTTP 500 from /v1/impoundments/${CORRELATION} with payload ${body_with_non_existent_vipsImpoundmentArray}
    Then Response code is HTTP  500
    And Response should include text  Failed to created impoundment for Notice Number

Empty JSON body impoundments POST returns error
    [Tags]           impoundments    authenticated    POST    unhappy
    [Documentation]  Should return an error.
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/impoundments/${CORRELATION} with payload {}
    Then Response code is HTTP  500
    And Response should include text  Validation failed for argument
    And Response should include text  Field error in object 'createImpoundment' on field 'vipsImpoundCreate': rejected value [null]

Duplicate impoundments POST returns error
    [Tags]           impoundments    authenticated    POST    unhappy
    [Documentation]  Should return an error.
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/impoundments/${CORRELATION} with payload ${body}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Failed to created impoundment for Notice Number : 22900838"}

Bad JSON impoundments POST returns error
    [Tags]           impoundments    authenticated    POST    unhappy
    [Documentation]  Should return an error.
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/impoundments/${CORRELATION} with payload This_is_a_bad_payload
    Then Response code is HTTP  500
    And Response should include text  JSON parse error
    And Response should include text  Unrecognized token 'This_is_a_bad_payload'
    And Response should include text  was expecting (JSON String, Number, Array, Object or token 'null', 'true' or 'false')
    
Impoundments GET authenticated returns error
    [Tags]           impoundments  authenticated    GET    unhappy
    [Documentation]  Should return HTTP 500
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request expecting HTTP 500 from /v1/impoundments/${CORRELATION}
    Then Response code is HTTP  500
    And Response content type is  application/json
    And Response body is  {"status_message":"Request method 'GET' not supported"}

Impoundments GET not logged in returns error
    [Tags]           impoundments  unauthenticated    GET    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION}``
    Given An unauthenticated GET request expecting HTTP 401 from /v1/impoundments/${CORRELATION}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}


Impoundments OPTIONS not logged in returns error
    [Tags]           impoundments    unauthenticated    OPTIONS    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION}``
    Given An unauthenticated OPTIONS request expecting HTTP 401 from /v1/impoundments/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Impoundments HEAD not logged in returns error
    [Tags]           impoundments    unauthenticated    HEAD    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION}``
    Given An unauthenticated HEAD request expecting HTTP 401 from /v1/impoundments/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is empty

Impoundments DELETE authenticated returns error
    [Tags]           impoundments    authenticated    DELETE    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated DELETE request expecting HTTP 500 from /v1/impoundments/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'DELETE' not supported"}

Impoundments DELETE not logged in returns error
    [Tags]           impoundments    unauthenticated    DELETE    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION}``
    Given An unauthenticated DELETE request expecting HTTP 401 from /v1/impoundments/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Impoundments PUT authenticated returns error
    [Tags]           impoundments    authenticated  PUT    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PUT digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PUT request expecting HTTP 500 from /v1/impoundments/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PUT' not supported"}

Impoundments PUT not logged in returns error
    [Tags]           impoundments    unauthenticated    PUT    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PUT digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION}``
    Given An unauthenticated PUT request expecting HTTP 401 from /v1/impoundments/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Impoundments POST not logged in returns error
    [Tags]           impoundments    unauthenticated    POST    happy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION}``
    Given An unauthenticated POST request expecting HTTP 401 from /v1/impoundments/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Impoundments PATCH authenticated returns error
    [Tags]           impoundments    authenticated    PATCH    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PATCH request expecting HTTP 500 from /v1/impoundments/${CORRELATION} with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PATCH' not supported"}

Impoundments PATCH not logged in returns error
    [Tags]           impoundments    unauthenticated    PATCH    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/impoundments/${CORRELATION}``
    Given An unauthenticated PATCH request expecting HTTP 401 from /v1/impoundments/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}