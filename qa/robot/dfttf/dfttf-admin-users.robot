# Digital Forms 12/24 web service tests

# =======================================================================================
#              _           _         _    _
#     /\      | |         (_)       | |  | |
#    /  \   __| |_ __ ___  _ _ __   | |  | |___  ___ _ __ ___
#   / /\ \ / _` | '_ ` _ \| | '_ \  | |  | / __|/ _ \ '__/ __|
#  / ____ \ (_| | | | | | | | | | | | |__| \__ \  __/ |  \__ \
# /_/    \_\__,_|_| |_| |_|_|_| |_|  \____/|___/\___|_|  |___/
#
# Tests for the /api/v1/admin/users endpoints in 12/24 web service
# =======================================================================================

*** Settings ***


Documentation  Digital Forms 12/24 web service test suite for the ``/api/v1/admin_user_roles`` endpoints and methods.
...
...            See current implementation in DFTTF source code (2021-12-22):
...            https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
...            
...            The test documentation for the endpoints at: https://justice.gov.bc.ca/wiki/pages/viewpage.action?pageId=314671737
...
...
...            For permissions given to each user type, see:
...            https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/data/permissions.json



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
 
Get users without authentication returns error
    [Tags]           admin users  GET  unauthenticated  unhappy
    [Documentation]  HTTP GET
    ... 
    ...              *Should not* be accessible without admin token.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet).\n
    ...              Python line in DFTTF source: ``@bp.route('/users', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_users.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/users authorization:"${OFFICER_TOKEN}"``
    Given An unauthenticated HTTP GET request expecting response 401 from /api/v1/admin/users
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Get users with basic auth returns error
    [Tags]           admin users  GET  unauthenticated  unhappy
    [Documentation]  HTTP GET
    ... 
    ...              *Should not* be accessible without admin token.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet).\n
    ...              Python line in DFTTF source: ``@bp.route('/users', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_users.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/users --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP GET request expecting response 401 from /api/v1/admin/users
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Get users with officer token returns error
    [Tags]           admin users  GET  unauthenticated  unhappy
    [Documentation]  HTTP GET
    ... 
    ...              *Should not* be accessible without admin token.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet).\n
    ...              Python line in DFTTF source: ``@bp.route('/users', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_users.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/users authorization:"${OFFICER_TOKEN}" ``
    Given An officer token HTTP GET request expecting response 401 from /api/v1/admin/users
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Get users with admin token returns users
    [Tags]           admin users  GET  authenticated  happy
    [Documentation]  HTTP GET
    ... 
    ...              *Should not* be accessible without admin token.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet).\n
    ...              Python line in DFTTF source: ``@bp.route('/users', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_users.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/users authorization:"${ADMIN_TOKEN}" ``
    Given An admin token HTTP GET request to /api/v1/admin/users
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Each item in the response should use ASCII encoding
    And Each item in the response should have no leading or trailing spaces
    And Response should have at least 2 records
    And Response should include text  "approved_dt":
    And Response should include text  "role_name":
    And Response should include text  "submitted_dt":
    And Response should include text  "username":"jonathan-longe@github"
    And Response should include text  "username":"jolonge@idir"


Get individual user without authentication returns error
    [Tags]           admin users  GET  unauthenticated  unhappy
    [Documentation]  HTTP GET
    ... 
    ...              *Should not* be accessible without admin token.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet).\n
    ...              Python line in DFTTF source: ``@bp.route('/users/<string:username>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_users.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/users authorization:"${ADMIN_TOKEN}" ``
    Given An unauthenticated HTTP GET request expecting response 401 from /api/v1/admin/users/${DFTTF_ADMIN_USER}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Get individual user with basic authentication returns error
    [Tags]           admin users  GET  unauthenticated  unhappy
    [Documentation]  HTTP GET
    ... 
    ...              *Should not* be accessible without admin token.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet).\n
    ...              Python line in DFTTF source: ``@bp.route('/users/<string:username>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_users.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/users --auth ${USERNAME}:${PASSWORD}" ``
    Given An authenticated HTTP GET request expecting response 401 from /api/v1/admin/users/${DFTTF_ADMIN_USER}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Get individual user with officer token returns error
    [Tags]           admin users  GET  unauthenticated  unhappy
    [Documentation]  HTTP GET
    ... 
    ...              *Should not* be accessible without admin token.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet).\n
    ...              Python line in DFTTF source: ``@bp.route('/users/<string:username>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_users.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/users authorization:"${OFFICERTOKEN}" ``
    Given An officer token HTTP GET request expecting response 401 from /api/v1/admin/users/${DFTTF_ADMIN_USER}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Get individual user with admin token not implemented
    [Tags]           admin users  GET  authenticated  happy
    [Documentation]  HTTP GET
    ... 
    ...              *Should not* be accessible without admin token.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet).\n
    ...              Python line in DFTTF source: ``@bp.route('/users/<string:username>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_users.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/users authorization:"${ADMIN_TOKEN}" ``
    Given An admin token HTTP GET request expecting response 405 from /api/v1/admin/users/${DFTTF_ADMIN_USER}
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


#  _____   ____   _____ _______
# |  __ \ / __ \ / ____|__   __|
# | |__) | |  | | (___    | |
# |  ___/| |  | |\___ \   | |
# | |    | |__| |____) |  | |
# |_|     \____/|_____/   |_|

Create user without authentication returns error
    [Tags]           admin users  POST  unauthenticated  unhappy
    [Documentation]  HTTP POST
    ...
    ...              *Should not* be accessible without authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"hi":"there","username":"abc"}' | http POST :5009/api/v1/admin/users``
    Given An unauthenticated HTTP POST request expecting response 401 from /api/v1/admin/users with payload {"hi":"there","username":"abc"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create user with basic auth returns error
    [Tags]           admin users  POST  unauthenticated  unhappy
    [Documentation]  HTTP POST
    ...
    ...              *Should not* be accessible without authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"hi":"there","username":"abc"}' | http POST :5009/api/v1/admin/users --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP POST request expecting response 401 from /api/v1/admin/users with payload {"hi":"there","username":"abc"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create user with officer token returns error
    [Tags]           admin users  POST  unauthenticated  unhappy
    [Documentation]  HTTP POST
    ...
    ...              *Should not* be accessible without authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"hi":"there","username":"abc"}' | http POST :5009/api/v1/admin/users authorization:"${ADMIN_TOKEN}"``
    Given An officer token HTTP POST request expecting response 401 from /api/v1/admin/users with payload {"hi":"there","username":"abc"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create user with admin token not implemented
    [Tags]           admin users  POST  authenticated  happy
    [Documentation]  HTTP POST
    ...
    ...              *Should not* be accessible without authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"hi":"there","username":"abc"}' | http POST :5009/api/v1/admin/users authorization:"${ADMIN_TOKEN}"``
    Given An admin token HTTP POST request expecting response 405 from /api/v1/admin/users with payload {"hi":"there","username":"abc"}
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


#  _____     _______ _____ _    _
# |  __ \ /\|__   __/ ____| |  | |
# | |__) /  \  | | | |    | |__| |
# |  ___/ /\ \ | | | |    |  __  |
# | |  / ____ \| | | |____| |  | |
# |_| /_/    \_\_|  \_____|_|  |_|

Update user without authentication returns error
    [Tags]           admin users  PATCH  unauthenticated  unhappy
    [Documentation]  HTTP PATCH
    ...
    ...              *Should not* be accessible without authentication. This endpoint currently doesn't seem to do anything.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>', methods=['PATCH'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"hi":"there","username":"abc"}' | http PATCH :5009/api/v1/admin/users/george_formby``
    Given An unauthenticated HTTP PATCH request expecting response 401 from /api/v1/admin/users/george_formby with payload {"hi":"there","username":"abc"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Update user with basic auth returns error
    [Tags]           admin users  PATCH  unauthenticated  unhappy
    [Documentation]  HTTP PATCH
    ...
    ...              *Should not* be accessible without authentication. This endpoint currently doesn't seem to do anything.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>', methods=['PATCH'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"hi":"there","username":"abc"}' | http PATCH :5009/api/v1/admin/users/george_formby``
    Given An authenticated HTTP PATCH request expecting response 401 from /api/v1/admin/users/george_formby with payload {"hi":"there","username":"abc"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Update user with officer token returns error
    [Tags]           admin users  PATCH  unauthenticated  unhappy
    [Documentation]  HTTP PATCH
    ...
    ...              *Should not* be accessible without authentication. This endpoint currently doesn't seem to do anything.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>', methods=['PATCH'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"hi":"there","username":"abc"}' | http PATCH :5009/api/v1/admin/users/george_formby``
    Given An officer token HTTP PATCH request expecting response 401 from /api/v1/admin/users/george_formby with payload {"hi":"there","username":"abc"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Update user with admin token returns error
    [Tags]           admin users  PATCH  unauthenticated  unhappy
    [Documentation]  HTTP PATCH
    ...
    ...              *Should not* be accessible without authentication. This endpoint currently doesn't seem to do anything.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>', methods=['PATCH'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"hi":"there","username":"abc"}' | http PATCH :5009/api/v1/admin/users/george_formby``
    Given An admin token HTTP PATCH request expecting response 401 from /api/v1/admin/users/george_formby with payload {"hi":"there","username":"abc"}
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


#  _____  ______ _      ______ _______ ______
# |  __ \|  ____| |    |  ____|__   __|  ____|
# | |  | | |__  | |    | |__     | |  | |__
# | |  | |  __| | |    |  __|    | |  |  __|
# | |__| | |____| |____| |____   | |  | |____
# |_____/|______|______|______|  |_|  |______|

Delete user without authentication returns error
    [Tags]           admin users  DELETE  unauthenticated  unhappy
    [Documentation]  HTTP DELETE
    ...
    ...              *Should* be accessible with authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>', methods=['DELETE'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``http DELETE :5009/api/v1/admin/users/george_formby``
    Given An unauthenticated HTTP DELETE request expecting response 401 from /api/v1/admin/users/george_formby
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Delete user with basic auth returns error
    [Tags]           admin users  DELETE  unauthenticated  unhappy
    [Documentation]  HTTP DELETE
    ...
    ...              *Should* be accessible with authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>', methods=['DELETE'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``http DELETE :5009/api/v1/admin/users/george_formby --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP DELETE request expecting response 401 from /api/v1/admin/users/george_formby
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Delete user with officer token returns error
    [Tags]           admin users  DELETE  unauthenticated  unhappy
    [Documentation]  HTTP DELETE
    ...
    ...              *Should* be accessible with authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>', methods=['DELETE'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``http DELETE :5009/api/v1/admin/users/george_formby authorization:"${OFFICER_TOKEN}"``
    Given An officer token HTTP DELETE request expecting response 401 from /api/v1/admin/users/george_formby
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Delete user with admin token is not implemented
    [Tags]           admin users  DELETE  unauthenticated  unhappy
    [Documentation]  HTTP DELETE
    ...
    ...              *Should* be accessible with authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>', methods=['DELETE'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``http DELETE :5009/api/v1/admin/users/george_formby authorization:"${ADMIN_TOKEN}"``
    Given An officer token HTTP DELETE request expecting response 405 from /api/v1/admin/users/george_formby
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}

    
#  _    _ ______          _____
# | |  | |  ____|   /\   |  __ \
# | |__| | |__     /  \  | |  | |
# |  __  |  __|   / /\ \ | |  | |
# | |  | | |____ / ____ \| |__| |
# |_|  |_|______/_/    \_\_____/

Get user headers without authentication
    [Tags]           admin users  HEAD  unauthenticated  unhappy
    [Documentation]  HTTP HEAD
    ...
    ...              An HTTP HEAD request is expected to return the HTTP headers for a request
    ...              without a body.
    ...
    ...              Example manual call: ```$ http HEAD :5009/api/v1/admin/users/stevefor@idir``
    Given An unauthenticated HTTP HEAD request expecting response 401 from /api/v1/admin/users/${DFTTF_ADMIN_USER}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error":"Unauthorized"}


Get user headers with authentication
    [Tags]           admin users  HEAD  authenticated  happy
    [Documentation]  HTTP HEAD
    ...
    ...              An HTTP HEAD request is expected to return the HTTP headers for a request
    ...              without a body.
    ...
    ...              Example manual call: ``$ http HEAD :5009/api/v1/admin/users/stevefor@idir  --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP HEAD request to /api/v1/admin/users/${DFTTF_ADMIN_USER}
    And Response code is HTTP  200
    And Response body should be empty
    # And headers include ... (insert expected headers here)


#   ____  _____ _______ _____ ____  _   _  _____
#  / __ \|  __ \__   __|_   _/ __ \| \ | |/ ____|
# | |  | | |__) | | |    | || |  | |  \| | (___
# | |  | |  ___/  | |    | || |  | | . ` |\___ \
# | |__| | |      | |   _| || |__| | |\  |____) |
#  \____/|_|      |_|  |_____\____/|_| \_|_____/

Get user options without authentication
    [Tags]           admin users  OPTIONS  unauthenticated  unhappy
    [Documentation]  HTTP OPTIONS: supported methods
    ...
    ...              An HTTP OPTIONS request is expected to return a list of supported HTTP methods
    ...              for an endpoint (eg. POST, GET, OPTIONS, HEAD).
    ...
    ...              Example manual call: ``$ http OPTIONS :5009/api/v1/admin/users/stevefor@idir``
    Given An unauthenticated HTTP OPTIONS request to /api/v1/admin/users/${DFTTF_ADMIN_USER}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error":"Unauthorized"}


Get user options with authentication
    [Tags]           admin users  OPTIONS  authenticated  happy
    [Documentation]  HTTP OPTIONS
    ...
    ...              An HTTP OPTIONS request is expected to return a list of supported HTTP methods
    ...              for an endpoint (eg. POST, GET, OPTIONS, HEAD).
    ...
    ...              Example manual call: ``$ http OPTIONS :5009/api/v1/admin/users/stevefor@idir --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP OPTIONS request to /api/v1/admin/users/${DFTTF_ADMIN_USER}
    Then Response code is HTTP  200
    Response Allow header should contain value GET
    Response Allow header should contain value POST
    Response Allow header should contain value PATCH
    Response Allow header should contain value DELETE
    Response Allow header should contain value HEAD
    Response Allow header should contain value OPTIONS
