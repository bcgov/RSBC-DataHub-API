# Digital Forms 12/24 web service tests

# =======================================================================================
#   _____                  _        _
#  / ____|                | |      (_)
# | |     ___  _   _ _ __ | |_ _ __ _  ___  ___
# | |    / _ \| | | | '_ \| __| '__| |/ _ \/ __|
# | |___| (_) | |_| | | | | |_| |  | |  __/\__ \
#  \_____\___/ \__,_|_| |_|\__|_|  |_|\___||___/
#
# Tests for the /api/v1/colors endpoints in 12/24 web service
# =======================================================================================

*** Settings ***


Documentation  Digital Forms 12/24 web service test suite for the ``/api/v1/countries`` endpoints and methods.
...
...            See current implementation in DFTTF source code (2021-12-22):
...            https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/colors.py
...            
...            There is no 'countries' table in the MRE.
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

Get all countries with no authentication
    [Tags]           countries  GET  unauthenticated
    [Documentation]  HTTP GET
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/countries', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/countries.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/countries``
    Given An unauthenticated HTTP GET request to /api/v1/countries
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Every record should have 4 subrecords
    And Each item in the response should use ASCII encoding
    And Each item in the response should have no leading or trailing spaces
    # TODO (requires JSON wrangling): And There should be no duplicate values in the response payload
    And Response should have at least 3 records


Get all countries with authentication should return same results as with no authentication
    [Tags]           countries  GET  authenticated
    [Documentation]  HTTP GET
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/countries', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/countries.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/countries``
    Given An authenticated HTTP GET request to /api/v1/countries
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response should be identical to the last unauthenticated request


Get all countries with officer token should return same results as with no authentication
    [Tags]           countries  GET  authenticated
    [Documentation]  HTTP GET
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/countries', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/countries.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/countries``
    Given An officer token HTTP GET request to /api/v1/countries
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response should be identical to the last unauthenticated request


Get all countries with admin token should return same results as with no authentication
    [Tags]           countries  GET  authenticated
    [Documentation]  HTTP GET
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/countries', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/countries.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/countries``
    Given An admin token HTTP GET request to /api/v1/countries
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response should be identical to the last unauthenticated request


Get one country without authentication is not implemented
    [Tags]  countries  GET
    [Documentation]  HTTP GET: just  one country (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/countries/<string:country_id>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/countries.py
    ...
    ...              Example manual call: ``$ http POST :5009/api/v1/countries/MEX``
    Given An unauthenticated HTTP GET request expecting response 405 from /api/v1/countries/MEX
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Get one country with basic auth is not implemented
    [Tags]  countries  GET
    [Documentation]  HTTP GET: just  one country (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/countries/<string:country_id>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/countries.py
    ...
    ...              Example manual call: ``$ http POST :5009/api/v1/countries/MEX``
    Given An authenticated HTTP GET request expecting response 405 from /api/v1/countries/MEX
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Get one country with officer token is not implemented
    [Tags]  countries  GET
    [Documentation]  HTTP GET: just  one country (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/countries/<string:country_id>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/countries.py
    ...
    ...              Example manual call: ``$ http POST :5009/api/v1/countries/MEX --authorization:"${OFFICER_TOKEN}``
    Given An officer token HTTP GET request expecting response 405 from /api/v1/countries/MEX
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Get one country with admin token is not implemented
    [Tags]  countries  GET 
    [Documentation]  HTTP GET: just  one country (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/countries/<string:country_id>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/countries.py
    ...
    ...              Example manual call: ``$ http POST :5009/api/v1/countries/MEX --authorization:"${ADMIN_TOKEN}``
    Given An admin token HTTP GET request expecting response 405 from /api/v1/countries/MEX
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


#  _____   ____   _____ _______
# |  __ \ / __ \ / ____|__   __|
# | |__) | |  | | (___    | |
# |  ___/| |  | |\___ \   | |
# | |    | |__| |____) |  | |
# |_|     \____/|_____/   |_|

Create a country without authentication or token returns authorization error
    [Tags]  countries  POST  unhappy
    [Documentation]  HTTP POST: add a country (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/countries', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/countries.py
    ...
    ...              Example manual call: ``$ echo '{"1234","TEST POLICE"}' | http POST :5009/api/v1/countries``
    Given An unauthenticated HTTP POST request expecting response 401 from /api/v1/countries with payload {"activeYN":"Y","internalYN":null,"objectCd":"DEU","objectDsc":"Germany"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create a country with basic authentication returns authorization error
    [Tags]  countries  POST  unhappy
    [Documentation]  HTTP POST: add a country (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/countries', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/countries.py
    ...
    ...              Example manual call: ``$ echo '{"activeYN":"Y","internalYN":null,"objectCd":"DEU","objectDsc":"Germany"}' | http POST :5009/api/v1/countries --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP POST request expecting response 401 from /api/v1/countries with payload {"activeYN":"Y","internalYN":null,"objectCd":"DEU","objectDsc":"Germany"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create a country with officer token returns authorization error
    [Tags]  countries  POST  unhappy
    [Documentation]  HTTP POST: add a country (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint returns HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/countries', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/countries.py
    ...
    ...              Example manual call: ``$ echo '{"activeYN":"Y","internalYN":null,"objectCd":"DEU","objectDsc":"Germany"}' | http POST :5009/api/v1/countries authorization:"${OFFICER_TOKEN}"``
    Given An officer token HTTP POST request expecting response 401 from /api/v1/countries with payload {"activeYN":"Y","internalYN":null,"objectCd":"DEU","objectDsc":"Germany"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create a country with admin token not implemented
    [Tags]  countries  POST  happy
    [Documentation]  HTTP POST: add a country (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/countries', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/countries.py
    ...
    ...              Example manual call: ``$ echo '{"activeYN":"Y","internalYN":null,"objectCd":"DEU","objectDsc":"Germany"}' | http POST :5009/api/v1/countries authorization:"${ADMIN_TOKEN}"``
    Given An admin token HTTP POST request expecting response 405 from /api/v1/countries with payload {"activeYN":"Y","internalYN":null,"objectCd":"DEU","objectDsc":"Germany"}
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


#  _____     _______ _____ _    _
# |  __ \ /\|__   __/ ____| |  | |
# | |__) /  \  | | | |    | |__| |
# |  ___/ /\ \ | | | |    |  __  |
# | |  / ____ \| | | |____| |  | |
# |_| /_/    \_\_|  \_____|_|  |_|

Update a country without authentication returns authorization error
    [Tags]  countries  PATCH  happy
    [Documentation]  HTTP PATCH: update a country (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/countries', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/countries.py
    ...
    ...              Example manual call: ``$ echo '{"activeYN":"Y","internalYN":null,"objectCd":"OTH","objectDsc":"Other Country"}' | http PATCH :5009/api/v1/countries/OTH``
    Given An unauthenticated HTTP PATCH request expecting response 401 from /api/v1/countries/OTH with payload {"activeYN":"Y","internalYN":null,"objectCd":"OTH","objectDsc":"Other Country"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Update a country with basic auth returns authorization error
    [Tags]  countries  PATCH  happy
    [Documentation]  HTTP PATCH: update a country (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/countries', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/countries.py
    ...
    ...              Example manual call: ``$ echo '{"activeYN":"Y","internalYN":null,"objectCd":"OTH","objectDsc":"Other Country"}' | http PATCH :5009/api/v1/countries/OTH --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP PATCH request expecting response 401 from /api/v1/countries/OTH with payload {"activeYN":"Y","internalYN":null,"objectCd":"OTH","objectDsc":"Other Country"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


Update a country with officer token returns authorization error
    [Tags]  countries  PATCH  happy
    [Documentation]  HTTP PATCH: update a country (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/countries', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/countries.py
    ...
    ...              Example manual call: ``$ echo '{"activeYN":"Y","internalYN":null,"objectCd":"OTH","objectDsc":"Other Country"}' | http PATCH :5009/api/v1/countries/OTH authorization:"${ADMIN_TOKEN}"``
    Given An officer token HTTP PATCH request expecting response 401 from /api/v1/countries/OTH with payload {"activeYN":"Y","internalYN":null,"objectCd":"OTH","objectDsc":"Other Country"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Update a country with admin token is not implemented
    [Tags]  countries  PATCH  happy
    [Documentation]  HTTP PATCH: update a country (not implemented) 
    ...
    ...              *Should* be available with or without authentication or token.
    ...
    ...              As of December 2021, endpoint responds with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/countries', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/countries.py
    ...
    ...              Example manual call: ``$ echo '{"activeYN":"Y","internalYN":null,"objectCd":"OTH","objectDsc":"Other Country"}' | http PATCH :5009/api/v1/countries/OTH authorization:"${ADMIN_TOKEN}"``
    Given An admin token HTTP PATCH request expecting response 405 from /api/v1/countries/OTH with payload {"activeYN":"Y","internalYN":null,"objectCd":"OTH","objectDsc":"Other Country"}
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


#  _    _ ______          _____
# | |  | |  ____|   /\   |  __ \
# | |__| | |__     /  \  | |  | |
# |  __  |  __|   / /\ \ | |  | |
# | |  | | |____ / ____ \| |__| |
# |_|  |_|______/_/    \_\_____/

Get all countries headers
    [Tags]  countries  HEAD  happy
    [Documentation]  HTTP HEAD
    ...
    ...              An HTTP HEAD request is expected to return the HTTP headers for a request
    ...              without a body.
    ...
    ...              Example manual call: ``$ http HEAD :5009/api/v1/countries``
    Given An unauthenticated HTTP HEAD request to /api/v1/countries
    And Response code is HTTP  200
    And Response body should be empty
    And Response Access-Control-Allow-Origin header should contain value *
    And Response Content-Type header should contain value application/json


Get country headers
    [Tags]  countries  HEAD  happy
    [Documentation]  HTTP HEAD
    ...
    ...              An HTTP HEAD request is expected to return the HTTP headers for a request
    ...              without a body.
    ...
    ...              Example manual call: ``$ http HEAD :5009/api/v1/countries/USA``
    Given An unauthenticated HTTP HEAD request to /api/v1/countries/USA
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

Get all countries options
    [Tags]  countries  OPTIONS  happy
    [Documentation]  HTTP OPTIONS
    ...
    ...              An HTTP OPTIONS request is expected to return a list of supported HTTP methods
    ...              for an endpoint (eg. GET, POST, PATCH, DELETE, HEAD, OPTIONS).
    ...
    ...             Example manual call: ``$ http OPTIONS :5009/api/v1/countries``
    Given An unauthenticated HTTP OPTIONS request to /api/v1/countries
    Then Response code is HTTP  200
    And Response Allow header should contain value GET
    And Response Allow header should contain value POST
    And Response Allow header should contain value PATCH
    And Response Allow header should contain value HEAD
    And Response Allow header should contain value OPTIONS
    And Response Allow header should not contain value DELETE
    And Response Allow header should not contain value PUT


Get country options
    [Tags]  countries  OPTIONS  happy
    [Documentation]  HTTP OPTIONS
    ...
    ...              An HTTP OPTIONS request is expected to return a list of supported HTTP methods
    ...              for an endpoint (eg. GET, POST, PATCH, DELETE, HEAD, OPTIONS).
    ...
    ...             Example manual call: ``$ http OPTIONS :5009/api/v1/countries/USA``
    Given An unauthenticated HTTP OPTIONS request to /api/v1/countries/USA
    Then Response code is HTTP  200
    And Response Allow header should contain value GET
    And Response Allow header should contain value POST
    And Response Allow header should contain value PATCH
    And Response Allow header should contain value HEAD
    And Response Allow header should contain value OPTIONS
    And Response Allow header should not contain value DELETE
    And Response Allow header should not contain value PUT
