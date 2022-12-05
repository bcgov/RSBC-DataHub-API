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
${VIPS_DOCUMENT_ID} =    643
${CORRELATION} =         robot-documents-001

*** Keywords ***
# See lib/*.robot

*** Test Cases ***

#     _   _
#    | | | | __ _ _ __  _ __  _   _
#    | |_| |/ _` | '_ \| '_ \| | | |
#    |  _  | (_| | |_) | |_) | |_| |
#    |_| |_|\__,_| .__/| .__/ \__, |
#                |_|   |_|    |___/

Documents GET authenticated
    [Tags]           documents  authenticated    GET    happy
    [Documentation]  Should return prohibition
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request to /v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response body contains  {"document":

Documents OPTIONS authenticated
    [Tags]           documents    authenticated    OPTIONS    happy
    [Documentation]  Should show supported headers
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated OPTIONS request to /v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  200
    And Response body is empty
    And Response allow header should contain value GET,HEAD,OPTIONS

Documents HEAD authenticated
    [Tags]           documents    authenticated    HEAD    happy
    [Documentation]  Should return headers, content
    ...
    ...              Example: ``$ https HEAD digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated HEAD request to /v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION}
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

Request for document that does not exist should return error with HTTP 404
    [Tags]           documents  authenticated    GET    unhappy
    [Documentation]  Should return a "not found" message with HTTP response code 404.
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/9223372036854775807/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request expecting HTTP 404 from /v1/documents/9223372036854775807/${CORRELATION}
    Then Response code is HTTP  404
    And Response content type is  application/json
    And Response body contains  Not Found

Request for overlong document id should return error
    [Tags]           documents  authenticated    GET    unhappy
    [Documentation]  The document id is a Java long integer, maximum value: 9223372036854775807. Try a document id of 9223372036854775807 + 1.
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/9223372036854775808/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request expecting HTTP 500 from /v1/documents/9223372036854775808/${CORRELATION}
    Then Response code is HTTP  500
    And Response content type is  application/json
    And Response body contains  Failed to convert value of type 'java.lang.String' to required type 'java.lang.Long'; nested exception is java.lang.NumberFormatException: For input string:

Request for document with alphanumeric id should return error
    [Tags]           documents  authenticated    GET    unhappy
    [Documentation]  Should return an error because the document is a long integer.
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/T3ST/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request expecting HTTP 500 from /v1/documents/TEST1/${CORRELATION}
    Then Response code is HTTP  500
    And Response content type is  application/json
    And Response body contains  Failed to convert value of type 'java.lang.String' to required type 'java.lang.Long'; nested exception is java.lang.NumberFormatException: For input string

Request for empty document id should return error
    [Tags]           documents  authenticated    GET    unhappy
    [Documentation]  Should return HTTP 500, or 401 (Unauthorized) because it's technically a different endpoint.
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents//\${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request expecting HTTP 500 from /v1/documents//${CORRELATION}
    Then Response code is HTTP  500
    And Response content type is  application/json
    And Response body contains  Request method 'GET' not supported

Documents GET not logged in
    [Tags]           documents  unauthenticated    GET    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION}``
    Given An unauthenticated GET request expecting HTTP 401 from /v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents OPTIONS not logged in
    [Tags]           documents    unauthenticated    OPTIONS    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION}``
    Given An unauthenticated OPTIONS request expecting HTTP 401 from /v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents HEAD not logged in
    [Tags]           documents    unauthenticated    HEAD    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION}``
    Given An unauthenticated HEAD request expecting HTTP 401 from /v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is empty

Documents DELETE authenticated
    [Tags]           documents    authenticated    DELETE    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated DELETE request expecting HTTP 500 from /v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'DELETE' not supported"}

Documents DELETE not logged in
    [Tags]           documents    unauthenticated    DELETE    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION}``
    Given An unauthenticated DELETE request expecting HTTP 401 from /v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents PUT authenticated
    [Tags]           documents    authenticated  PUT    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PUT digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PUT request expecting HTTP 500 from /v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PUT' not supported"}

Documents PUT not logged in
    [Tags]           documents    unauthenticated    PUT    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PUT digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION}``
    Given An unauthenticated PUT request expecting HTTP 401 from /v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents POST authenticated
    [Tags]           documents    authenticated    POST    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION} with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'POST' not supported"}

Documents POST not logged in
    [Tags]           documents    unauthenticated    POST    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION}``
    Given An unauthenticated POST request expecting HTTP 401 from /v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents PATCH authenticated
    [Tags]           documents    authenticated    PATCH    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PATCH request expecting HTTP 500 from /v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION} with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PATCH' not supported"}

Documents PATCH not logged in
    [Tags]           documents    unauthenticated    PATCH    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION}``
    Given An unauthenticated PATCH request expecting HTTP 401 from /v1/documents/${VIPS_DOCUMENT_ID}/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}