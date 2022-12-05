# Robot Framework

*** Settings ***
Documentation    Codetables GET endpoint
Library      JSONLibrary
Library      RequestsLibrary  # https://github.com/MarketSquare/robotframework-requests
Library      Collections      # Used to check header response from RequestsLibrary
Library      String           # https://robotframework.org/robotframework/latest/libraries/String.html
Library      Process          # https://robotframework.org/robotframework/latest/libraries/Process.html
Library      OperatingSystem  # https://robotframework.org/robotframework/latest/libraries/OperatingSystem.html
Library      DateTime         # https://robotframework.org/robotframework/latest/libraries/DateTime.html

# Settings for the DEV environment
#Variables   dev.Variables              # Environment settings

Resource   lib/keywords.resource        # Keywords
Resource   lib/kw-requests.resource     # Keywords for server requests
Resource   lib/kw-responses.resource    # Keywords for server responses

*** Variables ***
# See env.py
${CORRELATION} =    robot-code-tables-01

*** Keywords ***
# See lib/*.robot

*** Test Cases ***
#     _   _
#    | | | | __ _ _ __  _ __  _   _
#    | |_| |/ _` | '_ \| '_ \| | | |
#    |  _  | (_| | |_) | |_) | |_| |
#    |_| |_|\__,_| .__/| .__/ \__, |
#                |_|   |_|    |___/
Codetables GET authenticated
    [Tags]           codetables  authenticated    GET    happy  matrix 
    [Documentation]  Should return code table
    ...
    ...              Examples: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth "user:$PASSWORD"``
    ...              ``- $ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth "user:$PASSWORD" | jq '.configuration | .addresses'``
    Given An authenticated GET request to /v1/codetables/${CORRELATION}
    Then Response code is HTTP  200
    And Response content type is  application/json
    And Response should include text  "respMsg":"Success"
    And Set Global Variable    ${CODE_TABLES}  ${test_response.json()}
    And Set Global Variable    ${CODE_TABLES_TEXT}  ${test_response.text}

Codetables OPTIONS authenticated
    [Tags]           codetables    authenticated    OPTIONS    happy
    [Documentation]  Should show supported headers
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated OPTIONS request to /v1/codetables/${CORRELATION}
    Then Response code is HTTP  200
    And Response body is empty
    And Response allow header should contain value GET,HEAD,OPTIONS

Codetables HEAD authenticated
    [Tags]           codetables    authenticated    HEAD    happy
    [Documentation]  Should return headers, content
    ...
    ...              Example: ``$ https HEAD digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated HEAD request to /v1/codetables/${CORRELATION}
    Then Response code is HTTP  200
    And Response body is empty
    And Response content type is  application/json
    And Response pragma header should contain value no-cache
    And Response cache-control header should contain value no-cache, no-store, max-age=0, must-revalidate
    And Response x-content-type-options header should contain value nosniff
    And Response x-frame-options header should contain value DENY
    And Response x-xss-protection header should contain value 1; mode=block


# __     __        _  __         _        _     _
# \ \   / /__ _ __(_)/ _|_   _  | |_ __ _| |__ | | ___  ___
#  \ \ / / _ \ '__| | |_| | | | | __/ _` | '_ \| |/ _ \/ __|
#   \ V /  __/ |  | |  _| |_| | | || (_| | |_) | |  __/\__ \
#    \_/ \___|_|  |_|_|  \__, |  \__\__,_|_.__/|_|\___||___/
#                        |___/
Verify addresses table
    [Tags]           codetables  matrix
    [Documentation]  VIPS address types.
    Given Get keys from addresses table
    Then Should be equal as strings  ${TEST_TABLE}  ['BUSI', 'MAIL', 'RES']
    And Set Global Variable  ${TABLE_ADDRESSES}  ${TEST_TABLE}

Verify contactMethods table
    [Tags]           codetables  matrix
    [Documentation]  VIPS contact methods.
    Given Get keys from contactMethods table
    Then Should be equal as strings  ${TEST_TABLE}  ['EM', 'FAX', 'PHO']
    And Set Global Variable  ${TABLE_CONTACTMETHODS}  ${TEST_TABLE}

Verify countries table
    [Tags]           codetables  matrix
    [Documentation]  VIPS countries.
    Given Get keys from countries table
    Then Should be equal as strings  ${TEST_TABLE}  ['CAN', 'MEX', 'OTH', 'USA']
    And Set Global Variable  ${TABLE_COUNTRIES}  ${TEST_TABLE}

Verify data_sources table
    [Tags]           codetables  matrix
    [Documentation]  VIPS data sources.
    Given Get keys from data_sources table
    Then Should be equal as strings  ${TEST_TABLE}  ['CONM', 'CON', 'VIPS', 'ICBC']
    And Set Global Variable  ${TABLE_DATA_SOURCES}  ${TEST_TABLE}

Verify decisionOutcomes table
    [Tags]           codetables  matrix
    [Documentation]  VIPS outcomes for appeals.
    Given Get ADP keys from decisionOutcomes section
    Then Should be equal as strings  ${TEST_TABLE}  ['SUCC', 'UNSUCC']
    Given Get IRP keys from decisionOutcomes section
    Then Should be equal as strings  ${TEST_TABLE}  ['SUCC', 'UNSUCC']
    Given Get UL keys from decisionOutcomes section
    Then Should be equal as strings  ${TEST_TABLE}  ['SUCC', 'UNSUCC']
    Given Get IMP keys from decisionOutcomes section
    Then Should be equal as strings  ${TEST_TABLE}  ['SUCC', 'UNSUCC']
    # Each is the same, so only make one variable for decisionOutcomes
    And Set Global Variable  ${TABLE_DECISIONOUTCOMES}  ${TEST_TABLE}

Verify disposalActs table
    [Tags]           codetables  matrix
    [Documentation]  VIPS vehicle disposal acts.
    Given Get keys from disposalActs table
    Then Should be equal as strings  ${TEST_TABLE}  ['EDA', 'MVDACT', 'UNK', 'WLACT']
    And Set Global Variable  ${TABLE_DISPOSALACTSS}  ${TEST_TABLE}

Verify documentNotices table
    [Tags]           codetables  matrix
    [Documentation]  VIPS decision outcomes for prohibitions/impoundments.
    Given Get keys from documentNotices table with documentTypeCd
    Then Should be equal as strings  ${TEST_TABLE}  ['MV2689A', 'REVIEW', 'MV2716', 'MV2705', 'MV2687', 'MV2726', 'MV2727', 'ASDCAL', 'ATTACHMENT', 'MV2702A', 'BACREP', 'CERTQLFTEC', 'CERT', 'MV2708', 'MV2688', 'NONE', 'DRENRSMRT', 'ABSTRACT', 'MV2689', 'DINFLEV', 'MV2729', 'DREEVCRT', 'FAXCSADP', 'FAXCSIRP', 'FAXILODNGR', 'FAXILOUPGR', 'FAXREGOUPD', 'FAXURGREQ', 'MV2718', 'MV0728', 'MV2608', 'MV2721', 'MV2701', 'MV2717', 'MV2685DG', 'MV2685', 'MV2723', 'MV2725', 'MV2713A', 'MV2713B', 'MV2715', 'OTHER', 'MV2712', 'ADP250', 'PICKUP', 'POLLETTER', 'POLICE', 'POLSUPREP', 'POREPORT', 'MV2722', 'MV2702RV', 'MV2702RADG', 'MV2702RA', 'MV2724', 'MV2709', 'RQDOCARADP', 'RQDOCARIRP', 'REQDOCIRP', 'REQDOCMOC', 'MV0727', 'MV2711', 'STNDRDFST', 'MV2686', 'MV2728', 'MV0726', 'MV2703', 'MV2704', 'TOXREP', 'MV2710', 'IMPDOWNAR', 'IMPDOWNMOC', 'IMPUPGD', 'MV2707', 'MV2707A', 'VTICKET']
    And Set Global Variable  ${TABLE_DOCUMENTNOTICES}  ${TEST_TABLE}

Verify documents table
    [Tags]           codetables  matrix
    [Documentation]  VIPS documentation and forms.
    Given Get ADP keys from documents section
    Then Should be equal as strings  ${TEST_TABLE}  ['MV2689A', 'REVIEW', 'MV2687', 'ATTACHMENT', 'MV2702A', 'BACREP', 'CERT', 'CERTQLFTEC', 'MV2688', 'DRENRSMRT', 'ABSTRACT', 'MV2689', 'DINFLEV', 'DREEVCRT', 'FAXCSADP', 'FAXURGREQ', 'MV2608', 'MV2721', 'MV2685DG', 'MV2685', 'MV2725', 'OTHER', 'POREPORT', 'POLLETTER', 'POLICE', 'POLSUPREP', 'MV2722', 'MV2702RADG', 'MV2702RA', 'RQDOCARADP', 'REQDOCMOC', 'STNDRDFST', 'MV2686', 'TOXREP', 'VTICKET']
    And Set Global Variable  ${TABLE_DOCUMENTS_ADP}  ${TEST_TABLE}
    Given Get IRP keys from documents section
    Then Should be equal as strings  ${TEST_TABLE}  ['ASDCAL', 'REVIEW', 'MV2726', 'ATTACHMENT', 'MV2702A', 'ABSTRACT', 'FAXCSIRP', 'FAXURGREQ', 'MV2608', 'MV2721', 'MV2723', 'MV2725', 'POLLETTER', 'POLICE', 'POLSUPREP', 'MV2722', 'MV2724', 'RQDOCARIRP', 'REQDOCIRP', 'REQDOCMOC', 'MV2686', 'VTICKET']
    And Set Global Variable  ${TABLE_DOCUMENTS_IRP}  ${TEST_TABLE}
    Given Get UL keys from documents section
    Then Should be equal as strings  ${TEST_TABLE}  ['REVIEW', 'MV2727', 'ATTACHMENT', 'MV2702A', 'ABSTRACT', 'FAXURGREQ', 'MV2721', 'MV2725', 'POLLETTER', 'POLICE', 'POLSUPREP', 'MV2722', 'REQDOCMOC', 'MV2686', 'VTICKET']
    And Set Global Variable  ${TABLE_DOCUMENTS_UL}  ${TEST_TABLE}
    Given Get IMP keys from documents section
    Then Should be equal as strings  ${TEST_TABLE}  ['ASDCAL', 'REVIEW', 'MV2705', 'MV2716', 'ATTACHMENT', 'MV2702A', 'MV2708', 'MV2729', 'FAXILODNGR', 'FAXILOUPGR', 'FAXREGOUPD', 'FAXURGREQ', 'MV2718', 'MV0728', 'MV2721', 'MV2701', 'MV2717', 'MV2713A', 'MV2713B', 'MV2715', 'OTHER', 'MV2712', 'ADP250', 'PICKUP', 'POLLETTER', 'POLICE', 'POLSUPREP', 'MV2722', 'MV2702RV', 'MV2724', 'MV2709', 'MV2711', 'REQDOCMOC', 'MV0727', 'MV2686', 'MV2728', 'MV0726', 'MV2703', 'MV2704', 'MV2707', 'MV2707A', 'MV2710', 'IMPDOWNAR', 'IMPDOWNMOC', 'IMPUPGD', 'VTICKET']
    And Set Global Variable  ${TABLE_DOCUMENTS_IMP}  ${TEST_TABLE}

Verify dreEvaluations table
    [Tags]           codetables  matrix
    [Documentation]  VIPS Sobriety tests.
    Given Get ADP keys from dreEvaluations section
    Then Should be equal as strings  ${TEST_TABLE}  ['ALCOHO', 'CNSDEP', 'CNSSTM', 'CANNAB', 'DISANE', 'HALLUC', 'INHALA', 'NARANA', 'NOTAFF', 'TERREF']
    And Set Global Variable  ${TABLE_DREEVALUALUATIONS_ADP}  ${TEST_TABLE}
    Given Get IRP keys from dreEvaluations section
    Then Should be equal as strings  ${TEST_TABLE}  []
    And Set Global Variable  ${TABLE_DREEVALUALUATIONS_IRP}  ${TEST_TABLE}
    Given Get UL keys from dreEvaluations section
    Then Should be equal as strings  ${TEST_TABLE}  []
    And Set Global Variable  ${TABLE_DREEVALUALUATIONS_UL}  ${TEST_TABLE}
    Given Get IMP keys from dreEvaluations section
    Then Should be equal as strings  ${TEST_TABLE}  []
    And Set Global Variable  ${TABLE_DREEVALUALUATIONS_IMP}  ${TEST_TABLE}

Verify driverLicenceOffices table
    [Documentation]  ICBC office locations.
    JSON structure driverLicenceOffices should have at least 50 records   # ICBC offices in BC
    And Set Global Variable  ${TABLE_DRIVERLICENCEOFFICES}  ${TEST_TABLE}

Verify groundsDecisions table
    [Tags]           codetables  matrix
    [Documentation]  VIPS decision reasons.
    Given Get keys from groundsDecisions table with reviewAppTypeCd
    Then Should be equal as strings  ${TEST_TABLE}  ['ADP', 'CMPSN', 'DISPOSAL', 'EARLYDSPSL', 'ECONHSHP', 'IRP', 'OWNPRDDISP', 'OWNDRVR', 'OWNNOTDRVR', 'STREETRACE', 'UL']
    And Set Global Variable  ${TABLE_GROUNDSDECISION}  ${TEST_TABLE}

Verify impoundLotOperators table
    [Tags]           codetables  matrix
    [Documentation]  BC ILOs.
    Given Get keys from impoundLotOperators table with identityId
    Then Should be equal as strings  ${TEST_TABLE}  [492, 13, 490, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 510, 491, 27, 473, 28, 29, 30, 476, 31, 32, 33, 34, 35, 36, 37, 38, 39, 525, 40, 41, 521, 42, 43, 44, 524, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 483, 63, 526, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 475, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 519, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 485, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 486, 154, 155, 156, 157, 158, 159, 160, 161, 162, 489, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 487, 233, 234, 235, 236, 237, 238, 239, 493, 240, 241, 242, 243, 244, 245, 479, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 484, 272, 273, 274, 275, 276, 523, 277, 527, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 488, 315, 316, 480, 317, 518, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 478, 477, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 482, 357, 358, 359, 360, 361, 481, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 511, 522, 517, 512, 513, 514, 515, 516, 520, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 474, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472]
    And Set Global Variable  ${TABLE_IMPOUNDLOTOPERATORS}  ${TEST_TABLE}


Verify jurisdictions table
    [Tags]           codetables  matrix
    [Documentation]  VIPS legal jurisdictions.
    Given Get keys from jurisdictions table
    Then Should be equal as strings  ${TEST_TABLE}  ['AL', 'AK', 'AB', 'AZ', 'AR', 'BC', 'CA', 'CF', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MB', 'MD', 'MA', 'MX', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NB', 'NH', 'NJ', 'NM', 'NY', 'NF', 'NR', 'NC', 'ND', 'NT', 'NS', 'NU', 'OH', 'OK', 'ON', 'OR', 'FD', 'PA', 'PE', 'PR', 'QC', 'RI', 'SK', 'SC', 'SD', 'TN', 'TX', 'XX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'YT']
    And Set Global Variable  ${TABLE_JURISDICTIONS}  ${TEST_TABLE}


Verify noticePrefixNos table
    [Tags]           codetables  matrix
    [Documentation]  VIPS prohibition number prefixes.
    Given Get ADP keys from noticePrefixNos section
    Then Should be equal as strings  ${TEST_TABLE}  ['00']
    And Set Global Variable  ${TABLE_NOTICEPREFIXNOS_ADP}  ${TEST_TABLE}
    Given Get IRP keys from noticePrefixNos section
    Then Should be equal as strings  ${TEST_TABLE}  ['20', '21', '40']
    And Set Global Variable  ${TABLE_NOTICEPREFIXNOS_IRP}  ${TEST_TABLE}
    Given Get UL keys from noticePrefixNos section
    Then Should be equal as strings  ${TEST_TABLE}  ['30']
    And Set Global Variable  ${TABLE_NOTICEPREFIXNOS_UL}  ${TEST_TABLE}
    Given Get IMP keys from noticePrefixNos section
    Then Should be equal as strings  ${TEST_TABLE}  ['00', '20', '22']
    And Set Global Variable  ${TABLE_NOTICEPREFIXNOS_IMP}  ${TEST_TABLE}

Verify noticeTypes table
    [Tags]           codetables  matrix
    [Documentation]  Prohibition/impoundment notice types.
    Given Get keys from noticeTypes table
    Then Should be equal as strings  ${TEST_TABLE}  ['ADP', 'IRP', 'IMP', 'UL']
    And Set Global Variable  ${TABLE_NOTICETYPES}  ${TEST_TABLE}

Verify originalCauses table
    [Tags]           codetables  matrix
    [Documentation]  Reasons for issuing notices.
    Given Get ADP keys from originalCauses section
    Then Should be equal as strings  ${TEST_TABLE}  ['ADP09410', 'ADP1941A', 'ADP09412', 'ADP09413', 'ADP09411', 'ADP1941B']
    Given Get IRP keys from originalCauses section
    And Set Global Variable  ${TABLE_ORIGINALCAUSES_ADP}  ${TEST_TABLE}
    Then Should be equal as strings  ${TEST_TABLE}  ['IRP3', 'IRP30', 'IRP7', 'IRP90FAIL', 'IRP90REFUS']
    And Set Global Variable  ${TABLE_ORIGINALCAUSES_IRP}  ${TEST_TABLE}
    Given Get UL keys from originalCauses section
    Then Should be equal as strings  ${TEST_TABLE}  ['IRPINDEF']
    And Set Global Variable  ${TABLE_ORIGINALCAUSES_UL}  ${TEST_TABLE}
    Given Get IMP keys from originalCauses section
    Then Should be equal as strings  ${TEST_TABLE}  ['BACWARN3', 'BACWARN30', 'BACWARN7', 'BACFAIL', 'RACE', 'STUNT', 'IDEPPROHIB', 'IDEPUNLIC', 'MCUNLIC', 'EXSPEED', 'MULTIPLE', 'SITTING']
    And Set Global Variable  ${TABLE_ORIGINALCAUSES_IMP}  ${TEST_TABLE}


Verify policeDetachments table
    [Tags]           codetables  matrix
    [Documentation]  Police and RCMP detachments.
    #JSON structure policeDetachments should have at least 250 records
    Given Get keys from policeDetachments table with identityId
    Then Should be equal as strings  ${TEST_TABLE}  [304, 53, 89, 135, 185, 39, 40, 16, 41, 115, 42, 251, 303, 131, 116, 137, 164, 136, 95, 187, 186, 212, 213, 80, 56, 13, 12, 86, 237, 43, 96, 139, 138, 44, 45, 211, 36, 66, 182, 188, 141, 140, 190, 189, 58, 57, 59, 98, 97, 214, 127, 88, 254, 678, 168, 81, 17, 87, 18, 82, 60, 61, 99, 100, 102, 101, 103, 62, 170, 171, 146, 191, 63, 240, 64, 130, 145, 118, 104, 134, 238, 11, 10, 65, 229, 218, 236, 221, 228, 224, 223, 94, 232, 231, 217, 219, 227, 235, 225, 241, 215, 220, 230, 216, 234, 226, 239, 222, 233, 47, 46, 67, 20, 19, 21, 69, 68, 120, 119, 172, 210, 173, 184, 147, 148, 48, 49, 22, 50, 113, 105, 144, 121, 106, 52, 51, 70, 242, 243, 244, 150, 149, 71, 175, 174, 92, 72, 38, 132, 73, 117, 90, 245, 166, 169, 181, 151, 152, 37, 23, 24, 205, 192, 160, 176, 26, 25, 163, 194, 193, 195, 142, 206, 196, 247, 197, 93, 246, 199, 198, 112, 107, 123, 122, 27, 200, 208, 124, 109, 108, 74, 28, 153, 143, 248, 75, 85, 76, 30, 29, 201, 165, 154, 15, 177, 31, 179, 178, 133, 125, 180, 209, 34, 77, 156, 155, 126, 250, 249, 33, 157, 162, 202, 14, 129, 128, 679, 207, 203, 79, 78, 252, 253, 114, 204, 158, 54, 83, 110, 32, 84, 255, 183, 35, 111, 167, 91, 161, 159, 55, 256]
    And Set Global Variable  ${TABLE_POLICEDETACHMENTS}  ${TEST_TABLE}

Verify provinces table
    [Tags]           codetables  matrix
    [Documentation]  Provinces, states, countries.
    Given Get keys from provinces table
    Then Should be equal as strings  ${TEST_TABLE}  ['AL', 'AK', 'AB', 'AZ', 'AR', 'BC', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MB', 'MD', 'MA', 'MX', 'MI', 'MN', 'MS', 'MO', 'MT', 'NA', 'NV', 'NB', 'NH', 'NJ', 'NM', 'NY', 'NL', 'NC', 'ND', 'NT', 'NS', 'NU', 'OH', 'OK', 'ON', 'OR', 'FD', 'PA', 'PE', 'QC', 'RI', 'SK', 'SC', 'SD', 'TS', 'TX', 'UP', 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY', 'YT']
    And Set Global Variable  ${TABLE_PROVINCES}  ${TEST_TABLE}

Verify registration_roles table
    [Tags]           codetables  matrix
    [Documentation]  Vehicle registration roles.
    Given Get keys from registration_roles table
    Then Should be equal as strings  ${TEST_TABLE}  ['DRVR', 'LESE', 'REGOWN']
    And Set Global Variable  ${TABLE_REGISTRATION_ROLES}  ${TEST_TABLE}

Verify releaseReasons table
    [Tags]           codetables  matrix
    [Documentation]  VIPS data sources.
    Given Get keys from releaseReasons table
    Then Should be equal as strings  ${TEST_TABLE}  ['COMPASS', 'RR99', '48IMPEXP', 'IMPEXP', 'OTH', 'NOTDRVR', 'SUCCRVW', 'DLOBT', 'VEHISTLN', 'WRNGIMP']
    And Set Global Variable  ${TABLE_RELEASEREASONS}  ${TEST_TABLE}

Verify reviewApplications table
    [Tags]           codetables  matrix
    [Documentation]  VIPS reasons for application review.
    Given Get ADP keys from reviewApplications section
    Then Should be equal as strings  ${TEST_TABLE}  ['ADP']
    And Set Global Variable  ${TABLE_REVIEWAPPLICATIONS_ADP}  ${TEST_TABLE}
    Given Get IRP keys from reviewApplications section
    Then Should be equal as strings  ${TEST_TABLE}  ['IRP']
    And Set Global Variable  ${TABLE_REVIEWAPPLICATIONS_IRP}  ${TEST_TABLE}
    Given Get UL keys from reviewApplications section
    Then Should be equal as strings  ${TEST_TABLE}  ['UL']
    And Set Global Variable  ${TABLE_REVIEWAPPLICATIONS_UL}  ${TEST_TABLE}
    Given Get IMP keys from reviewApplications section
    Then Should be equal as strings  ${TEST_TABLE}  ['CMPSN', 'DISPOSAL', 'EARLYDSPSL', 'ECONHSHP', 'OWNPRDDISP', 'OWNDRVR', 'OWNNOTDRVR', 'STREETRACE']
    And Set Global Variable  ${TABLE_REVIEWAPPLICATIONS_IMP}  ${TEST_TABLE}

Verify reviewRoles table
    [Tags]           codetables  matrix
    [Documentation]  VIPS roles for reviews.
    Given Get ADP keys from reviewRoles section
    Then Should be equal as strings  ${TEST_TABLE}  ['APPNT', 'AUTHPERS', 'LWYR']
    And Set Global Variable  ${TABLE_REVIEWROLES_ADP}  ${TEST_TABLE}
    Given Get IRP keys from reviewRoles section
    Then Should be equal as strings  ${TEST_TABLE}  ['APPNT', 'AUTHPERS', 'LWYR']
    And Set Global Variable  ${TABLE_REVIEWROLES_IRP}  ${TEST_TABLE}
    Given Get UL keys from reviewRoles section
    Then Should be equal as strings  ${TEST_TABLE}  ['APPNT', 'AUTHPERS', 'LWYR']
    And Set Global Variable  ${TABLE_REVIEWROLES_UL}  ${TEST_TABLE}
    Given Get IMP keys from reviewRoles section
    Then Should be equal as strings  ${TEST_TABLE}  ['AUTHPERS', 'COHAB', 'LWYR', 'REGOWN']
    And Set Global Variable  ${TABLE_REVIEWROLES_IMP}  ${TEST_TABLE}

Verify reviewStatuses table
    [Tags]           codetables  matrix
    [Documentation]  VIPS data sources.
    Given Get keys from reviewStatuses table
    Then Should be equal as strings  ${TEST_TABLE}  ['CNCL', 'CMPL', 'INP']
    And Set Global Variable  ${TABLE_REVIEWSTATUSES}  ${TEST_TABLE}

Verify reviewTypes table
    [Tags]           codetables  matrix
    [Documentation]  VIPS roles for reviews.
    Given Get ADP keys from reviewTypes section
    Then Should be equal as strings  ${TEST_TABLE}  ['ORAL', 'WRIT']
    And Set Global Variable  ${TABLE_REVIEWTYPES_ADP}  ${TEST_TABLE}
    Given Get IRP keys from reviewTypes section
    Then Should be equal as strings  ${TEST_TABLE}  ['ORAL', 'WRIT']
    And Set Global Variable  ${TABLE_REVIEWTYPES_IRP}  ${TEST_TABLE}
    Given Get UL keys from reviewTypes section
    Then Should be equal as strings  ${TEST_TABLE}  ['WRIT']
    And Set Global Variable  ${TABLE_REVIEWTYPES_UL}  ${TEST_TABLE}
    Given Get IMP keys from reviewTypes section
    Then Should be equal as strings  ${TEST_TABLE}  ['ORAL', 'WRIT']
    And Set Global Variable  ${TABLE_REVIEWTYPES_ADP}  ${TEST_TABLE}

Verify scheduleAppTypes table
    [Tags]           codetables  matrix
    [Documentation]  ADP/IRP and IMP/UL.
    Given Get keys from scheduleAppTypes table with identityId
    Then Should be equal as strings  ${TEST_TABLE}  [1, 2]
    And Set Global Variable  ${TABLE_SCHEDULEAPPTYPES}  ${TEST_TABLE}

Verify unavailabilityReasons table
    [Tags]           codetables  matrix
    [Documentation]  Reasons for review centres not being open.
    Given Get keys from unavailabilityReasons table
    Then Should be equal as strings  ${TEST_TABLE}  ['CLS', 'STAT']
    And Set Global Variable  ${TABLE_UNAVAILABILITYREASONS}  ${TEST_TABLE}

Verify vehicleTypes table
    [Tags]           codetables  matrix
    [Documentation]  VIPS vehicle types.
    Given Get keys from vehicleTypes table
    Then Should be equal as strings  ${TEST_TABLE}  ['6', '2', '5', '3', '1', '4']
    And Set Global Variable  ${TABLE_VEHICLETYPES}  ${TEST_TABLE}


#     _   _       _
#    | | | |_ __ | |__   __ _ _ __  _ __  _   _
#    | | | | '_ \| '_ \ / _` | '_ \| '_ \| | | |
#    | |_| | | | | | | | (_| | |_) | |_) | |_| |
#     \___/|_| |_|_| |_|\__,_| .__/| .__/ \__, |
#                            |_|   |_|    |___/

Codetables GET not logged in
    [Tags]           codetables  unauthenticated    GET    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION}``
    Given An unauthenticated GET request expecting HTTP 401 from /v1/codetables/${CORRELATION}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Codetables OPTIONS not logged in
    [Tags]           codetables    unauthenticated    OPTIONS    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION}``
    Given An unauthenticated OPTIONS request expecting HTTP 401 from /v1/codetables/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Codetables HEAD not logged in
    [Tags]           codetables    unauthenticated    HEAD    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION}``
    Given An unauthenticated HEAD request expecting HTTP 401 from /v1/codetables/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is empty

Codetables DELETE authenticated
    [Tags]           codetables    authenticated    DELETE    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated DELETE request expecting HTTP 500 from /v1/codetables/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'DELETE' not supported"}

Codetables DELETE not logged in
    [Tags]           codetables    unauthenticated    DELETE    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https DELETE digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION}``
    Given An unauthenticated DELETE request expecting HTTP 401 from /v1/codetables/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Codetables PUT authenticated
    [Tags]           codetables    authenticated  PUT    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PUT digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PUT request expecting HTTP 500 from /v1/codetables/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PUT' not supported"}

Codetables PUT not logged in
    [Tags]           codetables    unauthenticated    PUT    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PUT digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION}``
    Given An unauthenticated PUT request expecting HTTP 401 from /v1/codetables/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Codetables POST authenticated
    [Tags]           codetables    authenticated    POST    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/codetables/${CORRELATION} with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'POST' not supported"}

Codetables POST not logged in
    [Tags]           codetables    unauthenticated    POST    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https POST digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION}``
    Given An unauthenticated POST request expecting HTTP 401 from /v1/codetables/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Codetables PATCH authenticated
    [Tags]           codetables    authenticated    PATCH    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PATCH request expecting HTTP 500 from /v1/codetables/${CORRELATION} with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PATCH' not supported"}

Codetables PATCH not logged in
    [Tags]           codetables    unauthenticated    PATCH    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PATCH digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION}``
    Given An unauthenticated PATCH request expecting HTTP 401 from /v1/codetables/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}