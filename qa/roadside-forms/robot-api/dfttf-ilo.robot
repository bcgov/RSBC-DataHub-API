# Digital Forms 12/24 web service tests

# =======================================================================================
#  _____ _      ____
# |_   _| |    / __ \
#   | | | |   | |  | |___
#   | | | |   | |  | / __|
#  _| |_| |___| |__| \__ \
# |_____|______\____/|___/
#
# Tests for the /api/v1/impound_lot_operators endpoints in 12/24 web service
# =======================================================================================

*** Settings ***


Documentation  Digital Forms 12/24 web service test suite for the ``/api/v1/impound_lot_operators`` endpoints and methods.
...
...            See current implementation in DFTTF source code (2021-12-22):
...            https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/colors.py
...            
...            There is no 'impound lot operators' table in the MRE.
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

Get all impound lot operators with no authentication
    [Tags]           impound lot operators  GET  unauthenticated
    [Documentation]  HTTP GET
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/impound_lot_operators', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/impound_lot_operators.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/impound_lot_operators``
    Given An unauthenticated HTTP GET request to /api/v1/impound_lot_operators
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Every record should have 4 subrecords
    And Each item in the response should use ASCII encoding
    And Each item in the response should have no leading or trailing spaces
    And Response should have at least 200 records
    And There should be no duplicate values in the response payload



Get all impound lot operators with authentication should return same results as with no authentication
    [Tags]           impound lot operators  GET  authenticated
    [Documentation]  HTTP GET
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/impound_lot_operators', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/impound_lot_operators.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/impound_lot_operators``
    Given An authenticated HTTP GET request to /api/v1/impound_lot_operators
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response should be identical to the last unauthenticated request


Get all impound lot operators with officer token should return same results as with no authentication
    [Tags]           impound lot operators  GET  authenticated
    [Documentation]  HTTP GET
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/impound_lot_operators', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/impound_lot_operators.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/impound_lot_operators``
    Given An officer token HTTP GET request to /api/v1/impound_lot_operators
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response should be identical to the last unauthenticated request


Get all impound lot operators with admin token should return same results as with no authentication
    [Tags]           impound lot operators  GET  authenticated
    [Documentation]  HTTP GET
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/impound_lot_operators', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/impound_lot_operators.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/impound_lot_operators``
    Given An admin token HTTP GET request to /api/v1/impound_lot_operators
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response should be identical to the last unauthenticated request


Get one impound lot operator without authentication is not implemented
    [Tags]  impound lot operators  GET
    [Documentation]  HTTP GET: just  one impound lot operator (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/impound_lot_operators/<string:impound lot operator_id>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/impound_lot_operators.py
    ...
    ...              Example manual call: ``$ http POST :5009/api/v1/impound_lot_operators/ABC``
    Given An unauthenticated HTTP GET request expecting response 405 from /api/v1/impound_lot_operators/ABC
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Get one impound lot operator with basic auth is not implemented
    [Tags]  impound lot operators  GET
    [Documentation]  HTTP GET: just  one impound lot operator (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/impound_lot_operators/<string:impound lot operator_id>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/impound_lot_operators.py
    ...
    ...              Example manual call: ``$ http POST :5009/api/v1/impound_lot_operators/ABC``
    Given An authenticated HTTP GET request expecting response 405 from /api/v1/impound_lot_operators/ABC
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Get one impound lot operator with officer token is not implemented
    [Tags]  impound lot operators  GET
    [Documentation]  HTTP GET: just  one impound lot operator (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/impound_lot_operators/<string:impound lot operator_id>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/impound_lot_operators.py
    ...
    ...              Example manual call: ``$ http POST :5009/api/v1/impound_lot_operators/ABC --authorization:"${OFFICER_TOKEN}``
    Given An officer token HTTP GET request expecting response 405 from /api/v1/impound_lot_operators/ABC
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Get one impound lot operator with admin token is not implemented
    [Tags]  impound lot operators  GET 
    [Documentation]  HTTP GET: just  one impound lot operator (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/impound_lot_operators/<string:impound lot operator_id>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/impound_lot_operators.py
    ...
    ...              Example manual call: ``$ http POST :5009/api/v1/impound_lot_operators/ABC --authorization:"${ADMIN_TOKEN}``
    Given An admin token HTTP GET request expecting response 405 from /api/v1/impound_lot_operators/ABC
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


#  _____   ____   _____ _______
# |  __ \ / __ \ / ____|__   __|
# | |__) | |  | | (___    | |
# |  ___/| |  | |\___ \   | |
# | |    | |__| |____) |  | |
# |_|     \____/|_____/   |_|

Create an impound lot operator without authentication or token returns authorization error
    [Tags]  impound lot operators  POST  unhappy
    [Documentation]  HTTP POST: add an impound lot operator (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/impound_lot_operators', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/impound_lot_operators.py
    ...
    ...              Example manual call: ``$ echo '{"city": "Saanich","id": "4CC0B2D5-7882-50E6-79E7-3C3AEAA22222","lot_address": "22222 Saanich Road","name": "Saanich 222 Towing","phone": "250-250-2222"}' | http POST :5009/api/v1/impound_lot_operators``
    Given An unauthenticated HTTP POST request expecting response 401 from /api/v1/impound_lot_operators with payload {"city": "Saanich","id": "4CC0B2D5-7882-50E6-79E7-3C3AEAA22222","lot_address": "22222 Saanich Road","name": "Saanich 222 Towing","phone": "250-250-2222"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create an impound lot operator with basic authentication returns authorization error
    [Tags]  impound lot operators  POST  unhappy
    [Documentation]  HTTP POST: add an impound lot operator (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/impound_lot_operators', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/impound_lot_operators.py
    ...
    ...              Example manual call: ``$ echo '{"city": "Saanich","id": "4CC0B2D5-7882-50E6-79E7-3C3AEAA22222","lot_address": "22222 Saanich Road","name": "Saanich 222 Towing","phone": "250-250-2222"}' | http POST :5009/api/v1/impound_lot_operators --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP POST request expecting response 401 from /api/v1/impound_lot_operators with payload {"city": "Saanich","id": "4CC0B2D5-7882-50E6-79E7-3C3AEAA22222","lot_address": "22222 Saanich Road","name": "Saanich 222 Towing","phone": "250-250-2222"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create an impound lot operator with officer token returns authorization error
    [Tags]  impound lot operators  POST  unhappy
    [Documentation]  HTTP POST: add an impound lot operator (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/impound_lot_operators', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/impound_lot_operators.py
    ...
    ...              Example manual call: ``$ echo '{"city": "Saanich","id": "4CC0B2D5-7882-50E6-79E7-3C3AEAA22222","lot_address": "22222 Saanich Road","name": "Saanich 222 Towing","phone": "250-250-2222"}' | http POST :5009/api/v1/impound_lot_operators authorization:"${OFFICER_TOKEN}"``
    Given An officer token HTTP POST request expecting response 401 from /api/v1/impound_lot_operators with payload {"city": "Saanich","id": "4CC0B2D5-7882-50E6-79E7-3C3AEAA22222","lot_address": "22222 Saanich Road","name": "Saanich 222 Towing","phone": "250-250-2222"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create an impound lot operator with admin token not implemented
    [Tags]  impound lot operators  POST  happy
    [Documentation]  HTTP POST: add an impound lot operator (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/impound_lot_operators', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/impound_lot_operators.py
    ...
    ...              Example manual call: ``$ echo '{"city": "Saanich","id": "4CC0B2D5-7882-50E6-79E7-3C3AEAA22222","lot_address": "22222 Saanich Road","name": "Saanich 222 Towing","phone": "250-250-2222"}' | http POST :5009/api/v1/impound_lot_operators authorization:"${ADMIN_TOKEN}"``
    Given An admin token HTTP POST request expecting response 405 from /api/v1/impound_lot_operators with payload {"city": "Saanich","id": "4CC0B2D5-7882-50E6-79E7-3C3AEAA22222","lot_address": "22222 Saanich Road","name": "Saanich 222 Towing","phone": "250-250-2222"}
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


#  _____     _______ _____ _    _
# |  __ \ /\|__   __/ ____| |  | |
# | |__) /  \  | | | |    | |__| |
# |  ___/ /\ \ | | | |    |  __  |
# | |  / ____ \| | | |____| |  | |
# |_| /_/    \_\_|  \_____|_|  |_|

Update an impound lot operator without authentication returns authorization error
    [Tags]  impound lot operators  PATCH  happy
    [Documentation]  HTTP PATCH: update an impound lot operator (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/impound_lot_operators', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/impound_lot_operators.py
    ...
    ...              Example manual call: ``$ echo '{"city":"Chilliwack2"}' | http PATCH :5009/api/v1/impound_lot_operators/4CC0B2D5-7882-50E6-79E7-3C3AEAA36485``
    Given An unauthenticated HTTP PATCH request expecting response 401 from /api/v1/impound_lot_operators/4CC0B2D5-7882-50E6-79E7-3C3AEAA36485 with payload {"city":"Chilliwack2"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Update an impound lot operator with basic auth returns authorization error
    [Tags]  impound lot operators  PATCH  happy
    [Documentation]  HTTP PATCH: update an impound lot operator (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/impound_lot_operators', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/impound_lot_operators.py
    ...
    ...              Example manual call: ``$ echo '{"city":"Chilliwack2"}' | http PATCH :5009/api/v1/impound_lot_operators/4CC0B2D5-7882-50E6-79E7-3C3AEAA36485 --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP PATCH request expecting response 401 from /api/v1/impound_lot_operators/4CC0B2D5-7882-50E6-79E7-3C3AEAA36485 with payload {"city":"Chilliwack2"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Update an impound lot operator with officer token returns authorization error
    [Tags]  impound lot operators  PATCH  happy
    [Documentation]  HTTP PATCH: update an impound lot operator (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/impound_lot_operators', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/impound_lot_operators.py
    ...
    ...              Example manual call: ``$ echo '{"city":"Chilliwack2"}' | http PATCH :5009/api/v1/impound_lot_operators/4CC0B2D5-7882-50E6-79E7-3C3AEAA36485 authorization:"${ADMIN_TOKEN}"``
    Given An officer token HTTP PATCH request expecting response 401 from /api/v1/impound_lot_operators/4CC0B2D5-7882-50E6-79E7-3C3AEAA36485 with payload {"city":"Chilliwack2"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Update an impound lot operator with admin token is not implemented
    [Tags]  impound lot operators  PATCH  happy
    [Documentation]  HTTP PATCH: update an impound lot operator (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/impound_lot_operators', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/impound_lot_operators.py
    ...
    ...              Example manual call: ``$ echo '{"city":"Chilliwack2"}' | http PATCH :5009/api/v1/impound_lot_operators/4CC0B2D5-7882-50E6-79E7-3C3AEAA36485 authorization:"${ADMIN_TOKEN}"``
    Given An admin token HTTP PATCH request expecting response 405 from /api/v1/impound_lot_operators/4CC0B2D5-7882-50E6-79E7-3C3AEAA36485 with payload {"city":"Chilliwack2"}
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


#  _    _ ______          _____
# | |  | |  ____|   /\   |  __ \
# | |__| | |__     /  \  | |  | |
# |  __  |  __|   / /\ \ | |  | |
# | |  | | |____ / ____ \| |__| |
# |_|  |_|______/_/    \_\_____/

Get all impound lot operators headers
    [Tags]  impound lot operators  HEAD  happy
    [Documentation]  HTTP HEAD
    ...
    ...              An HTTP HEAD request is expected to return the HTTP headers for a request
    ...              without a body.
    ...
    ...              Example manual call: ``$ http HEAD :5009/api/v1/impound_lot_operators``
    Given An unauthenticated HTTP HEAD request to /api/v1/impound_lot_operators
    And Response code is HTTP  200
    And Response body should be empty
    And Response Access-Control-Allow-Origin header should contain value *
    And Response Content-Type header should contain value application/json


Get impound lot operator headers
    [Tags]  impound lot operators  HEAD  happy
    [Documentation]  HTTP HEAD
    ...
    ...              An HTTP HEAD request is expected to return the HTTP headers for a request
    ...              without a body.
    ...
    ...              Example manual call: ``$ http HEAD :5009/api/v1/impound_lot_operators/3D8CAB0C-5708-336F-05DF-8B8FB6492ED4``
    Given An unauthenticated HTTP HEAD request to /api/v1/impound_lot_operators/3D8CAB0C-5708-336F-05DF-8B8FB6492ED4
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

Get all impound lot operators options
    [Tags]  impound lot operators  OPTIONS  happy
    [Documentation]  HTTP OPTIONS
    ...
    ...              An HTTP OPTIONS request is expected to return a list of supported HTTP methods
    ...              for an endpoint (eg. GET, POST, PATCH, DELETE, HEAD, OPTIONS).
    ...
    ...             Example manual call: ``$ http OPTIONS :5009/api/v1/impound_lot_operators``
    Given An unauthenticated HTTP OPTIONS request to /api/v1/impound_lot_operators
    Then Response code is HTTP  200
    And Response Allow header should contain value GET
    And Response Allow header should contain value POST
    And Response Allow header should contain value PATCH
    And Response Allow header should contain value HEAD
    And Response Allow header should contain value OPTIONS
    And Response Allow header should not contain value DELETE
    And Response Allow header should not contain value PUT


Get impound lot operator options
    [Tags]  impound lot operators  OPTIONS  happy
    [Documentation]  HTTP OPTIONS
    ...
    ...              An HTTP OPTIONS request is expected to return a list of supported HTTP methods
    ...              for an endpoint (eg. GET, POST, PATCH, DELETE, HEAD, OPTIONS).
    ...
    ...             Example manual call: ``$ http OPTIONS :5009/api/v1/impound_lot_operators/3D8CAB0C-5708-336F-05DF-8B8FB6492ED4``
    Given An unauthenticated HTTP OPTIONS request to /api/v1/impound_lot_operators/3D8CAB0C-5708-336F-05DF-8B8FB6492ED4
    Then Response code is HTTP  200
    And Response Allow header should contain value GET
    And Response Allow header should contain value POST
    And Response Allow header should contain value PATCH
    And Response Allow header should contain value HEAD
    And Response Allow header should contain value OPTIONS
    And Response Allow header should not contain value DELETE
    And Response Allow header should not contain value PUT
