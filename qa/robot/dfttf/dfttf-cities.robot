# Digital Forms 12/24 web service tests

# =======================================================================================
#   _____ _ _   _
#  / ____(_) | (_)
# | |     _| |_ _  ___  ___
# | |    | | __| |/ _ \/ __|
# | |____| | |_| |  __/\__ \
#  \_____|_|\__|_|\___||___/
#
# Tests for the /api/v1/cities endpoints in 12/24 web service
# =======================================================================================

*** Settings ***


Documentation  Digital Forms 12/24 web service test suite for the ``/api/v1/cities`` endpoints and methods.
...
...            See current implementation in DFTTF source code (2021-12-22):
...            https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/cities.py
...            
...            To validate the city list by hand, compare it to the municipality table in the MRE 
...            See wiki for details: https://justice.gov.bc.ca/wiki/display/REOS/MRE+municipality+table
...            Compare it to the MRE database municipality table (MRE_CA.dbo.municipality). Column edesc is 
...            char(79), 1200 rows, as of MRE 399.
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

Get all cities with no authentication
    [Tags]           cities  GET  unauthenticated
    [Documentation]  HTTP GET
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/cities', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/cities.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/cities``
    Given An unauthenticated HTTP GET request to /api/v1/cities
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Every record should be 3 to 29 characters long
    And Each item in the response should use ASCII encoding
    And Each item in the response should have no leading or trailing spaces
    And Response should have at least 1100 records
    And There should be no duplicate values in the response payload


Get all cities with authentication should return same results as with no authentication
    [Tags]           cities  GET  authenticated
    [Documentation]  HTTP GET
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/cities', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/cities.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/cities``
    Given An authenticated HTTP GET request to /api/v1/cities
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response should be identical to the last unauthenticated request


Get all cities with officer token should return same results as with no authentication
    [Tags]           cities  GET  authenticated
    [Documentation]  HTTP GET
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/cities', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/cities.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/cities``
    Given An officer token HTTP GET request to /api/v1/cities
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response should be identical to the last unauthenticated request


Get all cities with admin token should return same results as with no authentication
    [Tags]           cities  GET  authenticated
    [Documentation]  HTTP GET
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/cities', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/cities.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/cities``
    Given An admin token HTTP GET request to /api/v1/cities
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response should be identical to the last unauthenticated request


Get one city without authentication is not implemented
    [Tags]  cities  GET
    [Documentation]  HTTP GET: just  one city (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/cities/<string:city_id>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/cities.py
    ...
    ...              Example manual call: ``$ http POST :5009/api/v1/cities/Saanich``
    Given An unauthenticated HTTP GET request expecting response 405 from /api/v1/cities/Saanich
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Get one city with basic auth is not implemented
    [Tags]  cities  GET
    [Documentation]  HTTP GET: just  one city (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/cities/<string:city_id>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/cities.py
    ...
    ...              Example manual call: ``$ http POST :5009/api/v1/cities/Saanich``
    Given An authenticated HTTP GET request expecting response 405 from /api/v1/cities/Saanich
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Get one city with officer token is not implemented
    [Tags]  cities  GET
    [Documentation]  HTTP GET: just  one city (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/cities/<string:city_id>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/cities.py
    ...
    ...              Example manual call: ``$ http POST :5009/api/v1/cities/Saanich --authorization:"${OFFICER_TOKEN}``
    Given An officer token HTTP GET request expecting response 405 from /api/v1/cities/Saanich
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Get one city with admin token is not implemented
    [Tags]  cities  GET 
    [Documentation]  HTTP GET: just  one city (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/cities/<string:city_id>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/cities.py
    ...
    ...              Example manual call: ``$ http POST :5009/api/v1/cities/Saanich --authorization:"${ADMIN_TOKEN}``
    Given An admin token HTTP GET request expecting response 405 from /api/v1/cities/Saanich
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


#  _____   ____   _____ _______
# |  __ \ / __ \ / ____|__   __|
# | |__) | |  | | (___    | |
# |  ___/| |  | |\___ \   | |
# | |    | |__| |____) |  | |
# |_|     \____/|_____/   |_|

Create a city without authentication or token returns authorization error
    [Tags]  cities  POST  unhappy
    [Documentation]  HTTP POST: add a city (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/cities', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/cities.py
    ...
    ...              Example manual call: ``$ echo '{"1234","TEST POLICE"}' | http POST :5009/api/v1/cities``
    Given An unauthenticated HTTP POST request expecting response 401 from /api/v1/cities with payload {"Saanich 2"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create a city with basic authentication returns authorization error
    [Tags]  cities  POST  unhappy
    [Documentation]  HTTP POST: add a city (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/cities', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/cities.py
    ...
    ...              Example manual call: ``$ echo '{"Saanich 2"}' | http POST :5009/api/v1/cities --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP POST request expecting response 401 from /api/v1/cities with payload {"Saanich 2"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create a city with officer token returns authorization error
    [Tags]  cities  POST  unhappy
    [Documentation]  HTTP POST: add a city (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/cities', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/cities.py
    ...
    ...              Example manual call: ``$ echo '{"Saanich 2"}' | http POST :5009/api/v1/cities authorization:"${OFFICER_TOKEN}"``
    Given An officer token HTTP POST request expecting response 401 from /api/v1/cities with payload {"Saanich 2"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create a city with admin token not implemented
    [Tags]  cities  POST  happy
    [Documentation]  HTTP POST: add a city (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/cities', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/cities.py
    ...
    ...              Example manual call: ``$ echo '{"Saanich 2"}' | http POST :5009/api/v1/cities authorization:"${ADMIN_TOKEN}"``
    Given An admin token HTTP POST request expecting response 405 from /api/v1/cities with payload {"Saanich 2"}
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


#  _____     _______ _____ _    _
# |  __ \ /\|__   __/ ____| |  | |
# | |__) /  \  | | | |    | |__| |
# |  ___/ /\ \ | | | |    |  __  |
# | |  / ____ \| | | |____| |  | |
# |_| /_/    \_\_|  \_____|_|  |_|

Update a city without authentication returns authorization error
    [Tags]  cities  PATCH  happy
    [Documentation]  HTTP PATCH: update an city (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/cities', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/cities.py
    ...
    ...              Example manual call: ``$ echo '{"RSI", "Road Safety Initiative"}' | http PATCH :5009/api/v1/cities``
    Given An unauthenticated HTTP PATCH request expecting response 401 from /api/v1/cities/DE with payload {"RSI","Road Safety Initiative"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Update a city with basic auth returns authorization error
    [Tags]  cities  PATCH  happy
    [Documentation]  HTTP PATCH: update an city (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/cities', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/cities.py
    ...
    ...              Example manual call: ``$ echo '{"RSI", "Road Safety Initiative"}' | http PATCH :5009/api/v1/cities --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP PATCH request expecting response 401 from /api/v1/cities/DE with payload {"RSI","Road Safety Initiative"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Update a city with officer token returns authorization error
    [Tags]  cities  PATCH  happy
    [Documentation]  HTTP PATCH: update an city (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/cities', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/cities.py
    ...
    ...              Example manual call: ``$ echo '{"RSI", "Road Safety Initiative"}' | http PATCH :5009/api/v1/cities authorization:"${ADMIN_TOKEN}"``
    Given An officer token HTTP PATCH request expecting response 401 from /api/v1/cities/Saanich with payload {"RSI","Road Safety Initiative"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Update a city with admin token is not implemented
    [Tags]  cities  PATCH  happy
    [Documentation]  HTTP PATCH: update an city (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/cities', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/cities.py
    ...
    ...              Example manual call: ``$ echo '{"RSI", "Road Safety Initiative"}' | http PATCH :5009/api/v1/cities authorization:"${ADMIN_TOKEN}"``
    Given An admin token HTTP PATCH request expecting response 405 from /api/v1/cities/Saanich with payload {"RSI","Road Safety Initiative"}
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


#  _    _ ______          _____
# | |  | |  ____|   /\   |  __ \
# | |__| | |__     /  \  | |  | |
# |  __  |  __|   / /\ \ | |  | |
# | |  | | |____ / ____ \| |__| |
# |_|  |_|______/_/    \_\_____/

Get all cities headers
    [Tags]  cities  HEAD  happy
    [Documentation]  HTTP HEAD
    ...
    ...              An HTTP HEAD request is expected to return the HTTP headers for a request
    ...              without a body.
    ...
    ...              Example manual call: ``$ http HEAD :5009/api/v1/cities``
    Given An unauthenticated HTTP HEAD request to /api/v1/cities
    And Response code is HTTP  200
    And Response body should be empty
    And Response Access-Control-Allow-Origin header should contain value *
    And Response Content-Type header should contain value application/json


Get city headers
    [Tags]  cities  HEAD  happy
    [Documentation]  HTTP HEAD
    ...
    ...              An HTTP HEAD request is expected to return the HTTP headers for a request
    ...              without a body.
    ...
    ...              Example manual call: ``$ http HEAD :5009/api/v1/cities/Saanich``
    Given An unauthenticated HTTP HEAD request to /api/v1/cities/Saanich
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

Get all cities options
    [Tags]  cities  OPTIONS  happy
    [Documentation]  HTTP OPTIONS
    ...
    ...              An HTTP OPTIONS request is expected to return a list of supported HTTP methods
    ...              for an endpoint (eg. GET, POST, PATCH, DELETE, HEAD, OPTIONS).
    ...
    ...             Example manual call: ``$ http OPTIONS :5009/api/v1/cities``
    Given An unauthenticated HTTP OPTIONS request to /api/v1/cities
    Then Response code is HTTP  200
    And Response Allow header should contain value GET
    And Response Allow header should contain value POST
    And Response Allow header should contain value PATCH
    And Response Allow header should contain value HEAD
    And Response Allow header should contain value OPTIONS
    And Response Allow header should not contain value DELETE
    And Response Allow header should not contain value PUT


Get city options
    [Tags]  cities  OPTIONS  happy
    [Documentation]  HTTP OPTIONS
    ...
    ...              An HTTP OPTIONS request is expected to return a list of supported HTTP methods
    ...              for an endpoint (eg. GET, POST, PATCH, DELETE, HEAD, OPTIONS).
    ...
    ...             Example manual call: ``$ http OPTIONS :5009/api/v1/cities/Saanich``
    Given An unauthenticated HTTP OPTIONS request to /api/v1/cities/Saanich
    Then Response code is HTTP  200
    And Response Allow header should contain value GET
    And Response Allow header should contain value POST
    And Response Allow header should contain value PATCH
    And Response Allow header should contain value HEAD
    And Response Allow header should contain value OPTIONS
    And Response Allow header should not contain value DELETE
    And Response Allow header should not contain value PUT
