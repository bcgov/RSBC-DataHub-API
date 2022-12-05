# Digital Forms 12/24 web service tests

# =======================================================================================
#                                _
#     /\                        (_)
#    /  \   __ _  ___ _ __   ___ _  ___  ___
#   / /\ \ / _` |/ _ \ '_ \ / __| |/ _ \/ __|
#  / ____ \ (_| |  __/ | | | (__| |  __/\__ \
# /_/    \_\__, |\___|_| |_|\___|_|\___||___/
#           __/ |
#          |___/
#
# Tests for the /api/v1/agencies endpoints in 12/24 web service
# =======================================================================================

*** Settings ***


Documentation  Digital Forms 12/24 web service test suite for the ``/api/v1/agencies`` endpoints and methods.
...
...            See current implementation in DFTTF source code (2021-12-22):
...            https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/agencies.py
...            
...            To validate the agency list by hand, compare it to the config_jurisdictional table in the MRE 
...            from all three regions (NSE, VIR, LMD). See wiki for details: 
...            https://justice.gov.bc.ca/wiki/display/REOS/MRE+jurisdiction+%28police+agency%29+tables
...
...            The test documentation for the endpoints at: https://justice.gov.bc.ca/wiki/pages/viewpage.action?pageId=314671737


Library      RequestsLibrary  # https://github.com/MarketSquare/robotframework-requests
Library      Collections      # https://robotframework.org/robotframework/latest/libraries/Collections.html
Library      String           # https://robotframework.org/robotframework/latest/libraries/String.html
Library      Process          # https://robotframework.org/robotframework/latest/libraries/Process.html
Library      OperatingSystem  # https://robotframework.org/robotframework/latest/libraries/OperatingSystem.html
Library      DateTime         # https://robotframework.org/robotframework/latest/libraries/DateTime.html

Resource     dfttf-dev.resource             # Variables specific to environments (DEV, TEST)
Resource     dfttf-keywords.resource        # Shared library of Underlying keywords

Suite Setup  Create TTF sessions


*** Test Cases ***

#   _____ ______ _______
#  / ____|  ____|__   __|
# | |  __| |__     | |
# | | |_ |  __|    | |
# | |__| | |____   | |
#  \_____|______|  |_|

Get all agencies with no authentication
    [Tags]           agencies  GET  unauthenticated  happy
    [Documentation]  HTTP GET: full agency list
    ...
    ...              *Should* be available with or without authentication or token.
    ...

    ...
    ...              Python line in DFTTF source: ``@bp.route('/agencies', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/agencies.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/agencies``
    Given An unauthenticated HTTP GET request to /api/v1/agencies
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Every record should be 1 to 4 characters long
    And Each item in the response should use ASCII encoding
    And Each item in the response should have no leading or trailing spaces
    And Response should have at least 150 records
    And There should be no duplicate values in the response payload


Get all agencies with authentication should return same results as with no authentication
    [Tags]           agencies  GET  authenticated  happy
    [Documentation]  HTTP GET: full agency list
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/agencies', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/agencies.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/agencies --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP GET request to /api/v1/agencies
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response should be identical to the last unauthenticated request


Get all agencies with officer token should return same results as with no authentication
    [Tags]           agencies  GET  authenticated  happy
    [Documentation]  HTTP GET: full agency list
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/agencies', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/agencies.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/agencies authorization:"${OFFICER_TOKEN}"``
    Given An officer token HTTP GET request to /api/v1/agencies
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response should be identical to the last unauthenticated request


Get all agencies with admin token should return same results as with no authentication
    [Tags]           agencies  GET  authenticated  happy
    [Documentation]  HTTP GET: full agency list
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/agencies', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/agencies.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/agencies authorization:"${OFFICER_TOKEN}"``
    Given An admin token HTTP GET request to /api/v1/agencies
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response should be identical to the last unauthenticated request


Get one agency without authentication is not implemented
    [Tags]  agencies  GET
    [Documentation]  HTTP GET: just  one agency (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/agencies/<string:agency_id>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/agencies.py
    ...
    ...              Example manual call: ``$ http POST :5009/api/v1/agencies/DE``
    Given An unauthenticated HTTP GET request expecting response 405 from /api/v1/agencies/DE
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Get one agency with basic auth is not implemented
    [Tags]  agencies  GET
    [Documentation]  HTTP GET: just  one agency (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/agencies/<string:agency_id>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/agencies.py
    ...
    ...              Example manual call: ``$ http POST :5009/api/v1/agencies/DE``
    Given An authenticated HTTP GET request expecting response 405 from /api/v1/agencies/DE
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Get one agency with officer token is not implemented
    [Tags]  agencies  GET
    [Documentation]  HTTP GET: just  one agency (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/agencies/<string:agency_id>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/agencies.py
    ...
    ...              Example manual call: ``$ http POST :5009/api/v1/agencies/DE --authorization:"${OFFICER_TOKEN}``
    Given An officer token HTTP GET request expecting response 405 from /api/v1/agencies/DE
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Get one agency with admin token is not implemented
    [Tags]  agencies  GET 
    [Documentation]  HTTP GET: just  one agency (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/agencies/<string:agency_id>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/agencies.py
    ...
    ...              Example manual call: ``$ http POST :5009/api/v1/agencies/DE --authorization:"${ADMIN_TOKEN}``
    Given An admin token HTTP GET request expecting response 405 from /api/v1/agencies/DE
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


#  _____   ____   _____ _______
# |  __ \ / __ \ / ____|__   __|
# | |__) | |  | | (___    | |
# |  ___/| |  | |\___ \   | |
# | |    | |__| |____) |  | |
# |_|     \____/|_____/   |_|

Create an agency without authentication or token returns authorization error
    [Tags]  agencies  POST  unhappy
    [Documentation]  HTTP POST: add an agency (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/agencies', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/agencies.py
    ...
    ...              Example manual call: ``$ echo '{"1234","TEST POLICE"}' | http POST :5009/api/v1/agencies``
    Given An unauthenticated HTTP POST request expecting response 401 from /api/v1/agencies with payload {"1234","TEST POLICE"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create an agency with basic authentication returns authorization error
    [Tags]  agencies  POST  unhappy
    [Documentation]  HTTP POST: add an agency (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/agencies', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/agencies.py
    ...
    ...              Example manual call: ``$ echo '{"1234","TEST POLICE"}' | http POST :5009/api/v1/agencies --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP POST request expecting response 401 from /api/v1/agencies with payload {"1234","TEST POLICE"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create an agency with officer token returns authorization error
    [Tags]  agencies  POST  unhappy
    [Documentation]  HTTP POST: add an agency (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/agencies', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/agencies.py
    ...
    ...              Example manual call: ``$ echo '{"1234","TEST POLICE"}' | http POST :5009/api/v1/agencies authorization:"${OFFICER_TOKEN}"``
    Given An officer token HTTP POST request expecting response 401 from /api/v1/agencies with payload {"1234","TEST POLICE"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create an agency with admin token not implemented
    [Tags]  agencies  POST  happy
    [Documentation]  HTTP POST: add an agency (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/agencies', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/agencies.py
    ...
    ...              Example manual call: ``$ echo '{"1234","TEST POLICE"}' | http POST :5009/api/v1/agencies authorization:"${ADMIN_TOKEN}"``
    Given An admin token HTTP POST request expecting response 405 from /api/v1/agencies with payload {"1234","TEST POLICE"}
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


#  _____     _______ _____ _    _
# |  __ \ /\|__   __/ ____| |  | |
# | |__) /  \  | | | |    | |__| |
# |  ___/ /\ \ | | | |    |  __  |
# | |  / ____ \| | | |____| |  | |
# |_| /_/    \_\_|  \_____|_|  |_|

Update an agency without authentication returns authorization error
    [Tags]  agencies  PATCH
    [Documentation]  HTTP PATCH: update an agency (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/agencies', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/agencies.py
    ...
    ...              Example manual call: ``$ echo '{"1234","TEST POLICE"}' | http PATCH :5009/api/v1/agencies``
    Given An unauthenticated HTTP PATCH request expecting response 401 from /api/v1/agencies/DE with payload {"DE":"DE2"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Update an agency with basic auth returns authorization error
    [Tags]  agencies  PATCH
    [Documentation]  HTTP PATCH: update an agency (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/agencies', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/agencies.py
    ...
    ...              Example manual call: ``$ echo '{"1234","TEST POLICE"}' | http PATCH :5009/api/v1/agencies --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP PATCH request expecting response 401 from /api/v1/agencies/DE with payload {"DE":"DE2"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Update an agency with officer token returns authorization error
    [Tags]  agencies  PATCH
    [Documentation]  HTTP PATCH: update an agency (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/agencies', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/agencies.py
    ...
    ...              Example manual call: ``$ echo '{"1234","TEST POLICE"}' | http PATCH :5009/api/v1/agencies authorization:"${ADMIN_TOKEN}"``
    Given An officer token HTTP PATCH request expecting response 401 from /api/v1/agencies/DE with payload {"DE":"DE2"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Update an agency with admin token not implemented
    [Tags]  agencies  PATCH
    [Documentation]  HTTP PATCH: update an agency (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/agencies', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/agencies.py
    ...
    ...              Example manual call: ``$ echo '{"1234","TEST POLICE"}' | http PATCH :5009/api/v1/agencies authorization:"${ADMIN_TOKEN}"``
    Given An admin token HTTP PATCH request expecting response 405 from /api/v1/agencies/DE with payload {"DE":"DE2"}
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}



#  _    _ ______          _____
# | |  | |  ____|   /\   |  __ \
# | |__| | |__     /  \  | |  | |
# |  __  |  __|   / /\ \ | |  | |
# | |  | | |____ / ____ \| |__| |
# |_|  |_|______/_/    \_\_____/

Get agencies list headers
    [Tags]  agencies  HEAD  happy
    [Documentation]  HTTP HEAD
    ...
    ...              An HTTP HEAD request is expected to return the HTTP headers for a request
    ...              without a body.
    ...
    ...              Example manual call: ``$ http HEAD :5009/api/v1/agencies``
    Given An unauthenticated HTTP HEAD request to /api/v1/agencies
    And Response code is HTTP  200
    And Response body should be empty
    And Response Access-Control-Allow-Origin header should contain value *
    And Response Content-Type header should contain value application/json


Get agencies list headers
    [Tags]  agencies  HEAD  happy
    [Documentation]  HTTP HEAD
    ...
    ...              An HTTP HEAD request is expected to return the HTTP headers for a request
    ...              without a body.
    ...
    ...              Example manual call: ``$ http HEAD :5009/api/v1/agencies/DE``
    And An unauthenticated HTTP HEAD request to /api/v1/agencies/DE
    And Response code is HTTP  200
    And Response body should be empty
    And Response Access-Control-Allow-Origin header should contain value *
    And Response Content-Type header should contain value application/json


#   ____  _____ _______ _____ ____  _   _  _____
#  / __ \|  __ \__   __|_   _/ __ \| \ | |/ ____|
# | |  | | |__) | | |    | || |  | |  \| | (___
# | |  | |  ___/  | |    | || |  | | . ` |\___ \
# | |__| | |      | |   _| || |__| | |\  |____) |
#  \____/|_|      |_|  |_____\____/|_| \_|_____/

Get agencies list options
    [Tags]  agencies  OPTIONS  happy
    [Documentation]  HTTP OPTIONS
    ...
    ...              An HTTP OPTIONS request is expected to return a list of supported HTTP methods
    ...              for an endpoint (eg. GET, POST, HEAD, OPTIONS).
    ...
    ...             Example manual call: ``$ http OPTIONS :5009/api/v1/agencies``
    Given An unauthenticated HTTP OPTIONS request to /api/v1/agencies
    Then Response code is HTTP  200
    And Response Allow header should contain value GET
    And Response Allow header should contain value POST
    And Response Allow header should contain value HEAD
    And Response Allow header should contain value OPTIONS
    And Response Allow header should not contain value DELETE
    And Response Allow header should not contain value PATCH
    And Response Allow header should not contain value PUT


Get individual agency options
    [Tags]  agencies  OPTIONS  happy
    [Documentation]  HTTP OPTIONS: supported methods
    ...
    ...              An HTTP OPTIONS request is expected to return a list of supported HTTP methods
    ...              for an endpoint (GET, PATCH, HEAD, OPTIONS).
    ...
    ...             Example manual call: ``$ http OPTIONS :5009/api/v1/agencies/DE``
    Given An unauthenticated HTTP OPTIONS request to /api/v1/agencies/DE
    Then Response code is HTTP  200
    And Response Allow header should contain value GET
    And Response Allow header should contain value PATCH
    And Response Allow header should contain value HEAD
    And Response Allow header should contain value OPTIONS
    And Response Allow header should not contain value DELETE
    And Response Allow header should not contain value POST
    And Response Allow header should not contain value PUT
