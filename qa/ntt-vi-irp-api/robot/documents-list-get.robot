# Robot Framework

*** Settings ***
Documentation    Documents GET endpoint
Library    JSONLibrary
Library      RequestsLibrary  # https://github.com/MarketSquare/robotframework-requests
Library      Collections      # Used to check header response from RequestsLibrary
Library      String           # https://robotframework.org/robotframework/latest/libraries/String.html
Library      Process          # https://robotframework.org/robotframework/latest/libraries/Process.html
Library      OperatingSystem  # https://robotframework.org/robotframework/latest/libraries/OperatingSystem.html
Library      DateTime         # https://robotframework.org/robotframework/latest/libraries/DateTime.html

# Settings for the DEV environment
#Variables   dev.Variables              # Environment settings

Resource   lib/keywords.resource        # Keywords
Resource   lib/kw-requests.resource     # Keywords for server requests
Resource   lib/kw-responses.resource    # Keywords for server responses

*** Variables ***
# See env.py
${NOTICE_NUM_ADP} =    00197501
${NOTICE_NUM_IRP} =    40197501
${NOTICE_NUM_IMP} =    30197501
${NOTICE_NUM_UL} =     20100155
${CORRELATION} =   robot-documents-list-001

*** Keywords ***
# See lib/*.robot

*** Test Cases ***

#     _   _
#    | | | | __ _ _ __  _ __  _   _
#    | |_| |/ _` | '_ \| '_ \| | | |
#    |  _  | (_| | |_) | |_) | |_| |
#    |_| |_|\__,_| .__/| .__/ \__, |
#                |_|   |_|    |___/

Retrieve IMP documents
    [Tags]           documents-list  authenticated    GET    happy
    [Documentation]  Should return prohibition
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM}/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request to /v1/documents/list/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response body is  {"results":[{"addToFileDtm":"2022-10-26T15:23:05.000-07:00","disclosedToClientDtm":null,"disclosureDocumentYN":"N","documentId":611,"documentTypeCd":"MV2687","documentTypeDsc":"Application For Review ADP","impoundmentId":null,"pageCount":1,"prohibitionId":3426,"receivedDtm":"2022-10-26T15:08:19.000-07:00"},{"addToFileDtm":"2022-10-26T15:28:14.000-07:00","disclosedToClientDtm":null,"disclosureDocumentYN":"N","documentId":612,"documentTypeCd":"MV2687","documentTypeDsc":"Application For Review ADP","impoundmentId":null,"pageCount":1,"prohibitionId":3426,"receivedDtm":"2022-10-26T15:27:55.000-07:00"}]}

Retrieve ADP documents
    [Tags]           documents-list  authenticated    GET    happy
    [Documentation]  Should return prohibition
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM_ADP}/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request to /v1/documents/list/${NOTICE_NUM_ADP}/${CORRELATION}
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response body is  TBD

Retrieve IRP documents
    [Tags]           documents-list  authenticated    GET    happy
    [Documentation]  Should return prohibition
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM_IRP}/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request to /v1/documents/list/${NOTICE_NUM_IRP}/${CORRELATION}
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response body is  TBD

Retrieve URL documents
    [Tags]           documents-list  authenticated    GET    happy
    [Documentation]  Should return prohibition
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM_UL}/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request to /v1/documents/list/${NOTICE_NUM_UL}/${CORRELATION}
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response body is  TBD


Retrieve IMP documents
    [Tags]           documents-list  authenticated    GET    happy
    [Documentation]  Should return prohibition
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM_IRP}/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request to /v1/documents/list/${NOTICE_NUM_IRP}/${CORRELATION}
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response body is  TBD

Documents GET authenticated
    [Tags]           documents-list  authenticated    GET    happy
    [Documentation]  Should return prohibition
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM}/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request to /v1/documents/list/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response body contains  {"results":

Documents GET not logged in
    [Tags]           documents-list  unauthenticated    GET    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated GET request expecting HTTP 401 from /v1/documents/list/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}


Documents OPTIONS authenticated
    [Tags]           documents-list    authenticated    OPTIONS    happy
    [Documentation]  Should show supported headers
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated OPTIONS request to /v1/documents/list/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  200
    And Response body is empty
    And Response allow header should contain value GET,HEAD,OPTIONS


#     _   _       _
#    | | | |_ __ | |__   __ _ _ __  _ __  _   _
#    | | | | '_ \| '_ \ / _` | '_ \| '_ \| | | |
#    | |_| | | | | | | | (_| | |_) | |_) | |_| |
#     \___/|_| |_|_| |_|\__,_| .__/| .__/ \__, |
#                            |_|   |_|    |___/
Request for notice number that does not exist should return error with HTTP 404
    [Tags]           documents-list  authenticated    GET    unhappy
    [Documentation]  Should return a "not found" message with HTTP response code 404.
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/9223372036854775807/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request expecting HTTP 404 from /v1/documents/list/9223372036854775807/${CORRELATION}
    Then Response code is HTTP  404
    And Response content type is  application/json
    And Response body contains  Not Found

Request for overlong notice number should return error
    [Tags]           documents-list  authenticated    GET    unhappy
    [Documentation]  The document id is a Java long integer, maximum value: 9223372036854775807. Try a document id of 9223372036854775807 + 1.
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/9223372036854775808/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request expecting HTTP 404 from /v1/documents/list/9223372036854775808/${CORRELATION}
    Then Response code is HTTP  404
    And Response content type is  application/json
    And Response body contains  Not Found

Request for notice number with alphanumeric id should return error
    [Tags]           documents-list  authenticated    GET    unhappy
    [Documentation]  Should return an error because the document is a long integer.
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/T3ST/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request expecting HTTP 404 from /v1/documents/list/TEST1/${CORRELATION}
    Then Response code is HTTP  404
    And Response content type is  application/json
    And Response body contains  Not Found

Request for empty notice number should return error
    [Tags]           documents-list  authenticated    GET    unhappy
    [Documentation]  Should return HTTP 500, or 401 (Unauthorized) because it's technically a different endpoint.
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list//${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request expecting HTTP 500 from /v1/documents/list//${CORRELATION}
    Then Response code is HTTP  500
    And Response content type is  application/json
    And Response body contains  Failed to convert value of type 'java.lang.String' to required type 'java.lang.Long'

Documents OPTIONS not logged in
    [Tags]           documents-list    unauthenticated    OPTIONS    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated OPTIONS request expecting HTTP 401 from /v1/documents/list/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents HEAD authenticated
    [Tags]           documents-list    authenticated    HEAD    happy
    [Documentation]  Should return headers, content
    ...
    ...              Example: ``$ https HEAD digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated HEAD request to /v1/documents/list/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  200
    And Response body is empty
    And Response content type is  application/json
    And Response pragma header should contain value no-cache
    And Response cache-control header should contain value no-cache, no-store, max-age=0, must-revalidate
    And Response x-content-type-options header should contain value nosniff
    And Response x-frame-options header should contain value DENY
    And Response x-xss-protection header should contain value 1; mode=block

Documents HEAD not logged in
    [Tags]           documents-list    unauthenticated    HEAD    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated HEAD request expecting HTTP 401 from /v1/documents/list/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is empty

Documents DELETE authenticated
    [Tags]           documents-list    authenticated    DELETE    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated DELETE request expecting HTTP 500 from /v1/documents/list/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'DELETE' not supported"}

Documents DELETE not logged in
    [Tags]           documents-list    unauthenticated    DELETE    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated DELETE request expecting HTTP 401 from /v1/documents/list/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents PUT authenticated
    [Tags]           documents-list    authenticated  PUT    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PUT digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PUT request expecting HTTP 500 from /v1/documents/list/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PUT' not supported"}

Documents PUT not logged in
    [Tags]           documents-list    unauthenticated    PUT    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PUT digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated PUT request expecting HTTP 401 from /v1/documents/list/${NOTICE_NUM}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents POST authenticated
    [Tags]           documents-list    authenticated    POST    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/documents/list/${NOTICE_NUM}/${CORRELATION} with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'POST' not supported"}

Documents POST not logged in
    [Tags]           documents-list    unauthenticated    POST    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated POST request expecting HTTP 401 from /v1/documents/list/${NOTICE_NUM}/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents PATCH authenticated
    [Tags]           documents-list    authenticated    PATCH    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PATCH request expecting HTTP 500 from /v1/documents/list/${NOTICE_NUM}/${CORRELATION} with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PATCH' not supported"}

Documents PATCH not logged in
    [Tags]           documents-list    unauthenticated    PATCH    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/list/${NOTICE_NUM}/${CORRELATION}``
    Given An unauthenticated PATCH request expecting HTTP 401 from /v1/documents/list/${NOTICE_NUM}/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}