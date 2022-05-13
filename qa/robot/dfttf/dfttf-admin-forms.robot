# Digital Forms 12/24 web service tests

# =======================================================================================
#              _           _         ______
#     /\      | |         (_)       |  ____|
#    /  \   __| |_ __ ___  _ _ __   | |__ ___  _ __ _ __ ___  ___
#   / /\ \ / _` | '_ ` _ \| | '_ \  |  __/ _ \| '__| '_ ` _ \/ __|
#  / ____ \ (_| | | | | | | | | | | | | | (_) | |  | | | | | \__ \
# /_/    \_\__,_|_| |_| |_|_|_| |_| |_|  \___/|_|  |_| |_| |_|___/
#
# Tests for the /api/v1/admin/forms endpoints in 12/24 web service
# =======================================================================================

*** Settings ***


Documentation  Digital Forms 12/24 web service test suite for the ``/api/v1/admin/forms`` endpoints and methods.
...
...            See current implementation in DFTTF source code (2021-12-22):
...            https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/blueprints/admin_forms.py
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

Get admin forms without authentication
    [Tags]           admin forms  GET  unauthenticated  unhappy
    [Documentation]  HTTP GET
    ... 
    ...              *Should not* be accessible without authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet).\n
    ...              Python line in DFTTF source: ``@bp.route('/forms', methods=['GET'])``
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/forms``
    Given An unauthenticated HTTP GET request expecting response 401 from /api/v1/admin/forms
    Then Response code is HTTP  401
    And Response body should match  {"error":"Unauthorized"}
    

Get admin forms with authentication
    [Tags]           admin forms  GET  authenticated  happy
    [Documentation]  HTTP GET
    ...
    ...              *Should* be accessible with authentication.
    ...
    ...              For details, see https://justice.gov.bc.ca/jirarsi/browse/DF-1445 (includes spreadsheet)\n
    ...              Python line in DFTTF source: ``@bp.route('/forms', methods=['GET'])``
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/forms --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP GET request to /api/v1/admin/forms
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Each item in the response should use ASCII encoding
    And Each item in the response should have no leading or trailing spaces
    And Response should have exactly 2 records


Attempt to get one form without authentication
    [Tags]           admin forms  GET  unauthenticated  unhappy
    [Documentation]  HTTP GET
    ...
    ...              *Should not* be accessible without authentication.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/forms/<string:form_id>', methods=['GET'])``
    ...
    ...              Example manual call: $ http :5009/api/v1/admin/forms/IRP
    Given An unauthenticated HTTP GET request expecting response 401 from /api/v1/admin/forms/IRP
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error":"Unauthorized"}


Attempt to get one form with authentication
    [Tags]           admin forms  GET  authenticated  happy
    [Documentation]  HTTP GET
    ...
    ...              As of December 2021, endpoint should respond with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              Python line in DFTTF source: ``@bp.route('/forms/<string:form_id>', methods=['GET'])``
    ...
    ...              Example manual call: ``$ http :5009/api/v1/admin/forms/IRP --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP GET request expecting response 405 from /api/v1/admin/forms/IRP
    Then Response code is HTTP  405
    And Response content type is  text/html
    And Response body should match  method not implemented


#  _____   ____   _____ _______
# |  __ \ / __ \ / ____|__   __|
# | |__) | |  | | (___    | |
# |  ___/| |  | |\___ \   | |
# | |    | |__| |____) |  | |
# |_|     \____/|_____/   |_|

Attempt to create admin form without authentication
    [Tags]           admin forms  POST  unauthenticated  unhappy
    [Documentation]  HTTP POST
    ...
    ...              *Should not* be accessible without authentication.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/forms', methods=['POST'])``
    ...
    ...              Example manual call: ``$ echo '{"form":"form"}' | http POST :5009/api/v1/admin/forms``
    Given An unauthenticated HTTP POST request expecting response 401 from /api/v1/admin/forms with payload {"form":"form"}
    Then Response code is HTTP  401
    And Response body should match  {"error":"Unauthorized"}


Attempt to create admin form with authentication but invalid JSON payload
    [Tags]           admin forms  POST  authenticated  unhappy
    [Documentation]  HTTP POST
    ...
    ...              *Should* be accessible with authentication.
    ...
    ...              Processed by form middleware: ``get_json_payload > validate_form_payload > admin_create_form`` in
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/middleware/form_middleware.py
    ...              Possible failure responses: payload_missing, failed_validation, server_error_response in
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/http_responses.py
    ...
    ...              Python line in DFTTF source: ``@bp.route('/forms', methods=['POST'])``
    ...
    ...              Example manual call: ``$ echo '{"form":"form"}' | http POST :5009/api/v1/admin/forms --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP POST request expecting response 400 from /api/v1/admin/forms with payload {"form_id":"steve1","form_type":"steve"}
    Then Response code is HTTP  400
    # Notice the space character between the colon and "failed"
    And Response body should match  {"error": "failed validation"}


Attempt to create admin form with authentication but missing payload
    [Tags]           admin forms  POST  authenticated  unhappy
    [Documentation]  HTTP POST
    ...
    ...              *Should* be accessible with authentication.
    ...
    ...              Processed by form middleware: ``get_json_payload > validate_form_payload > admin_create_form`` in
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/middleware/form_middleware.py
    ...              Possible failure responses: payload_missing, failed_validation, server_error_response in
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/http_responses.py
    ...
    ...              Python line in DFTTF source: ``@bp.route('/forms', methods=['POST'])``
    ...
    ...              Example manual call: ``$ http POST :5009/api/v1/admin/forms --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP POST request to /api/v1/admin/forms with payload ""
    Then Response code is HTTP  403
    And Response body should match  missing payload
    
    
Create admin form with authentication and valid JSON payload
    [Tags]           admin forms  POST  authenticated  happy
    [Documentation]  HTTP POST
    ...
    ...              *Should* be accessible with authentication.
    ...
    ...              Processed by form middleware: ``get_json_payload > validate_form_payload > admin_create_form`` in
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/middleware/form_middleware.py
    ...              Possible failure responses: payload_missing, failed_validation, server_error_response in
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/http_responses.py
    ...
    ...              Python line in DFTTF source: ``@bp.route('/forms', methods=['POST'])``
    ...
    ...              Example manual call: ``$ echo '{"form_id":"steve1","form_type":"IRP"}' | http POST :5009/api/v1/admin/forms --auth ${USERNAME}:${PASSWORD}``
    ...              *Note*: Once a form is created, it can currently only be deleted by removing it from the database manually. Appears to be
    ...              an in-memory datbase based on SQLAlchemy? See:
    ...              https://github.com/bcgov/RSBC-DataHub-API/blob/release/2021-09-22/python/prohibition_web_service/models.py
    Given An authenticated HTTP POST request to /api/v1/admin/forms with payload {"form_id":"steve1","form_type":"IRP"}
    Then Response code is HTTP  201
    And Response body should match  {"success":true}
    

#  _____     _______ _____ _    _
# |  __ \ /\|__   __/ ____| |  | |
# | |__) /  \  | | | |    | |__| |
# |  ___/ /\ \ | | | |    |  __  |
# | |  / ____ \| | | |____| |  | |
# |_| /_/    \_\_|  \_____|_|  |_|

Attempt to update admin form without authentication
    [Tags]           admin forms  PATCH  unauthenticated  unhappy
    [Documentation]  HTTP PATCH
    ...
    ...              *Should not* be accessible without authentication.
    ...
    ...              Python line in DFTTF source: ``@bp.route('/forms/<string:form_id>', methods=['PATCH'])``
    ...
    ...              Example manual call: ``$ echo '{"form":"main"}' | http PATCH :5009/api/v1/admin/forms/main``
    Given An unauthenticated HTTP PATCH request expecting response 401 from /api/v1/admin/forms/main with payload {"form":"main"}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error":"Unauthorized"}


Attempt to update admin form with authentication
    [Tags]           admin forms  PATCH  authenticated  happy
    [Documentation]  HTTP PATCH
    ...
    ...              As of December 2021, endpoint should respond with HTTP 405 "NOT IMPLEMENTED".
    ...
    ...              *Should* be accessible without authentication.
    ...
    ...              Python line in DFTTF source: `@bp.route('/forms/<string:form_id>', methods=['PATCH'])`
    ...
    ...              Example manual call: ``$ echo '{"form_id":"steve1","form_type":"IRP"}' | http PATCH :5009/api/v1/admin/forms/steve1 --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP PATCH request expecting response 405 from /api/v1/admin/forms/steve1 with payload {"form_id":"steve1","form_type":"IRP"}
    Then Response code is HTTP  405
    And Response content type is  text/html
    And Response body should match  method not implemented


#  _    _ ______          _____
# | |  | |  ____|   /\   |  __ \
# | |__| | |__     /  \  | |  | |
# |  __  |  __|   / /\ \ | |  | |
# | |  | | |____ / ____ \| |__| |
# |_|  |_|______/_/    \_\_____/

Get admin form headers without authentication
    [Tags]           admin forms  HEAD  unauthenticated  unhappy
    [Documentation]  HTTP HEAD
    ...
    ...              An HTTP HEAD request is expected to return the HTTP headers for a request
    ...              without a body.
    ...
    ...              Example manual call: ```$ http HEAD :5009/api/v1/admin/forms``
    Given An unauthenticated HTTP HEAD request expecting response 401 from /api/v1/admin/forms
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error":"Unauthorized"}


Get admin form headers with authentication
    [Tags]           admin forms  HEAD  authenticated  happy
    [Documentation]  HTTP HEAD
    ...
    ...              An HTTP HEAD request is expected to return the HTTP headers for a request
    ...              without a body.
    ...
    ...              Example manual call: ``$ http HEAD :5009/api/v1/admin/forms  --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP HEAD request to /api/v1/admin/forms
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
    [Tags]           admin forms  OPTIONS  unauthenticated  unhappy
    [Documentation]  HTTP OPTIONS: supported methods
    ...
    ...              An HTTP OPTIONS request is expected to return a list of supported HTTP methods
    ...              for an endpoint (eg. POST, GET, OPTIONS, HEAD).
    ...
    ...              Example manual call: ``$ http OPTIONS :5009/api/v1/admin/forms``
    Given An unauthenticated HTTP OPTIONS request to /api/v1/admin/forms
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body should match  {"error":"Unauthorized"}


Get admin form options with authentication
    [Tags]           admin forms  OPTIONS  authenticated  happy
    [Documentation]  HTTP OPTIONS
    ...
    ...              An HTTP OPTIONS request is expected to return a list of supported HTTP methods
    ...              for an endpoint (eg. POST, GET, OPTIONS, HEAD).
    ...
    ...              Example manual call: ``$ http OPTIONS :5009/api/v1/admin/forms  --auth ${USERNAME}:${PASSWORD}``
    Given An authenticated HTTP OPTIONS request to /api/v1/admin/forms
    Then Response code is HTTP  200
    Response Allow header should contain value POST
    Response Allow header should contain value GET
    Response Allow header should contain value OPTIONS
    Response Allow header should contain value HEAD
    Response Allow header should contain value PATCH
