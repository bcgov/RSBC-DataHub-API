# Digital Forms 12/24 web service tests

# =======================================================================================
#              _           _         _    _                 _____       _
#     /\      | |         (_)       | |  | |               |  __ \     | |
#    /  \   __| |_ __ ___  _ _ __   | |  | |___  ___ _ __  | |__) |___ | | ___  ___
#   / /\ \ / _` | '_ ` _ \| | '_ \  | |  | / __|/ _ \ '__| |  _  // _ \| |/ _ \/ __|
#  / ____ \ (_| | | | | | | | | | | | |__| \__ \  __/ |    | | \ \ (_) | |  __/\__ \
# /_/    \_\__,_|_| |_| |_|_|_| |_|  \____/|___/\___|_|    |_|  \_\___/|_|\___||___/
#
# Tests for the /api/v1/admin/user/roles endpoints in 12/24 web service
# =======================================================================================

*** Settings ***


Documentation  Digital Forms 12/24 web service test suite for the ``/api/v1/admin_user_roles`` endpoints and methods.
...
...            See current implementation in DFTTF source code (2021-12-22):
...            https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
...            
...            The test documentation for the endpoints at: https://justice.gov.bc.ca/wiki/pages/viewpage.action?pageId=314671737
...
...            User permissions are stored in a static file in git. Two roles are currently officer and administrator.
...            - Officer permissions
...              "forms-create",
...              "forms-get",
...              "forms-update",
...              "driver-get",
...              "vehicle-get",
...              "user_roles-index"
...
...            - Administrator permissions:
...              "admin_user_roles-index",
...              "admin_user_roles-update",
...              "admin_user_roles-delete",
...              "admin_user_roles-create",
...              "admin_users-index"
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
 
Get roles for existing user without admin token returns error
    [Tags]           admin user roles  GET  unauthenticated  unhappy
    [Documentation]  HTTP GET
    ... 
    ...              *Should not* be accessible without admin token.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet).\n
    ...              Python line in DFTTF source: ``@bp.route('/users/<string:username>/roles', methods=['GET']))``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/users/stevef4@github/roles``
    Given An unauthenticated HTTP GET request expecting response 401 from /api/v1/admin/users/${DFTTF_ADMIN_USER}/roles
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Get roles for non-existent user without admin token returns error
    [Tags]           admin user roles  GET  unauthenticated  unhappy
    [Documentation]  HTTP GET
    ... 
    ...              *Should not* be accessible without admin token.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet).\n
    ...              Python line in DFTTF source: ``@bp.route('/users/<string:username>/roles', methods=['GET']))``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/users/rick_moranis/roles``
    Given An unauthenticated HTTP GET request expecting response 401 from /api/v1/admin/users/rick_moranis/roles
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Get roles for existing user with officer token returns error
    [Tags]           admin user roles  GET  unauthenticated  unhappy
    [Documentation]  HTTP GET
    ...
    ...              *Should* be accessible with admin token.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles', methods=['GET']))``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/users/stevef4@github/roles authorization:"${OFFICER_TOKEN}"``
    Given An officer token HTTP GET request expecting response 401 from /api/v1/admin/users/${DFTTF_ADMIN_USER}/roles
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Get roles for existing user with admin token returns roles
    [Tags]           admin user roles  GET  authenticated  happy
    [Documentation]  HTTP GET
    ...
    ...              *Should* be accessible with admin token.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles', methods=['GET']))``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/users/stevef4@github/roles authorization:"${ADMIN_TOKEN}"``
    Given An admin token HTTP GET request to /api/v1/admin/users/${DFTTF_ADMIN_USER}/roles
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Each item in the response should use ASCII encoding
    And Each item in the response should have no leading or trailing spaces
    And Response should have exactly 2 records
    And Response should include text  "approved_dt":
    And Response should include text  "role_name":
    And Response should include text  "submitted_dt":
    And Response should include text  "username":"${DFTTF_ADMIN_USER}"


Get roles for non-existent user with authentication
    [Tags]           admin user roles  GET  authenticated  happy
    [Documentation]  HTTP GET
    ...
    ...              *Should* be accessible with authentication.
    ...           
    ...              An empty array means a user does not exist?
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles', methods=['GET']))``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/users/rick_moranis/roles authorization:"${ADMIN_TOKEN}"``
    Given An admin token HTTP GET request to /api/v1/admin/users/rick_moranis/roles
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Each item in the response should use ASCII encoding
    And Each item in the response should have no leading or trailing spaces
    And Response should have exactly 0 records


Get permissions for a user role without authorization returns error
    [Tags]           admin user roles  GET  unauthenticated  unhappy
    [Documentation]  HTTP GET
    ...
    ...              *Should not* be accessible without authentication?
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles/<string:role_name>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/users/stevef4@github/roles/officer``
    Given An authenticated HTTP GET request expecting response 401 from /api/v1/admin/users/${DFTTF_ADMIN_USER}/roles/officer
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error":"Unauthorized"}


Get permissions for a user role with authentication is not implemented
    [Tags]           admin user roles  GET  authenticated  happy
    [Documentation]  HTTP GET
    ...
    ...              *Should* be accessible with authentication, but is not yet implemented.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles/<string:role_name>', methods=['GET'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/users/stevef4@github/roles/adm authorization:"${ADMIN_TOKEN}"``
    Given An authenticated HTTP GET request expecting response 405 from /api/v1/admin/users/${DFTTF_ADMIN_USER}/roles/officer
    Then Response code is HTTP  405
    And Response content type is  application/json
    And Response body should match  {"error": "method not implemented"}


#  _____   ____   _____ _______
# |  __ \ / __ \ / ____|__   __|
# | |__) | |  | | (___    | |
# |  ___/| |  | |\___ \   | |
# | |    | |__| |____) |  | |
# |_|     \____/|_____/   |_|

Create new user without authentication or token returns authorization error
    [Tags]           admin user roles  POST  unauthenticated  unhappy
    [Documentation]  HTTP POST
    ...
    ...              *Should not* be accessible without authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"role_name":"administrator","requested_username":"tom_lehrer"}' | http POST :5009/api/v1/admin/users/tom_lehrer/roles``
    Given An unauthenticated HTTP POST request expecting response 401 from /api/v1/admin/users/tom_lehrer/roles with payload {"role_name":"administrator","requested_username":"tom_lehrer"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create new user with basic auth returns error
    [Tags]           admin user roles  POST  unauthenticated  unhappy
    [Documentation]  HTTP POST
    ...
    ...              *Should not* be accessible without authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"role_name":"administrator","requested_username":"tim_curry"}' | http POST :5009/api/v1/admin/users/tim_curry/roles --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP POST request expecting response 401 from /api/v1/admin/users/tim_curry/roles with payload {"role_name":"administrator","requested_username":"tim_curry"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create new user with officer token returns error
    [Tags]           admin user roles  POST  unauthenticated  unhappy
    [Documentation]  HTTP POST
    ...
    ...              *Should not* be accessible without admin token.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"role_name":"singer","requested_username":"george_michael"}' | http POST :5009/api/v1/admin/users/george_michael/roles authorization:"${OFFICER_TOKEN}"``
    Given An officer token HTTP POST request expecting response 401 from /api/v1/admin/users/george_michael/roles with payload {"role_name":"singer","requested_username":"george_michael"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Create new user with admin token is successful
    [Tags]           admin user roles  POST  authenticated  happy
    [Documentation]  HTTP POST
    ...
    ...              *Should* be accessible with authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"role_name":"administrator","requested_username":"george_formby"}' | http POST :5009/api/v1/admin/users/george_formby/roles authorization:"${ADMIN_TOKEN}"``
    Given An admin token HTTP POST request to /api/v1/admin/users/george_formby/roles with payload {"role_name":"administrator","requested_username":"george_formby"}
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Each item in the response should use ASCII encoding
    And Each item in the response should have no leading or trailing spaces
    And Response should have exactly 4 records
    And Response should include text  "approved_dt":
    And Response should include text  "role_name":"administrator"
    And Response should include text  "submitted_dt":
    And Response should include text  "username":"george_formby"


Create duplicate user with admin token returns error
    [Tags]           admin user roles  POST  authenticated  unhappy
    [Documentation]  HTTP POST
    ...
    ...              *Should* be accessible with authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"role_name":"administrator","requested_username":"george_formby"}' | http POST :5009/api/v1/admin/users/george_formby/roles authorization:"${ADMIN_TOKEN}"``
    ...              
    ...              Requests to create a duplicate resource should return HTTP 400-level error. Of the available responses, an HTTP 409 CONFLICT
    ...              the most appropriate: seems best. Could also be 422 UNPROCESSABLE ENTITY, but this may not be standard. See:
    ...              - https://www.rfc-editor.org/rfc/rfc7231.html#section-6.5.8  (HTTP 409)
    Given An admin token HTTP POST request expecting response 409 from /api/v1/admin/users/george_formby/roles with payload {"role_name":"administrator","requested_username":"george_formby"}
    Then Response code is HTTP  409
    And Response content type is  application/json
    And Response body should match  {"error": "conflict"}


Create new user second role with admin token is successful
    [Tags]           admin user roles  POST  authenticated  happy
    [Documentation]  HTTP POST
    ...
    ...              *Should* be accessible with authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"role_name":"officer","requested_username":"george_formby"}' | http POST :5009/api/v1/admin/users/george_formby/roles authorization:"${ADMIN_TOKEN}"``
    Given An admin token HTTP POST request to /api/v1/admin/users/george_formby/roles with payload {"role_name":"officer","requested_username":"george_formby"}
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Each item in the response should use ASCII encoding
    And Each item in the response should have no leading or trailing spaces
    And Response should have exactly 4 records
    And Response should include text  "approved_dt":
    And Response should include text  "role_name":"officer"
    And Response should include text  "submitted_dt":
    And Response should include text  "username":"george_formby"
    

Create user using malformed JSON with admin token returns error
    [Tags]           admin user roles  POST  authenticated  unhappy
    [Documentation]  HTTP POST
    ...
    ...              *Should* be accessible with authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles', methods=['POST'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"role_na' | http POST :5009/api/v1/admin/users/george_michael/roles authorization:"${ADMIN_TOKEN}"``
    ...              
    ...              HTTP 403 specification:
    ...              - https://www.rfc-editor.org/rfc/rfc7231.html#section-6.5.3
    Given An admin token HTTP POST request expecting response 403 from /api/v1/admin/users/george_michael/roles with payload {"role_na
    Then Response code is HTTP  403
    And Response content type is  application/json
    And Response body should match  {"error": "missing payload"}


#  _____     _______ _____ _    _
# |  __ \ /\|__   __/ ____| |  | |
# | |__) /  \  | | | |    | |__| |
# |  ___/ /\ \ | | | |    |  __  |
# | |  / ____ \| | | |____| |  | |
# |_| /_/    \_\_|  \_____|_|  |_|

Update role without authentication returns error
    [Tags]           admin user roles  PATCH  unauthenticated  unhappy
    [Documentation]  HTTP PATCH
    ...
    ...              *Should not* be accessible without authentication. This endpoint currently doesn't seem to do anything.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles/<string:role_name>', methods=['PATCH'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"role_name":"officer","requested_username":"george_formby"}' | http PATCH :5009/api/v1/admin/users/george_formby/roles/administrator``
    Given An unauthenticated HTTP PATCH request expecting response 401 from /api/v1/admin/users/george_formby/roles/officer with payload {"role_name":"officer","requested_username":"george_formby"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Update role with basic auth returns error
    [Tags]           admin user roles  PATCH  unauthenticated  unhappy
    [Documentation]  HTTP PATCH
    ...
    ...              *Should not* be accessible without authentication. This endpoint currently doesn't seem to do anything.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles/<string:role_name>', methods=['PATCH'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"role_name":"officer","requested_username":"george_formby"}' | http PATCH :5009/api/v1/admin/users/george_formby/roles/administrator --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP PATCH request expecting response 401 from /api/v1/admin/users/george_formby/roles/officer with payload {"role_name":"officer","requested_username":"george_formby"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Update role with officer token returns error
    [Tags]           admin user roles  PATCH  unauthenticated  unhappy
    [Documentation]  HTTP PATCH
    ...
    ...              *Should not* be accessible without authentication. This endpoint currently doesn't seem to do anything.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles/<string:role_name>', methods=['PATCH'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"role_name":"entertainer","requested_username":"george_formby"}' | http PATCH :5009/api/v1/admin/users/george_formby/roles/administrator authorization:"${OFFICER_TOKEN}"``
    Given An officer token HTTP PATCH request expecting response 401 from /api/v1/admin/users/george_formby/roles/officer with payload {"role_name":"officer","requested_username":"george_formby"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Update role with admin token is successful
    [Tags]           admin user roles  PATCH  authenticated  happy
    [Documentation]  HTTP PATCH
    ...
    ...              *NOTE: This endpoint currently doesn't seem to do anything.*
    ... 
    ...              *Should* be accessible with authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles/<string:role_name>', methods=['PATCH'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``echo '{"role_name":"entertainer","requested_username":"george_formby"}' | http PATCH :5009/api/v1/admin/users/george_formby/roles/administrator authorization:"${ADMIN_TOKEN}"``
    Given An admin token HTTP PATCH request to /api/v1/admin/users/george_formby/roles/officer with payload {"role_name":"officer","requested_username":"george_formby"}
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Each item in the response should use ASCII encoding
    And Each item in the response should have no leading or trailing spaces
    And Response should have exactly 4 records
    And Response should include text  "approved_dt":
    And Response should include text  "role_name":"officer"
    And Response should include text  "submitted_dt":
    And Response should include text  "username":"george_formby"

#  _____  ______ _      ______ _______ ______
# |  __ \|  ____| |    |  ____|__   __|  ____|
# | |  | | |__  | |    | |__     | |  | |__
# | |  | |  __| | |    |  __|    | |  |  __|
# | |__| | |____| |____| |____   | |  | |____
# |_____/|______|______|______|  |_|  |______|

Delete role without authentication returns error
    [Tags]           admin user roles  DELETE  unauthenticated  unhappy
    [Documentation]  HTTP DELETE
    ...
    ...              *Should* be accessible with authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles/<string:role_name>', methods=['DELETE'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``http DELETE :5009/api/v1/admin/users/george_formby/roles/administrator``
    Given An unauthenticated HTTP DELETE request expecting response 401 from /api/v1/admin/users/george_formby/roles/officer
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Delete role with basic authentication returns error
    [Tags]           admin user roles  DELETE  unauthenticated  unhappy
    [Documentation]  HTTP DELETE
    ...
    ...              *Should* be accessible with authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles/<string:role_name>', methods=['DELETE'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``http DELETE :5009/api/v1/admin/users/george_formby/roles/administrator --auth ${USERNAME}:${PASSWORD}``
   Given An authenticated HTTP DELETE request expecting response 401 from /api/v1/admin/users/george_formby/roles/officer
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Delete role with officer token returns error
    [Tags]           admin user roles  DELETE  unauthenticated  unhappy
    [Documentation]  HTTP DELETE
    ...
    ...              *Should* be accessible with authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles/<string:role_name>', methods=['DELETE'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``http DELETE :5009/api/v1/admin/users/george_formby/roles/administrator authorization:"${OFFICER_TOKEN}"``
   Given An officer token HTTP DELETE request expecting response 401 from /api/v1/admin/users/george_formby/roles/officer
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error": "unauthorized"}


Delete role with admin token is successful
    [Tags]           admin user roles  DELETE  authenticated  happy
    [Documentation]  HTTP DELETE
    ...
    ...              *Should* be accessible with authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles/<string:role_name>', methods=['DELETE'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``http DELETE :5009/api/v1/admin/users/george_formby/roles/officer authorization:"${ADMIN_TOKEN}"``
    Given An admin token HTTP DELETE request to /api/v1/admin/users/george_formby/roles/officer
    Then Response code is HTTP  200
    And Response body should match  okay


Delete nonexistent role with admin token returns client error
    [Tags]           admin user roles  DELETE  authenticated  happy
    [Documentation]  HTTP DELETE
    ...
    ...              *Should* be accessible with authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source:  ``@bp.route('/users/<string:username>/roles/<string:role_name>', methods=['DELETE'])``
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_user_roles.py
    ...
    ...              Example manual call: ``http DELETE :5009/api/v1/admin/users/george_formby/roles/officer2 authorization:"${ADMIN_TOKEN}"``
    Given An admin token HTTP DELETE request expecting response 400 from /api/v1/admin/users/george_formby/roles/officer
    Then Response code is HTTP  400
    And Response content type is  text/html
    And Each item in the response should use ASCII encoding
    And Each item in the response should have no leading or trailing spaces


#  _    _ ______          _____
# | |  | |  ____|   /\   |  __ \
# | |__| | |__     /  \  | |  | |
# |  __  |  __|   / /\ \ | |  | |
# | |  | | |____ / ____ \| |__| |
# |_|  |_|______/_/    \_\_____/

Get role headers without authentication
    [Tags]           admin user roles  HEAD  unauthenticated  unhappy
    [Documentation]  HTTP HEAD
    ...
    ...              An HTTP HEAD request is expected to return the HTTP headers for a request
    ...              without a body.
    ...
    ...              Example manual call: ``$ http HEAD :5009/api/v1/admin/users/stevefor@idir/roles``
    Given An unauthenticated HTTP HEAD request expecting response 401 from /api/v1/admin/users/${DFTTF_ADMIN_USER}/roles
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error":"Unauthorized"}


Get role headers with authentication
    [Tags]           admin user roles  HEAD  authenticated  happy
    [Documentation]  HTTP HEAD
    ...
    ...              An HTTP HEAD request is expected to return the HTTP headers for a request
    ...              without a body.
    ...
    ...              Example manual call: ``$ http HEAD :5009/api/v1/admin/users/stevefor@idir/roles  --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP HEAD request to /api/v1/admin/users/${DFTTF_ADMIN_USER}/roles
    And Response code is HTTP  200
    And Response body should be empty
    # And headers include ... (insert expected headers here)


#   ____  _____ _______ _____ ____  _   _  _____
#  / __ \|  __ \__   __|_   _/ __ \| \ | |/ ____|
# | |  | | |__) | | |    | || |  | |  \| | (___
# | |  | |  ___/  | |    | || |  | | . ` |\___ \
# | |__| | |      | |   _| || |__| | |\  |____) |
#  \____/|_|      |_|  |_____\____/|_| \_|_____/

Get admin form options without authentication
    [Tags]           admin user roles  OPTIONS  unauthenticated  unhappy
    [Documentation]  HTTP OPTIONS: supported methods
    ...
    ...              An HTTP OPTIONS request is expected to return a list of supported HTTP methods
    ...              for an endpoint (eg. POST, GET, OPTIONS, HEAD).
    ...
    ...              Example manual call: ``$ http OPTIONS :5009/api/v1/admin/users/stevefor@idir/roles``
    Given An unauthenticated HTTP OPTIONS request to /api/v1/admin/users/${DFTTF_ADMIN_USER}/roles
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error":"Unauthorized"}


Get admin form options with authentication
    [Tags]           admin user roles  OPTIONS  authenticated  happy
    [Documentation]  HTTP OPTIONS
    ...
    ...              An HTTP OPTIONS request is expected to return a list of supported HTTP methods
    ...              for an endpoint (eg. POST, GET, OPTIONS, HEAD).
    ...
    ...              Example manual call: ``$ http OPTIONS :5009/api/v1/admin/users/stevefor@idir/roles  --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP OPTIONS request to /api/v1/admin/users/${DFTTF_ADMIN_USER}/roles
    Then Response code is HTTP  200
    And Response Allow header should contain value GET
    And Response Allow header should contain value POST
    And Response Allow header should contain value PATCH
    And Response Allow header should contain value DELETE
    And Response Allow header should contain value HEAD
    And Response Allow header should contain value OPTIONS
    And Response Allow header should not contain value PUT
