# Robot Framework

*** Settings ***
Documentation    Healthcheck endpoint
Library    JSONLibrary
Library      RequestsLibrary  # https://github.com/MarketSquare/robotframework-requests
Library      Collections      # Used to check header response from RequestsLibrary
Library      String           # https://robotframework.org/robotframework/latest/libraries/String.html
Library      Process          # https://robotframework.org/robotframework/latest/libraries/Process.html
Library      OperatingSystem  # https://robotframework.org/robotframework/latest/libraries/OperatingSystem.html
Library      DateTime         # https://robotframework.org/robotframework/latest/libraries/DateTime.html

# Settings for the DEV environment
Resource   dev.resource              # Environment settings

Resource   lib/keywords.resource        # Keywords
Resource   lib/kw-requests.resource     # Keywords for server requests
Resource   lib/kw-responses.resource    # Keywords for server responses

*** Variables ***
# See dev.resources

*** Keywords ***
# See lib/*.robot

*** Test Cases ***


Healthcheck GET authenticated
    [Tags]           healthcheck  authenticated    GET    happy
    [Documentation]  Should return statuses
    ...
    ...              Example: ``$ https ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/utility/ords/ping/robota1 --auth "user:$PASSWORD"``
    Given An authenticated GET request to /v1/utility/ords/ping/robot1
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response body is  {"responseMessage":{"VIPS ORDS Health Status":"success","DIGITAL FORMS ORDS Health Status":"success"}}

Healthcheck GET not logged in
    [Tags]           healthcheck  unauthenticated    GET    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/utility/ords/ping/robot1``
    Given An unauthenticated GET request expecting HTTP 401 from /v1/utility/ords/ping/robot1
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Healthcheck OPTIONS authenticated
    [Tags]           healthcheck    authenticated    OPTIONS    happy
    [Documentation]  Should show supported headers
    ...
    ...              Example: ``$ https OPTIONS ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/utility/ords/ping/robot1 --auth user:$PASSWORD``
    Given An authenticated OPTIONS request to /v1/utility/ords/ping/robot1
    Then Response code is HTTP  200
    And Response body is empty
    And Response allow header should contain value GET,HEAD,OPTIONS

Healthcheck OPTIONS not logged in
    [Tags]           healthcheck    unauthenticated    OPTIONS    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/utility/ords/ping/robot1``
    Given An unauthenticated OPTIONS request expecting HTTP 401 from /v1/utility/ords/ping/robot1
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Healthcheck HEAD authenticated
    [Tags]           healthcheck    authenticated    HEAD    happy
    [Documentation]  Should return headers, content
    ...
    ...              Example: ``$ https HEAD ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/utility/ords/ping/robot1 --auth user:$PASSWORD``
    Given An authenticated HEAD request to /v1/utility/ords/ping/robot1
    Then Response code is HTTP  200
    And Response body is empty
    And Response content type is  application/json
    And Response pragma header should contain value no-cache
    And Response cache-control header should contain value no-cache, no-store, max-age=0, must-revalidate
    And Response x-content-type-options header should contain value nosniff
    And Response x-frame-options header should contain value DENY
    And Response x-xss-protection header should contain value 1; mode=block

Healthcheck HEAD not logged in
    [Tags]           healthcheck    unauthenticated    HEAD    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/utility/ords/ping/robot1``
    Given An unauthenticated HEAD request expecting HTTP 401 from /v1/utility/ords/ping/robot1
    Then Response code is HTTP  401
    And Response body is empty

Healthcheck DELETE authenticated
    [Tags]           healthcheck    authenticated    DELETE    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https DELETE ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/utility/ords/ping/robot1 --auth user:$PASSWORD``
    Given An authenticated DELETE request expecting HTTP 500 from /v1/utility/ords/ping/robot1
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'DELETE' not supported"}

Healthcheck DELETE not logged in
    [Tags]           healthcheck    unauthenticated    DELETE    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https DELETE ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/utility/ords/ping/robot1``
    Given An unauthenticated DELETE request expecting HTTP 401 from /v1/utility/ords/ping/robot1
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Healthcheck PUT authenticated
    [Tags]           healthcheck    authenticated  PUT    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PUT ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/utility/ords/ping/robot1 --auth user:$PASSWORD``
    Given An authenticated PUT request expecting HTTP 500 from /v1/utility/ords/ping/robot1
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PUT' not supported"}

Healthcheck PUT not logged in
    [Tags]           healthcheck    unauthenticated    PUT    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PUT ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/utility/ords/ping/robot1``
    Given An unauthenticated PUT request expecting HTTP 401 from /v1/utility/ords/ping/robot1
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Healthcheck POST authenticated
    [Tags]           healthcheck    authenticated    POST    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https POST ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/utility/ords/ping/robot1 --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/utility/ords/ping/robot1 with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'POST' not supported"}

Healthcheck POST not logged in
    [Tags]           healthcheck    unauthenticated    POST    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https POST ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/utility/ords/ping/robot1``
    Given An unauthenticated POST request expecting HTTP 401 from /v1/utility/ords/ping/robot1 with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Healthcheck PATCH authenticated
    [Tags]           healthcheck    authenticated    PATCH    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PATCH ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/utility/ords/ping/robot1 --auth user:$PASSWORD``
    Given An authenticated PATCH request expecting HTTP 500 from /v1/utility/ords/ping/robot1 with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PATCH' not supported"}

Healthcheck PATCH not logged in
    [Tags]           healthcheck    unauthenticated    PATCH    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PATCH ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/utility/ords/ping/robot1``
    Given An unauthenticated PATCH request expecting HTTP 401 from /v1/utility/ords/ping/robot1 with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}