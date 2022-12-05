# Robot Framework Script to test NTT VI-IRP API

## Install Robot Framework and libraries

    pip install --user robotframework robotframework-requests robotframework-jsonlibrary rpaframework 

## OpenAPI spec

See https://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/swagger-ui/index.html#/

### Endpoints

The following endpoints have tests in this test suite:

    Codetables
    [x] GET     /codetables/{correlationId}

    DfPayloads 
    [-] GET     /dfpayloads/{noticeNo}/{correlationId}
    [ ] PUT     /dfpayloads/{noticeNo}/{correlationId}
    [-] POST    /dfpayloads/{noticeNo}/{correlationId}
    [ ] DELETE  /dfpayloads/{noticeNo}/{correlationId}

    Prohibitions
    [x] GET     /prohibitions/{correlationId}
    [x] POST    /prohibitions/{noticeNo}/{correlationId}

    Documents
    [x] GET     /documents/{documentId}/{correlationId}
    [x] GET     /documents/list/{noticeNo}/{correlationId}
    [x] POST    /documents/{correlationId}
    [ ] POST    /documents/association/notice/{documentId}/{correlationId}

    Utility
    [x] GET     /utility/ords/ping/{correlationId}
    
    Impoundments
    [x] POST    /impoundments/{correlationId}
    [x] GET     /impoundments/{noticeNo}/{correlationId}

### Codetables

Examples of retrieving the code tables:

    https ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth "user:$PASSWORD"

List tables returned from the endpoint:

    https ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth "user:$PASSWORD" | jq '.configuration | keys[]'

    "addresses"
    "contactMethods"
    "countries"
    "data_sources"
    "decisionOutcomes"
    "disposalActs"
    "disposalDecisions"
    "documentNotices"
    "documents"
    "dreEvaluations"
    "driverLicenceOffices"
    "groundsDecisions"
    "impoundLotOperators"
    "jurisdictions"
    "noticePrefixNos"
    "noticeTypes"
    "originalCauses"
    "policeDetachments"
    "provinces"
    "registration_roles"
    "releaseReasons"
    "reviewApplications"
    "reviewRoles"
    "reviewStatuses"
    "reviewTypes"
    "scheduleAppTypes"
    "unavailabilityReasons"
    "vehicleTypes"

List items in table, reviewApplications section:

    https ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth "user:$PASSWORD" | jq '.configuration | .reviewApplications[] | .noticeTypeCd'

    "ADP"
    "IRP"
    "UL"
    "IMP"
