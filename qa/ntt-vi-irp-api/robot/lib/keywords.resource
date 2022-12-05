*** Settings ***
Library      DateTime         # https://robotframework.org/robotframework/latest/libraries/DateTime.html
Library      Process

*** Keywords ***

Create DF VI-IRP API sessions
    [Documentation]  Set up authenticated and unauthenticated sessions for suite tests.

    # UNauthenticated session
    ${headers}=  Create dictionary   Content-Type=application/json; charset=utf-8  Accept-Charset=utf-8
    Create Session 	unauthenticated_session 	${API_URL}  verify=True  headers=${headers}
    Set suite variable  ${UNAUTHENTICATED_SESSION}  unauthenticated_session    children=true

    # Authenticated session with credentials
    ${auth} =    Create List  ${API_USERNAME}  ${API_PASSWORD}
    ${headers}=  Create dictionary  Content-Type=application/json; charset=utf-8  Accept-Charset=utf-8
    Create Session      authenticated_session    url=${API_URL}  auth=${auth}  verify=True  headers=${headers}
    Set suite variable  ${AUTHENTICATED_SESSION}  authenticated_session    children=true

    #${date} =    Get Current Date    result_format=robot-%Y-%m-%d-%H%M-%S
    #Set suite variable    ${CORRELATION}    ${date}    children=true

Get next available VIPS ${PROHIBITION_TYPE} record
    [Documentation]  Get the next available prohibition number for VIPS ADP/IRP/UL/IMP records.
    ...              Call with ${PROHIBITION_TYPE} set to one of: ADP, IRP, UL, IMP.
    ...              For implementation details, see get-next-available-vips-number.ps1 script.
    ${result} =  Run process  Powershell.exe  .\\get-next-available-vips-number.ps1  ${PROHIBITION_TYPE}  timeout=60s  on_timeout=continue
    Log  STDOUT: ${result.stdout}
    Log  STDERR: ${result.stderr}
    [return]  ${result.stdout}

Get next BCDL in sequence
    [Documentation]  Calls a PowerShell script to iterate a counter. Used to ensure BC driver licence numbers are
    ...              somewhat unique in VIPS.
    ...              For implementation details, see get-count.ps1 script.
    ${result} =  Run process  Powershell.exe  .\\get-count.ps1  BCDL  timeout=5s  on_timeout=continue
    Log  STDOUT: ${result.stdout}
    Log  STDERR: ${result.stderr}
    [return]  ${result.stdout}

Random birthdate
    [Documentation]  Calls a PowerShell script to generate a random birthdate in ISO-8601 format for use with API.
    ${result} =  Run process  Powershell.exe  .\\get-random-date.ps1  1930-01-01  2012-01-01  %Y-%m-%dT00:00:00.000%Z:00  timeout=5s  on_timeout=continue
    Log  STDOUT: ${result.stdout}
    Log  STDERR: ${result.stderr}
    [return]  ${result.stdout}