*** Settings ***
Library    RPA.JSON    # https://github.com/robocorp/rpaframework/
Library    Process     # https://robotframework.org/robotframework/latest/libraries/Process.html
Library    String

*** Keywords ***

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
    Should contain  ${test_response.text}  ${substring}  Response body does not contain '${substring}'. Body received: '${test_response.text}'

Response body does not contain
    [Arguments]  ${substring}
    Log  ${substring}
    Should not contain  ${test_response.text}  ${substring}  Response body unexpectedly contains '${substring}'.

Response should be identical to the last unauthenticated request
    Should be equal  ${last_unauthenticated_response.text}  ${test_response.text}

Response body is
    [Arguments]  ${body_text}
    Should be equal as strings  ${test_response.text.strip()}  ${body_text.strip()}  Expected response body to be '${body_text.strip()}' but received: '${test_response.text.strip()}' instead.

Response body is empty
    Should Be True    len('${test_response.text}') == 0

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

Response should have at least ${min_length} records
    Log  ${test_response.json()}
    ${records_length} =  Get Length  ${test_response.json()}
    Run keyword and warn on failure  Should be true  ${records_length} > ${min_length}  ${TEST NAME}: Not enough records (found ${records_length}, expected at least ${min_length}).





JSON payload includes ${section_name} section
    ${json_records} =    Get values from JSON    ${test_response.json()}    $.configuration.${section_name}
    ${length} =  Get Length  ${json_records}
    Should be true  ${length} > 0  ${TEST NAME}: Did not find '${section_name}' in JSON response
    Log    Found ${section_name} in payload: ${json_records}


JSON structure ${section_name} should have at least ${min_length} records
    ${json_records} =    Get values from JSON    ${test_response.json()}    $.configuration.${section_name}
    Log    Found records: ${json_records}[0]    # 'Get values from JSON' returns results in an array
    ${length} =  Get Length  ${json_records}[0]
    Log    Found ${length} in ${section_name}
    Should be true  ${length} >= ${min_length}  ${TEST NAME}: Not enough records (found ${length}, expected at least ${min_length}).

Code table ${section_name} should have at least ${min_length} records
    ${json_records} =    Get values from JSON    ${TEST_TABLE}    $.configuration.${section_name}
    Log    Found records: ${json_records}[0]    # 'Get values from JSON' returns results in an array
    ${length} =  Get Length  ${json_records}[0]
    Log    Found ${length} in ${section_name}
    Should be true  ${length} >= ${min_length}  ${TEST NAME}: Not enough records (found ${length}, expected at least ${min_length}).


Get keys from ${section_name} table
    ${json_records} =    Get values from JSON    ${CODE_TABLES}    $.configuration.${section_name}
    Log    Found records: ${json_records}[0]    # 'Get values from JSON' returns results in an array
    ${length} =  Get Length  @${json_records}[0]
    Log    Found ${length} in ${section_name}
    ${codes} =  Create List
    FOR  ${item}  IN  @{json_records}[0]
        ${cd} =  JSONLibrary.Get Value From Json    ${item}    $..objectCd
        Log  ${cd}
        Append to list  ${codes}  ${cd[0]}
    END
    Log  ${codes}
    Set Test Variable   ${TEST_TABLE}  ${codes}

Get keys from ${section_name} table with identityId
    ${json_records} =    Get values from JSON    ${CODE_TABLES}    $.configuration.${section_name}
    Log    Found records: ${json_records}[0]    # 'Get values from JSON' returns results in an array
    ${length} =  Get Length  @${json_records}[0]
    Log    Found ${length} in ${section_name}
    ${codes} =  Create List
    FOR  ${item}  IN  @{json_records}[0]
        ${cd} =  JSONLibrary.Get Value From Json    ${item}    $..identityId
        Log  ${cd}
        Append to list  ${codes}  ${cd[0]}
    END
    Log  ${codes}
    Set Test Variable   ${TEST_TABLE}  ${codes}

Get keys from ${section_name} table with reviewAppTypeCd
    ${json_records} =    Get values from JSON    ${CODE_TABLES}    $.configuration.${section_name}
    Log    Found records: ${json_records}[0]    # 'Get values from JSON' returns results in an array
    ${length} =  Get Length  @${json_records}[0]
    Log    Found ${length} in ${section_name}
    ${codes} =  Create List
    FOR  ${item}  IN  @{json_records}[0]
        ${cd} =  JSONLibrary.Get Value From Json    ${item}    $..reviewAppTypeCd
        Log  ${cd}
        Append to list  ${codes}  ${cd[0]}
    END
    Log  ${codes}
    Set Test Variable   ${TEST_TABLE}  ${codes}

Get keys from ${section_name} table with documentTypeCd
    ${json_records} =    Get values from JSON    ${CODE_TABLES}    $.configuration.${section_name}
    Log    Found records: ${json_records}[0]    # 'Get values from JSON' returns results in an array
    ${length} =  Get Length  @${json_records}[0]
    Log    Found ${length} in ${section_name}
    ${codes} =  Create List
    FOR  ${item}  IN  @{json_records}[0]
        ${cd} =  JSONLibrary.Get Value From Json    ${item}    $..documentTypeCd
        Log  ${cd}
        Append to list  ${codes}  ${cd[0]}
    END
    Log  ${codes}
    Set Test Variable   ${TEST_TABLE}  ${codes}

Get ${type} keys from ${section} section
    [Documentation]  Calls jq command-line tool with query to extract values from JSON. This is easier than trying to
    ...              query JSON in RF. Note that Run Process will freeze if output is too large. Mitigate by redirecting
    ...              to a file, as mentioned in https://github.com/robotframework/robotframework/issues/3661. For example:
    ...              add stdout=filename.txt to redirect output to a file.
    ...              This works with structures like 'documents' and 'decisionOutcomes'.
    ${jq_query} =  Set variable  .configuration | .${section}\[] | select(.noticeTypeCd==\"${type}\") | .codes[] | select(.activeYN==\"Y\") | .objectCd
    ${result} =  Run process  jq  ${jq_query}  -r  stdin=${CODE_TABLES_TEXT}  timeout=5s  on_timeout=continue
    Log  STDOUT: ${result.stdout}
    Log  STDERR: ${result.stderr}
    # Iterate through lines in output and add to list, for easy comparison of results
    ${codes} =  Create List
    @{lines}=  Split to lines  ${result.stdout}
    FOR  ${line}   IN   @{lines}
        Append to list  ${codes}  ${line}
    END
    Set Test Variable   ${TEST_TABLE}  ${codes}









Response should have exactly ${required_length} records
    Log  ${test_response.json()}
    ${records_length} =  Get Length  ${test_response.json()}
    Should be true  ${records_length} == ${required_length}  ${TEST NAME}: Found ${records_length} records (expected ${required_length}).

${string_value} must be ${smallest_value} to ${largest_value} characters long
    Log  ${string_value}
    ${value_length} =  Get Length  ${string_value}
    Run keyword and warn on failure  Should be true  ${value_length} >= ${smallest_value}  ${TEST NAME}: Value '${string_value}' is less than ${smallest_value} characters long
    Run keyword and warn on failure  Should be true  ${value_length} <= ${largest_value}   ${TEST NAME}: Value '${string_value}' is more than ${largest_value} characters long

${string} should contain only ASCII characters
    Should match regexp  ${string}  [A-Z,0-9]*  ${TEST NAME}: Non-ASCII characters found in '${string}'

${string} must have no leading or trailing spaces
    Run keyword and warn on failure  Should be equal as strings  ${string}  ${string.strip()}  ${TEST NAME}: Value contains leading or trailing space in '${string}'


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
