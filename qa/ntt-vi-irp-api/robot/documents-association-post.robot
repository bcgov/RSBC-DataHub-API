# Robot Framework

*** Settings ***
Documentation    Documents POST endpoint
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
Resource   ./documents-association-post.resource
Resource   ./documents-post-DEV.resource

*** Variables ***
# See env.py
${CORRELATION} =    robot-prohibition-post-01
${DOCUMENT_ID} =     617

*** Keywords ***
# See lib/*.robot

A new impoundment with no associated document
    An authenticated POST request to /v1/impoundments/${CORRELATION} with payload ${impoundment_body}
    And Response code is HTTP  200
    Set Test Variable    ${test_impoundment}  ${test_response}

A new document with no associated impoundment or prohibition
    An authenticated POST request to /v1/documents/${CORRELATION} with payload ${DOCUMENT_POST_PAYLOAD_IMP}
    And Response code is HTTP  200
    Set Test Variable    ${test_document}  ${test_response}
    ${document_id} =  JSONLibrary.Get Value From Json    ${test_response}    $..document_id
    Log  New document is: ${document_id}

*** Test Cases ***

#     _   _
#    | | | | __ _ _ __  _ __  _   _
#    | |_| |/ _` | '_ \| '_ \| | | |
#    |  _  | (_| | |_) | |_) | |_| |
#    |_| |_|\__,_| .__/| .__/ \__, |
#                |_|   |_|    |___/

Documents POST authenticated
    [Tags]           documents-association    authenticated    POST    happy
    [Documentation]  Should create document association
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${DOCUMENT_ID}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request to /v1/documents/association/notice/${DOCUMENT_ID}/${CORRELATION} with payload {"noticeNo":"22900213","noticeTypeCd": "IMP"}
    #Then Response code is HTTP  200
    And Response body is  {"status_message":"success"}

Associate new document with new impoundment
    [Tags]            documents-association  authenticated  POST  happy  end-to-end
    [Documentation]   Should find association
    Given A new impoundment with no associated document
    And A new document with no associated impoundment or prohibition
    An authenticated POST request to /v1/documents/association/notice/${DOCUMENT_ID}/${CORRELATION} with payload {"noticeNo":"22900213","noticeTypeCd": "IMP"}
    Then Response code is HTTP  200
    And Response body is  {"status_message":"success"}

Documents OPTIONS authenticated
    [Tags]           documents-association    authenticated    OPTIONS    happy
    [Documentation]  Should show supported headers
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${DOCUMENT_ID}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated OPTIONS request to /v1/documents/association/notice/${DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  200
    And Response body is empty
    And Response allow header should contain value GET,HEAD,OPTIONS

Documents HEAD authenticated
    [Tags]           documents-association    authenticated    HEAD    happy
    [Documentation]  Should return headers, content
    ...
    ...              Example: ``$ https HEAD digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${DOCUMENT_ID}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated HEAD request to /v1/documents/association/notice/${DOCUMENT_ID}/${CORRELATION}
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

Documents association with empty payload returns error
    [Tags]           documents-association    authenticated    POST    unhappy
    [Documentation]  Should create document association
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${DOCUMENT_ID}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/documents/association/notice/${DOCUMENT_ID}/${CORRELATION} with payload "{}"
    
    Then Response code is HTTP  500
    And Response body contains  JSON parse error: Cannot construct instance

Request association for document that does not exist should return error
    [Tags]           documents-association    authenticated    POST    unhappy
    [Documentation]  Should return an error, but currently returns an HTTP 201 ("CREATED"). Discussed this with Shaun, and it comes
    ...              from VIPS, there is no validation in the API itself. VIPS reports that the operation was successful. As this
    ...              is unlikely to be an issue in the Digital Forms project, as long as the system calling the API checks its data,
    ...              I'm just leaving this test failing for now, rather than submit a defect to fix an issue that may never happen in real life.
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${DOCUMENT_ID}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 404 from /v1/documents/association/notice/99123457/${CORRELATION} with payload {"noticeNo":"22900213","noticeTypeCd": "IMP"}
    Then Response code is HTTP  404
    And Response body contains  Not Found




Documents GET authenticated
    [Tags]           documents-association  authenticated    GET    unhappy
    [Documentation]  Should return HTTP 500
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${DOCUMENT_ID}/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request to /v1/documents/association/notice/${DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  500
    And Response content type is  application/json
    And Response body is  {"status_message":"Request method 'GET' not supported"}

Documents GET not logged in
    [Tags]           documents-association  unauthenticated    GET    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${DOCUMENT_ID}/${CORRELATION}``
    Given An unauthenticated GET request expecting HTTP 401 from /v1/documents/association/notice/${DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}


Documents OPTIONS not logged in
    [Tags]           documents-association    unauthenticated    OPTIONS    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${DOCUMENT_ID}/${CORRELATION}``
    Given An unauthenticated OPTIONS request expecting HTTP 401 from /v1/documents/association/notice/${DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents HEAD not logged in
    [Tags]           documents-association    unauthenticated    HEAD    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${DOCUMENT_ID}/${CORRELATION}``
    Given An unauthenticated HEAD request expecting HTTP 401 from /v1/documents/association/notice/${DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is empty

Documents DELETE authenticated
    [Tags]           documents-association    authenticated    DELETE    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${DOCUMENT_ID}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated DELETE request expecting HTTP 500 from /v1/documents/association/notice/${DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'DELETE' not supported"}

Documents DELETE not logged in
    [Tags]           documents-association    unauthenticated    DELETE    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${DOCUMENT_ID}/${CORRELATION}``
    Given An unauthenticated DELETE request expecting HTTP 401 from /v1/documents/association/notice/${DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents PUT authenticated
    [Tags]           documents-association    authenticated  PUT    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PUT digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${DOCUMENT_ID}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PUT request expecting HTTP 500 from /v1/documents/association/notice/${DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PUT' not supported"}

Documents PUT not logged in
    [Tags]           documents-association    unauthenticated    PUT    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PUT digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${DOCUMENT_ID}/${CORRELATION}``
    Given An unauthenticated PUT request expecting HTTP 401 from /v1/documents/association/notice/${DOCUMENT_ID}/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents POST not logged in
    [Tags]           documents-association    unauthenticated    POST    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${DOCUMENT_ID}/${CORRELATION}``
    Given An unauthenticated POST request expecting HTTP 401 from /v1/documents/association/notice/${DOCUMENT_ID}/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Documents PATCH authenticated
    [Tags]           documents-association    authenticated    PATCH    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${DOCUMENT_ID}/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PATCH request expecting HTTP 500 from /v1/documents/association/notice/${DOCUMENT_ID}/${CORRELATION} with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PATCH' not supported"}

Documents PATCH not logged in
    [Tags]           documents-association    unauthenticated    PATCH    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${DOCUMENT_ID}/${CORRELATION}``
    Given An unauthenticated PATCH request expecting HTTP 401 from /v1/documents/association/notice/${DOCUMENT_ID}/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}