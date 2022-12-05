*** Settings ***
Resource   keywords.resource
Library    RPA.JSON
Resource   random.resource
Library    String
Library    JSONLibrary

*** Keywords ***

Random ${CODE_TABLE} value
    [Documentation]  Returns a valid entry from a code table at random.
    ${random_value} =  Evaluate  random.choice(${CODE_TABLE})  random
    [Return]  ${random_value}

Set ${field} to random value from table ${TABLE}
    [Documentation]  Updates
    ${random_value} =  Evaluate  random.choice(${PAYLOAD})  random
    ${PAYLOAD} =  RPA.JSON.Update value to JSON  ${PAYLOAD}  ${field}  ${random_value}

Set impoundment impoundmentNoticeNo to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsImpoundCreate.impoundmentNoticeNo  ${value}

Set next available impoundment impoundmentNoticeNo
    [Documentation]  Use the next available IMP notice number.
    ${AVAILABLE_RECORD_NUMBER} =  Get next available VIPS IMP record
    Set impoundment impoundmentNoticeNo to ${AVAILABLE_RECORD_NUMBER}

Set impoundment vipsImpoundCreate dlJurisdictionCd to ${value}
    [Documentation]  Set for an impoundment payload. Not to be confused with
    ...              vipsLicenceCreateObj > dlJurisdictionCd!
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsImpoundCreate.dlJurisdictionCd  ${value}

Pick impoundment vipsImpoundCreate dlJurisdictionCd at random
    [Documentation]  Pick random ILO for an impoundment payload. Not to be confused with
    ...              vipsLicenceCreateObj > dlJurisdictionCd!
    ${random} =  Random ${TABLE_JURISDICTIONS} value
    Set impoundment vipsImpoundCreate dlJurisdictionCd to ${random}

Set impoundment impoundLotOperatorId to ${value}
    [Documentation]  Set for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsImpoundCreate.impoundLotOperatorId  ${value}

Pick impoundment impoundLotOperatorId at random
    [Documentation]  Pick random ILO for an impoundment payload.
    ${random} =  Random ${TABLE_IMPOUNDLOTOPERATORS} value
    Set impoundment impoundLotOperatorId to ${random}


SSet impoundment impoundmentDt to ${value}
    [Documentation]  Set for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsImpoundCreate.impoundmentDt  ${value}

Make impoundment impoundmentDt today
    [Documentation]  Set the impoundment date as today, ten minutes ago.
    ${today} =  Get Current Date	local
    ${earlier_today} =  Subtract Time From Date    ${today}    10 minutes  result_format=%Y-%m-%dT%H:%M:%S.000-08:00
    ${string_date} =  Convert to String  ${earlier_today}
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsImpoundCreate.impoundmentDt  ${string_date}

A future impountment impoundmentDt date
    [Documentation]  Set the impoundment date as today, half an hour in the future.
    ${today} =  Get Current Date	local
    ${earlier_today} =  Add Time To Date    ${today}    30 minutes  result_format=%Y-%m-%dT%H:%M:%S.000-08:00
    ${string_date} =  Convert to String  ${earlier_today}
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsImpoundCreate.impoundmentDt  ${string_date}

Set impoundment policeDetatchmentId to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsImpoundCreate.policeDetatchmentId  ${value}

Pick impoundment policeDetatchmentId at random
    [Documentation]  Pick random policeDetatchmentId value for an impoundment payload.
    ${random} =  Random ${TABLE_POLICEDETACHMENTS} value
    Set impoundment policeDetatchmentId to ${random}

Set impoundment originalCauseCds to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsImpoundCreate.originalCauseCds  ${value}

Select all impoundment originalCauseCds
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsImpoundCreate.originalCauseCds  ${TABLE_ORIGINALCAUSES_IMP}

Select incorrect originalCauseCds
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsImpoundCreate.originalCauseCds  ${TABLE_ORIGINALCAUSES_IRP}


Pick impoundment originalCauseCds at random
    [Documentation]  Pick random originalCauseCds value for an impoundment payload. 
    ${random} =  Random ${TABLE_ORIGINALCAUSES_IMP} value
    @{list} =	Create List	${random}
    Set impoundment originalCauseCds to ${list}

Set impoundment policeOfficerNm to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsImpoundCreate.policeOfficerNm  ${value}

Pick impoundment policeOfficerNm at random
    [Documentation]  Pick random value for an impoundment.
    ${random} =  Random ${DE_PHONETIC} value
    Set impoundment policeOfficerNm to ${random}

Set impoundment policeOfficerNo to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsImpoundCreate.policeOfficerNo  ${value}

Pick impoundment policeOfficerNo at random
    [Documentation]  Pick random value for an impoundment.
    ${RandomLength}=     Evaluate  random.sample(range(4, 8),1)   random
    ${random} =  Generate Random String  ${RandomLength}[0]  [NUMBERS]
    Set impoundment policeOfficerNo to ${random}

Set impoundment policeFileNo to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsImpoundCreate.policeFileNo  ${value}

Pick impoundment policeFileNo at random
    [Documentation]  Pick random value for an impoundment.
    ${RandomLength}=     Evaluate  random.sample(range(4, 7),1)   random
    ${random} =  Generate Random String  ${RandomLength}[0]  [NUMBERS]
    Set impoundment policeFileNo to ${random}

Set impoundment seizureLocationTxt to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsImpoundCreate.seizureLocationTxt  ${value}

Pick impoundment seizureLocationTxt at random
    [Documentation]  Pick random value for an impoundment.
    ${random} =  Random ${BC_MUNICIPALITIES} value
    Set impoundment seizureLocationTxt to ${random}

Set impoundment firstGivenNm to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsRegistrationCreateArray[0].firstGivenNm  ${value}
    Log  ${new_payload}

Pick impoundment firstGivenNm at random
    [Documentation]  Pick random value for an impoundment.
    ${random} =  Random ${ADJECTIVES} value
    Set impoundment firstGivenNm to ${random}

Set impoundment secondGivenNm to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsRegistrationCreateArray[0].secondGivenNm  ${value}
    Log  ${new_payload}

Pick impoundment secondGivenNm at random
    [Documentation]  Pick random value for an impoundment.
    ${random} =  Random ${GREEK_LETTERS} value
    Set impoundment secondGivenNm to ${random}

Set impoundment thirdGivenNm to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsRegistrationCreateArray[0].thirdGivenNm  ${value}
    Log  ${new_payload}

Pick impoundment thirdGivenNm at random
    [Documentation]  Pick random value for an impoundment.
    ${random} =  Random ${OLD_PHONETIC} value
    Set impoundment thirdGivenNm to ${random}

Set impoundment surnameNm to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsRegistrationCreateArray[0].surnameNm  ${value}
    Log  ${new_payload}

Pick impoundment surnameNm at random
    [Documentation]  Pick random value for an impoundment.
    ${random} =  Random ${ISO_PHONETIC} value
    Set impoundment surnameNm to ${random}

Set impoundment addressFirstLineTxt to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsRegistrationCreateArray[0].vipsAddressArray[0].addressFirstLineTxt  ${value}
    Log  ${new_payload}

Pick impoundment addressFirstLineTxt at random
    [Documentation]  Pick random value for an impoundment.
    ${RandomLength}=     Evaluate  random.sample(range(1, 5),1)   random
    ${number} =  Generate Random String  ${RandomLength}[0]  [NUMBERS]
    ${street} =  Random ${BC_STREETS} value
    ${random_address} =  Set Variable  ${number} ${street}
    Set impoundment addressFirstLineTxt to ${random_address}

Set impoundment addressSecondLineTxt to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsRegistrationCreateArray[0].vipsAddressArray[0].addressSecondLineTxt  ${value}
    Log  ${new_payload}

Pick impoundment addressSecondLineTxt at random
    [Documentation]  Pick random value for an impoundment.
    ${random} =  Random ${ISO_PHONETIC} value
    Set impoundment addressSecondLineTxt to ${random} suite

Set impoundment addressThirdLineTxt to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsRegistrationCreateArray[0].vipsAddressArray[0].addressThirdLineTxt  ${value}
    Log  ${new_payload}

Pick impoundment addressThirdLineTxt at random
    [Documentation]  Pick random value for an impoundment.
    ${random} =  Random ${COLOURS} value
    Set impoundment addressThirdLineTxt to ${random} door

Set impoundment cityNm to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsRegistrationCreateArray[0].vipsAddressArray[0].cityNm  ${value}
    Log  ${new_payload}

Pick impoundment cityNm at random
    [Documentation]  Pick random value for an impoundment.
    ${random} =  Random ${BC_MUNICIPALITIES} value
    Set impoundment cityNm to ${random}

Set impoundment postalCodeTxt to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsRegistrationCreateArray[0].vipsAddressArray[0].postalCodeTxt  ${value}
    Log  ${new_payload}

Pick impoundment postalCodeTxt at random
    [Documentation]  Pick random value for an impoundment.
    ${random} =  Random postal code
    Set impoundment postalCodeTxt to ${random}
    

Set impoundment countryNm to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsRegistrationCreateArray[0].vipsAddressArray[0].countryNm  ${value}
    Log  ${new_payload}

Pick impoundment countryNm at random
    [Documentation]  Pick random value for an impoundment.
    ${random} =  Random ${TABLE_COUNTRIES} value
    Set impoundment countryNm to ${random}

Set impoundment driverLicenceNo to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsRegistrationCreateArray[0].vipsLicenceCreateObj.driverLicenceNo  ${value}
    Log  ${new_payload}

Set next impoundment driverLicenceNo
    [Documentation]  Pick random value for an impoundment.
    ${dl} =  Get next BCDL in sequence
    Set impoundment driverLicenceNo to ${dl}

Set impoundment birthDt to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsLicenceCreateObj.birthDt  ${value}
    Log  ${new_payload}

Pick impoundment birthDt at random
    [Documentation]  Pick random value for an impoundment.
    ${random} =  Random birthdate
    Set impoundment birthDt to ${random}

Set impoundment vipsLicenceCreateObj dlJurisdictionCd to ${value}
    [Documentation]  Set value for an impoundment payload. Not to be confused with
    ...              vipsImpoundCreate > dlJurisdictionCd!
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsLicenceCreateObj.dlJurisdictionCd  ${value}
    Log  ${new_payload}

Pick impoundment vipsLicenceCreateObj dlJurisdictionCd at random
    [Documentation]  Pick random value for an impoundment. Not to be confused with
    ...              vipsImpoundCreate > dlJurisdictionCd!
    ${random} =  Random ${TABLE_JURISDICTIONS} value
    Set impoundment dlJurisdictionCd to ${random}

Set impoundment licencePlateNo to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsVehicleCreate.licencePlateNo  ${value}
    Log  ${new_payload}

Pick impoundment licencePlateNo at random
    [Documentation]  Pick random value for an impoundment.
    ${random} =  Random licence plate
    Set impoundment licencePlateNo to ${random}

Set impoundment vehicleIdentificationNo to ${value}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsVehicleCreate.vehicleIdentificationNo  ${value}
    Log  ${new_payload}

Pick impoundment vehicleIdentificationNo at random
    [Documentation]  Pick random value for an impoundment.
    ${random} =  Random VIN
    Set impoundment vehicleIdentificationNo to ${random}

Set impoundment vipsDocumentIdArray to ${value_list}
    [Documentation]  Set value for an impoundment payload.
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsDocumentIdArray  ${value_list}
    Log  ${new_payload}

Impoundment vipsDocumentIdArray is empty
    [Documentation]  Set value for an impoundment payload.
    @{EmptyDocumentList} =    Create List
    ${new_payload} =  RPA.JSON.Update value to JSON  ${new_payload}  $.vipsDocumentIdArray  ${EmptyDocumentList}
    Log  ${new_payload}

A random impoundment payload
    [Documentation]  Generic HTTP POST method, authenticated or unauthenticated, expected to succeed.
    ${json} =    RPA.JSON.Convert String to JSON    ${body} 
    Set Test Variable    ${new_payload}  ${json}
    
    # Randomise fields in JSON vipsImpoundCreate section
    Set next available impoundment impoundmentNoticeNo
    Set impoundment vipsImpoundCreate dlJurisdictionCd to BC
    Pick impoundment impoundLotOperatorId at random
    Make impoundment impoundmentDt today
    Pick impoundment policeDetatchmentId at random
    Pick impoundment originalCauseCds at random
    Pick impoundment policeOfficerNm at random
    Pick impoundment policeOfficerNo at random
    Pick impoundment policeFileNo at random
    Pick impoundment seizureLocationTxt at random
    
    # Randomise fields in JSON vipsRegistrationCreateArray section
    Pick impoundment firstGivenNm at random
    Pick impoundment secondGivenNm at random
    Pick impoundment thirdGivenNm at random
    Pick impoundment surnameNm at random

    # Randomise fields in JSON vipsRegistrationCreateArray > vipsAddressArray section
    Pick impoundment addressFirstLineTxt at random
    Pick impoundment addressSecondLineTxt at random
    Pick impoundment addressThirdLineTxt at random
    Pick impoundment cityNm at random
    Set impoundment countryNm to CAN
    Pick impoundment postalCodeTxt at random

    # Randomise fields in JSON vipsLicenceCreateObj section
    Set next impoundment driverLicenceNo
    Pick impoundment birthDt at random
    Set impoundment vipsLicenceCreateObj dlJurisdictionCd to BC

    # Randomise fields in JSON vipsVehicleCreate section
    Pick impoundment licencePlateNo at random
    Pick impoundment vehicleIdentificationNo at random
    # There are several other fields that could be updated

    # Randomise vipsDocumentIdArray
    # ...

    # Randomise vipsImpoundmentArray
    # ...

    # Check my work
    Log  Freshly generated payload: ${new_payload}
    ${payload_string} =  Convert To String    ${new_payload}
    Set Test Variable    ${payload}  ${payload_string}
    Log  ${payload}

# GET expecting success
An ${authentication_type} GET request to ${uri}
    [Documentation]  Generic HTTP GET method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  GET On Session 	${UNAUTHENTICATED_SESSION} 	${uri}
        Set suite variable  ${last_unauthenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  GET On Session 	${AUTHENTICATED_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# GET expecting error
An ${authentication_type} GET request expecting HTTP ${expected_status_code} from ${uri}
    [Documentation]  Generic HTTP GET method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  GET On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  GET On Session 	${AUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# POST expecting success
An ${authentication_type} POST request to ${uri} with payload ${payload}
    [Documentation]  Generic HTTP POST method, authenticated or unauthenticated, expected to succeed.
    ${AVAILABLE_RECORD_NUMBER} =  Get next available VIPS IMP record
    ${json}=    RPA.JSON.Convert String to JSON    ${payload}
    ${UPDATED_PAYLOAD} =  RPA.JSON.Update value to JSON  ${json}  $.vipsImpoundCreate.impoundmentNoticeNo  ${AVAILABLE_RECORD_NUMBER}
    Log  Updated payload: ${UPDATED_PAYLOAD}
    Log  Body palyoad: ${payload}
    ${json} =    RPA.JSON.Convert JSON to String  ${UPDATED_PAYLOAD}
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  POST On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  ${json}
        Set suite variable  ${last_unauthenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  POST On Session 	${AUTHENTICATED_SESSION} 	${uri}  ${json}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

A POST request to ${uri} with JSON payload ${payload}
    [Documentation]  Generic HTTP POST method, authenticated or unauthenticated, expected to succeed.
    ${json}=	JSONLibrary.Convert JSON to String	${payload}
    Log  JSON STRING: ${json}
    ${response} =  POST On Session 	${AUTHENTICATED_SESSION} 	${uri}  ${json}
    Set suite variable  ${last_authenticated_response}  ${response}
    Set test variable  ${test_response}  ${response}





# POST expecting error
An ${authentication_type} POST request expecting HTTP ${expected_status_code} from ${uri} with payload ${payload}
    [Documentation]  Generic HTTP POST method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  POST On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  ${payload}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  POST On Session 	${AUTHENTICATED_SESSION} 	${uri}  ${payload}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# PATCH expecting success
An ${authentication_type} PATCH request to ${uri} with payload ${payload}
    [Documentation]  Generic PATCH method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  PATCH On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  ${payload}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  PATCH On Session 	${AUTHENTICATED_SESSION} 	${uri}  ${payload}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# PATCH expecting error
An ${authentication_type} PATCH request expecting HTTP ${expected_status_code} from ${uri} with payload ${payload}
    [Documentation]  Generic HTTP PATCH method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  PATCH On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  ${payload}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  PATCH On Session 	${AUTHENTICATED_SESSION} 	${uri}  ${payload}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# DELETE expecting success
An ${authentication_type} HTTP DELETE request to ${uri}
    [Documentation]  Generic DELETE method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  DELETE On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  DELETE On Session 	${AUTHENTICATED_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# DELETE expecting error
An ${authentication_type} DELETE request expecting HTTP ${expected_status_code} from ${uri}
    [Documentation]  Generic HTTP DELETE method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  DELETE On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  DELETE On Session 	${AUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# DELETE expecting error
An unauthenticated HTTP DELETE request, expecting an error, to
    [Arguments]  ${URI}
    ${response} =  DELETE On Session 	${UNAUTHENTICATED_SESSION} 	${URI}  expected_status=405
    Set test variable  ${test_response}  ${response}


# HEAD expecting success
An ${authentication_type} HEAD request to ${uri}
    [Documentation]  Generic PATCH method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  HEAD On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  HEAD On Session 	${AUTHENTICATED_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

# HEAD, expecting error response
An ${authentication_type} HEAD request expecting HTTP ${expected_status_code} from ${uri}
    [Documentation]  Generic HTTP POST method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  HEAD On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  HEAD On Session 	${AUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# OPTIONS expecting success
An ${authentication_type} OPTIONS request to ${uri}
    [Documentation]  Generic OPTIONS method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  OPTIONS On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  OPTIONS On Session 	${AUTHENTICATED_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

# OPTIONS expecting error
An ${authentication_type} OPTIONS request expecting HTTP ${expected_status_code} from ${uri}
    [Documentation]  Generic HTTP OPTIONS method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  OPTIONS On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  OPTIONS On Session 	${AUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

# PUT expecting success
An ${authentication_type} PUT request to ${uri}
    [Documentation]  Generic PUT method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  PUT On Session 	${UNAUTHENTICATED_SESSION} 	${uri}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  PUT On Session 	${AUTHENTICATED_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

# PUT expecting error
An ${authentication_type} PUT request expecting HTTP ${expected_status_code} from ${uri}
    [Documentation]  Generic HTTP PUT method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  PUT On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  PUT On Session 	${AUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}