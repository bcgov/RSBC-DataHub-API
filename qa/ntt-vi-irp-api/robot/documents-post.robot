# Robot Framework

*** Settings ***
Documentation    Documents POST endpoint
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
Resource   ./documents-post-DEV.resource      

*** Variables ***
# See env.py
${CORRELATION} =    robot-prohibition-post-01

*** Keywords ***
# See lib/*.robot

*** Test Cases ***

#     _   _
#    | | | | __ _ _ __  _ __  _   _
#    | |_| |/ _` | '_ \| '_ \| | | |
#    |  _  | (_| | |_) | |_) | |_| |
#    |_| |_|\__,_| .__/| .__/ \__, |
#                |_|   |_|    |___/

Submit ADP document is successful
    [Tags]           documents    authenticated    POST    happy
    [Documentation]  Should create new document
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request to /v1/documents/${CORRELATION} with payload ${DOCUMENT_POST_PAYLOAD_ADP}
    Then Response code is HTTP  200
    And Response body contains  {"document_id":

Submit IRP document is successful
    [Tags]           documents    authenticated    POST    happy
    [Documentation]  Should create new document
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request to /v1/documents/${CORRELATION} with payload ${DOCUMENT_POST_PAYLOAD_IRP}
    Then Response code is HTTP  200
    And Response body contains  {"document_id":

Submit UL document is successful
    [Tags]           documents    authenticated    POST    happy
    [Documentation]  Should create new document
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request to /v1/documents/${CORRELATION} with payload ${DOCUMENT_POST_PAYLOAD_UL}
    Then Response code is HTTP  200
    And Response body contains  {"document_id":

Submit IMP document is successful
    [Tags]           documents    authenticated    POST    happy
    [Documentation]  Should create new document
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request to /v1/documents/${CORRELATION} with payload ${DOCUMENT_POST_PAYLOAD_IMP}
    Then Response code is HTTP  200
    And Response body contains  {"document_id":


Documents OPTIONS authenticated
    [Tags]           documents    authenticated    OPTIONS    happy
    [Documentation]  Should show supported headers
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated OPTIONS request to /v1/documents/${CORRELATION}
    Then Response code is HTTP  200
    And Response body is empty
    And Response allow header should contain value GET,HEAD,OPTIONS

Documents HEAD authenticated
    [Tags]           documents    authenticated    HEAD    happy
    [Documentation]  Should return headers, content
    ...
    ...              Example: ``$ https HEAD digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated HEAD request to /v1/documents/${CORRELATION}
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

Submit document with empty JSON returns error
    [Tags]           documents    authenticated    POST    unhappy
    [Documentation]  Should return error.
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/documents/${CORRELATION} with payload "{}"
    Then Response code is HTTP  500
    And Response body contains  JSON parse error: Cannot construct instance

Submit document with empty body returns error
    [Tags]           documents    authenticated    POST    unhappy
    [Documentation]  Should return error.
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/documents/${CORRELATION} with payload ""
    Then Response code is HTTP  500
    And Response body contains  JSON parse error: Cannot coerce empty String

Submit document with malformed JSON body returns error
    [Tags]           documents    authenticated    POST    unhappy
    [Documentation]  Should return error.
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/documents/${CORRELATION} with payload a{bc123
    Then Response code is HTTP  500
    And Response body contains  JSON parse error: Unrecognized token 'a'

Submit document with invalid notice_subject_code
    [Tags]           documents    authenticated    POST    unhappy
    [Documentation]  Should return error.
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/documents/${CORRELATION} with payload ${DOCUMENT_POST_PAYLOAD_INVALID_NOTICE_SUBJECT}
    Then Response code is HTTP  500
    And Response body contains  rejected value [FINGERPRINTS]

Submit document with empty file object returns error
    [Tags]           documents    authenticated    POST    unhappy
    [Documentation]  Should return error. Actually, this generates an assertion failure from the Layer 7 gateway.
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/documents/${CORRELATION} with payload ${DOCUMENT_POST_PAYLOAD_EMPTY_FILE_OBJECT}
    Then Response code is HTTP  500
    And Response body contains  Assertion Falsified

Submit document with missing file object field returns error
    [Tags]           documents    authenticated    POST    unhappy
    [Documentation]  Should return error.
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/documents/${CORRELATION} with payload ${DOCUMENT_POST_PAYLOAD_MISSING_FILE_OBJECT}
    Then Response code is HTTP  500
    And Response body contains  Field error in object 'storeVIPSDocument' on field 'fileObject': rejected value [null]

Submit document with empty type code returns error
    [Tags]           documents    authenticated    POST    unhappy
    [Documentation]  Should return error.
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/documents/${CORRELATION} with payload ${DOCUMENT_POST_PAYLOAD_EMPTY_TYPE_CODE}
    Then Response code is HTTP  500
    And Response body contains  Assertion Falsified

Submit document with missing type code returns error
    [Tags]           documents    authenticated    POST    unhappy
    [Documentation]  Should return error. Actually, this generates an assertion failure from the Layer 7 gateway.
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/documents/${CORRELATION} with payload ${DOCUMENT_POST_PAYLOAD_MISSING_TYPE_CODE}
    Then Response code is HTTP  500
    And Response body contains  Field error in object 'storeVIPSDocument' on field 'typeCode': rejected value [null]

Submit document with invalid notice_type_code
    [Tags]           documents    authenticated    POST    unhappy
    [Documentation]  Should create new document
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/documents/${CORRELATION} with payload ${DOCUMENT_POST_PAYLOAD_INVALID_NOTICE_TYPE}
    Then Response code is HTTP  500
    And Response body contains  rejected value [GOODNESS_GRACIOUS]

Documents GET authenticated
    [Tags]           documents  authenticated    GET    unhappy
    [Documentation]  Should return HTTP 500
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request to /v1/documents/${CORRELATION}
    Then Response code is HTTP  500
    And Response content type is  application/json
    And Response body is  {"status_message":"Request method 'GET' not supported"}

Documents GET not logged in
    [Tags]           documents  unauthenticated    GET    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION}``
    Given An unauthenticated GET request expecting HTTP 401 from /v1/documents/${CORRELATION}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents OPTIONS not logged in
    [Tags]           documents    unauthenticated    OPTIONS    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION}``
    Given An unauthenticated OPTIONS request expecting HTTP 401 from /v1/documents/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents HEAD not logged in
    [Tags]           documents    unauthenticated    HEAD    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION}``
    Given An unauthenticated HEAD request expecting HTTP 401 from /v1/documents/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is empty

Documents DELETE authenticated
    [Tags]           documents    authenticated    DELETE    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated DELETE request expecting HTTP 500 from /v1/documents/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'DELETE' not supported"}

Documents DELETE not logged in
    [Tags]           documents    unauthenticated    DELETE    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION}``
    Given An unauthenticated DELETE request expecting HTTP 401 from /v1/documents/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents PUT authenticated
    [Tags]           documents    authenticated  PUT    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PUT digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PUT request expecting HTTP 500 from /v1/documents/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PUT' not supported"}

Documents PUT not logged in
    [Tags]           documents    unauthenticated    PUT    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PUT digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION}``
    Given An unauthenticated PUT request expecting HTTP 401 from /v1/documents/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents POST not logged in
    [Tags]           documents    unauthenticated    POST    happy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION}``
    Given An unauthenticated POST request expecting HTTP 401 from /v1/documents/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents PATCH authenticated
    [Tags]           documents    authenticated    PATCH    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PATCH request expecting HTTP 500 from /v1/documents/${CORRELATION} with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PATCH' not supported"}

Documents PATCH not logged in
    [Tags]           documents    unauthenticated    PATCH    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${CORRELATION}``
    Given An unauthenticated PATCH request expecting HTTP 401 from /v1/documents/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}