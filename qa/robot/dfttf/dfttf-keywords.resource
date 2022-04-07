# Digital Forms 12/24 web service test keywords

# =======================================================================================
#      _       _       _       _  __                                _           _       _       _    
#   /\| |/\ /\| |/\ /\| |/\   | |/ /                               | |       /\| |/\ /\| |/\ /\| |/\ 
#   \ ` ' / \ ` ' / \ ` ' /   | ' / ___ _   ___      _____  _ __ __| |___    \ ` ' / \ ` ' / \ ` ' / 
#  |_     _|_     _|_     _|  |  < / _ \ | | \ \ /\ / / _ \| '__/ _` / __|  |_     _|_     _|_     _|
#   / , . \ / , . \ / , . \   | . \  __/ |_| |\ V  V / (_) | | | (_| \__ \   / , . \ / , . \ / , . \ 
#   \/|_|\/ \/|_|\/ \/|_|\/   |_|\_\___|\__, | \_/\_/ \___/|_|  \__,_|___/   \/|_|\/ \/|_|\/ \/|_|\/ 
#                                        __/ |                                                       
#                                       |___/ 
# =======================================================================================

*** Keywords ***

Create TTF sessions
    [Documentation]  Set up unauthenticated session, an authenticated session, and an authenticated
    ...              session with a Keykloak token (Authorization header).
    # Set up unauthenticated session
    ${headers}=  Create dictionary   Content-Type=application/json; charset=utf-8  Accept-Charset=utf-8
    Create Session 	unauthenticated_session 	${DFTTF_WEB_SERVICE_URL}  verify=True  headers=${headers}
    Set suite variable  ${DFTTF_UNAUTHENTICATED_SESSION}  unauthenticated_session
    
    # Set up authenticated session with credentials (see namespace secrets:)
    ${auth} =    Create List  ${FLASK_BASIC_AUTH_USER}  ${FLASK_BASIC_AUTH_PASS}
    ${headers}=  Create dictionary  Content-Type=application/json; charset=utf-8  Accept-Charset=utf-8
    Create Session      authenticated_session    url=${DFTTF_WEB_SERVICE_URL}  auth=${auth}  verify=True  headers=${headers}
    Set suite variable  ${DFTTF_AUTHENTICATED_SESSION}  authenticated_session

    # Set up an authenticated session with a Keykloak admin token (Authorization header with Bearer token, 
    # harvested from a browser and stored in the environment file, like dfttf-dev.resource).
    ${headers}=  Create dictionary   Content-Type=application/json; charset=utf-8  Accept-Charset=utf-8  Authorization=${ADMIN_BEARER_TOKEN}
    Create Session      admin_token_session    url=${DFTTF_WEB_SERVICE_URL}  verify=True  headers=${headers}
    Set suite variable  ${DFTTF_ADMIN_TOKEN_SESSION}  admin_token_session

    # Set up an authenticated session with a Keykloak officer token (Authorization header with Bearer token, 
    # harvested from a browser and stored in the environment file, like dfttf-dev.resource).
    ${headers}=  Create dictionary   Content-Type=application/json; charset=utf-8  Accept-Charset=utf-8  Authorization=${OFFICER_BEARER_TOKEN}
    Create Session      officer_token_session    url=${DFTTF_WEB_SERVICE_URL}  verify=True  headers=${headers}
    Set suite variable  ${DFTTF_OFFICER_TOKEN_SESSION}  officer_token_session


Response content type is
    [Arguments]  ${header_value}
    ${content_type} =  Get from Dictionary  ${test_response.headers}  content-type
    Should Contain  ${content_type}  ${header_value}

Response code is HTTP
    [Arguments]  ${response_status_code}
    Should be equal as strings  ${test_response.status_code}  ${response_status_code}  HTTP response code ${test_response.status_code} received. Expected ${response_status_code}

Response code is not HTTP
    [Arguments]  ${response_status_code}
    Should not be equal as strings  ${test_response.status_code}  ${response_status_code}  HTTP response code ${test_response.status_code} received. Expected it not to be ${test_response.status_code}.

Response body contains
    [Arguments]  ${substring}
    Log  ${substring}
    Should contain  ${test_response.text}  ${substring}  Response body does not contain '${substring}'. Body received: '${test_response.text'

Response body does not contain
    [Arguments]  ${substring}
    Log  ${substring}
    Should not contain  ${test_response.text}  ${substring}  Response body unexpectedly contains '${substring}'.

${string_value} must be ${smallest_value} to ${largest_value} characters long
    Log  ${string_value}
    ${value_length} =  Get Length  ${string_value}
    Run keyword and warn on failure  Should be true  ${value_length} >= ${smallest_value}  ${TEST NAME}: Value '${string_value}' is less than ${smallest_value} characters long
    Run keyword and warn on failure  Should be true  ${value_length} <= ${largest_value}   ${TEST NAME}: Value '${string_value}' is more than ${largest_value} characters long

${string} should contain only ASCII characters
    Should match regexp  ${string}  [A-Z,0-9]*  ${TEST NAME}: Non-ASCII characters found in '${string}'

${string} must have no leading or trailing spaces
    Run keyword and warn on failure  Should be equal as strings  ${string}  ${string.strip()}  ${TEST NAME}: Value contains leading or trailing space in '${string}'

Response should have at least ${min_length} records
    Log  ${test_response.json()}
    ${records_length} =  Get Length  ${test_response.json()}
    Run keyword and warn on failure  Should be true  ${records_length} > ${min_length}  ${TEST NAME}: Not enough records (found ${records_length}, expected at least ${min_length}).

Response should have exactly ${required_length} records
    Log  ${test_response.json()}
    ${records_length} =  Get Length  ${test_response.json()}
    Should be true  ${records_length} == ${required_length}  ${TEST NAME}: Found ${records_length} records (expected ${required_length}).

${item} should have at least ${min_length} values
    ${records_length} =  Get Length  ${item}
    Run keyword and warn on failure  Should be true  ${records_length} > ${min_length}  ${TEST NAME}: Not enough values (expected at least ${min_length} values in '${item}')

Every record should be ${smallest_value} to ${largest_value} characters long
    FOR  ${item}  IN  @{test_response.json()}
        Log  ${item}
        Run keyword and warn on failure  ${item} must be ${smallest_value} to ${largest_value} characters long
    END

There should be no duplicate values in the response payload
    FOR  ${item}  IN  @{test_response.json()}
        Log  Checking for duplicates in ${item}
        ${item} must not appear multiple times in the response
    END

# TODO: This is super slow! Implement in custom Python keyword.
${string_to_count} must not appear multiple times in the response
    ${item_count} =  Evaluate  0
    FOR  ${item}  IN  @{test_response.json()}
        ${stripped_item} =  Strip String  ${item}
        IF  "${stripped_item}" == "${string_to_count}"
            ${item_count} =  Evaluate  ${item_count} + 1
        END
        Log  Count: ${item_count}
    END
    Should be equal as integers  ${item_count}  1  Value '${string_to_count}' appears in the payload ${item_count} times.

Every record should have ${expected_record_count} subrecords
    FOR  ${item}  IN  @{test_response.json()}
        Log  ${item}
        ${records_length} =  Get Length  ${item}
        Should be equal as integers  ${expected_record_count}  ${expected_record_count}  ${records_length}
    END

Each item in the response should use ASCII encoding
    FOR  ${item}  IN  @{test_response.json()}
        Log  ${item}
        Run keyword and warn on failure  ${item} should contain only ASCII characters
    END

Each item in the response should have no leading or trailing spaces
    FOR  ${item}  IN  @{test_response.json()}
        Run keyword and warn on failure  ${item} must have no leading or trailing spaces
    END

Response should be identical to the last unauthenticated request
    Should be equal  ${last_unauthenticated_response.text}  ${test_response.text}

Response body should match 
    [Arguments]  ${body_text}
    Should be equal as strings  ${test_response.text.strip()}  ${body_text.strip()}  Expected response body to be '${body_text.strip()}' but received: '${test_response.text.strip()}' instead.

Response body should be empty
    Should be equal  ${test_response.text}  ""  Expected an empty response body, but received '${test_response.text}' instead.

Response should include ${header_name} header
   Dictionary should contain key  ${test_response.headers}  ${header_name}

Response should include ${header_name} header with value ${value}
    Dictionary should contain key  ${test_response.headers}  ${header_name}  ${value}

Response ${header_name} header should contain value ${header_value}
    ${all_header_values} =  Get from Dictionary  ${test_response.headers}  ${header_name}
    Should contain  ${all_header_values}  ${header_value}


Response ${header_name} header should not contain value ${header_value}
    ${all_header_values} =  Get from Dictionary  ${test_response.headers}  ${header_name}
    Should not contain  ${all_header_values}  ${header_value}

Response should include text
    [Arguments]  ${text_to_find}
    Should contain  ${test_response.text}  ${text_to_find}

# =======================================================================================
# REST METHODS
# =======================================================================================

# GET expecting success
An ${authentication_type} HTTP GET request to ${uri}
    [Documentation]  Generic HTTP GET method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  GET On Session 	${DFTTF_UNAUTHENTICATED_SESSION} 	${uri}
        Set suite variable  ${last_unauthenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  GET On Session 	${DFTTF_AUTHENTICATED_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "admin token"
        ${response} =  GET On Session 	${DFTTF_ADMIN_TOKEN_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "officer token"
        ${response} =  GET On Session 	${DFTTF_OFFICER_TOKEN_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

# GET expecting an error response
An ${authentication_type} HTTP GET request expecting response ${expected_status_code} from ${uri}
    [Documentation]  Generic HTTP GET method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  GET On Session 	${DFTTF_UNAUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  GET On Session 	${DFTTF_AUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "admin token"
        ${response} =  GET On Session 	${DFTTF_ADMIN_TOKEN_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "officer token"
        ${response} =  GET On Session 	${DFTTF_OFFICER_TOKEN_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

# POST expecting success
An ${authentication_type} HTTP POST request to ${uri} with payload ${payload}
    [Documentation]  Generic HTTP POST method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  POST On Session 	${DFTTF_UNAUTHENTICATED_SESSION} 	${uri}  ${payload}
        Set suite variable  ${last_unauthenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  POST On Session 	${DFTTF_AUTHENTICATED_SESSION} 	${uri}  ${payload}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "admin token"
        ${response} =  POST On Session 	${DFTTF_ADMIN_TOKEN_SESSION} 	${uri}  ${payload}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "officer token"
        ${response} =  POST On Session 	${DFTTF_OFFICER_TOKEN_SESSION} 	${uri}  ${payload}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

# POST expecting error
An ${authentication_type} HTTP POST request expecting response ${expected_status_code} from ${uri} with payload ${payload}
    [Documentation]  Generic HTTP POST method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  POST On Session 	${DFTTF_UNAUTHENTICATED_SESSION} 	${uri}  ${payload}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  POST On Session 	${DFTTF_AUTHENTICATED_SESSION} 	${uri}  ${payload}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "admin token"
        ${response} =  POST On Session 	${DFTTF_ADMIN_TOKEN_SESSION} 	${uri}  ${payload}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "officer token"
        ${response} =  POST On Session 	${DFTTF_OFFICER_TOKEN_SESSION} 	${uri}  ${payload}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

# PATCH expecting success
An ${authentication_type} HTTP PATCH request to ${uri} with payload ${payload}
    [Documentation]  Generic PATCH method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  PATCH On Session 	${DFTTF_UNAUTHENTICATED_SESSION} 	${uri}  ${payload}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  PATCH On Session 	${DFTTF_AUTHENTICATED_SESSION} 	${uri}  ${payload}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "admin token"
        ${response} =  PATCH On Session 	${DFTTF_ADMIN_TOKEN_SESSION} 	${uri}  ${payload}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "officer token"
        ${response} =  PATCH On Session 	${DFTTF_OFFICER_TOKEN_SESSION} 	${uri}  ${payload}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

# PATCH expecting error
An ${authentication_type} HTTP PATCH request expecting response ${expected_status_code} from ${uri} with payload ${payload}
    [Documentation]  Generic HTTP PATCH method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  PATCH On Session 	${DFTTF_UNAUTHENTICATED_SESSION} 	${uri}  ${payload}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  PATCH On Session 	${DFTTF_AUTHENTICATED_SESSION} 	${uri}  ${payload}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "admin token"
        ${response} =  PATCH On Session 	${DFTTF_ADMIN_TOKEN_SESSION} 	${uri}  ${payload}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "officer token"
        ${response} =  PATCH On Session 	${DFTTF_OFFICER_TOKEN_SESSION} 	${uri}  ${payload}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

# DELETE expecting success
An ${authentication_type} HTTP DELETE request to ${uri}
    [Documentation]  Generic DELETE method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  DELETE On Session 	${DFTTF_UNAUTHENTICATED_SESSION} 	${uri}  
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  DELETE On Session 	${DFTTF_AUTHENTICATED_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "admin token"
        ${response} =  DELETE On Session 	${DFTTF_ADMIN_TOKEN_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "officer token"
        ${response} =  DELETE On Session 	${DFTTF_OFFICER_TOKEN_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

# PATCH expecting error
An ${authentication_type} HTTP DELETE request expecting response ${expected_status_code} from ${uri}
    [Documentation]  Generic HTTP DELETE method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  DELETE On Session 	${DFTTF_UNAUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  DELETE On Session 	${DFTTF_AUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "admin token"
        ${response} =  DELETE On Session 	${DFTTF_ADMIN_TOKEN_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "officer token"
        ${response} =  DELETE On Session 	${DFTTF_OFFICER_TOKEN_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

# DELETE expected to return an error
An unauthenticated HTTP DELETE request, expecting an error, to
    [Arguments]  ${URI}
    ${response} =  DELETE On Session 	${DFTTF_UNAUTHENTICATED_SESSION} 	${URI}  expected_status=405
    Set test variable  ${test_response}  ${response}

# HEAD
An ${authentication_type} HTTP HEAD request to ${uri}
    [Documentation]  Generic PATCH method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  HEAD On Session 	${DFTTF_UNAUTHENTICATED_SESSION} 	${uri}  
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  HEAD On Session 	${DFTTF_AUTHENTICATED_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "admin token"
        ${response} =  HEAD On Session 	${DFTTF_ADMIN_TOKEN_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "officer token"
        ${response} =  HEAD On Session 	${DFTTF_OFFICER_TOKEN_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

# HEAD, expecting error response
An ${authentication_type} HTTP HEAD request expecting response ${expected_status_code} from ${uri}
    [Documentation]  Generic HTTP POST method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  HEAD On Session 	${DFTTF_UNAUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  HEAD On Session 	${DFTTF_AUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "admin token"
        ${response} =  HEAD On Session 	${DFTTF_ADMIN_TOKEN_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "officer token"
        ${response} =  HEAD On Session 	${DFTTF_OFFICER_TOKEN_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

# OPTIONS
An ${authentication_type} HTTP OPTIONS request to ${uri}
    [Documentation]  Generic OPTIONS method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  OPTIONS On Session 	${DFTTF_UNAUTHENTICATED_SESSION} 	${uri}  
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  OPTIONS On Session 	${DFTTF_AUTHENTICATED_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "admin token"
        ${response} =  OPTIONS On Session 	${DFTTF_ADMIN_TOKEN_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "officer token"
        ${response} =  OPTIONS On Session 	${DFTTF_OFFICER_TOKEN_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}