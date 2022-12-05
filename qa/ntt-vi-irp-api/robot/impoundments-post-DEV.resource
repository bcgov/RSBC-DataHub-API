*** Variables ***

${body} =  {
...     "vipsImpoundCreate": {
...       "dlJurisdictionCd": "BC",
...       "driverLicenceNo": "1975003",
...       "impoundLotOperatorId": 80, 
...       "impoundmentDt": "2022-11-02T00:01:01.100-07:00",
...       "impoundmentNoticeNo": 22900838,
...       "impoundmentReleaseDt": "six",
...       "noticeSubjectCd": "VEHI",
...       "noticeTypeCd": "IMP",
...       "originalCauseCds": ["STUNT","RACE","BACFAIL"],
...       "policeDetatchmentId": 41,
...       "policeOfficerNm": "RATH",
...       "policeOfficerNo": "DE112",
...       "policeFileNo": "RSI-1234",
...       "projectedReleaseDt": null,
...       "seizureLocationTxt": "Victoria",
...       "vehicleReturnedDt": null
...   },
...     "vipsRegistrationCreateArray": [
...       { 
...       "dataSourceCd": "VIPS",
...       "firstGivenNm": "HARRY",
...       "icbcEnterpriseId": "123",
...       "organizationNm": null,
...       "registrationRoleCd": "REGOWN",
...       "secondGivenNm": "BARRY",
...       "surnameNm": "LUNGPAYNE",
...       "thirdGivenNm": "LARRY",
...       "vipsAddressArray": [
...           {
...           "additionalDeliveryLineTxt": null,
...           "addressFirstLineTxt": "100 Main St",
...           "addressSecondLineTxt": "Green Door",
...           "addressThirdLineTxt": "",
...           "cityNm": "Ashcroft",
...           "countryNm": "CAN",
...           "postalCodeTxt": "V1A2A2",
...           "provinceCd": "BC",
...           "registrationAddressTypeCd": "MAIL"
...           }
...       ],
...       "vipsLicenceCreateObj": {
...           "birthDt": "1975-01-08T00:00:00.000-07:00",
...           "driverLicenceNo": "1975002",
...           "dlJurisdictionCd": "BC"
...       }
...       }
...   ],
...     "vipsVehicleCreate": {
...       "commercialMotorCarrierId": "NSC0123456789",
...       "licencePlateNo": "888HHH",
...       "lpDecalValidYy": 2022,
...       "lpJurisdictionCd": "BC",
...       "manufacturedYy": 1982,
...       "nscJurisdictionTxt": "BC",
...       "registrationNo": "8762133",
...       "vehicleColourTxt": "Brown",
...       "vehicleIdentificationNo": "1G8DC18H4CF114023",
...       "vehicleMakeTxt": "Chevrolet",
...       "vehicleModelTxt": "Blazer",
...       "vehicleStyleTxt": "4DR",
...       "vehicleTypeCd": "1"
...   },
...     "vipsDocumentIdArray": [ 605
...   ],
...     "vipsImpoundmentArray": [
...   ]
...   }

${body_with_non_existent_vipsImpoundmentArray} =  {
...     "vipsImpoundCreate": {
...       "dlJurisdictionCd": "BC",
...       "driverLicenceNo": "1975003",
...       "impoundLotOperatorId": 80, 
...       "impoundmentDt": "2022-11-02T00:01:01.100-07:00",
...       "impoundmentNoticeNo": 22900838,
...       "impoundmentReleaseDt": "six",
...       "noticeSubjectCd": "VEHI",
...       "noticeTypeCd": "IMP",
...       "originalCauseCds": ["STUNT","RACE","BACFAIL"],
...       "policeDetatchmentId": 41,
...       "policeOfficerNm": "RATH",
...       "policeOfficerNo": "DE112",
...       "policeFileNo": "RSI-1234",
...       "projectedReleaseDt": null,
...       "seizureLocationTxt": "Victoria",
...       "vehicleReturnedDt": null
...   },
...     "vipsRegistrationCreateArray": [
...       { 
...       "dataSourceCd": "VIPS",
...       "firstGivenNm": "HARRY",
...       "icbcEnterpriseId": "123",
...       "organizationNm": null,
...       "registrationRoleCd": "REGOWN",
...       "secondGivenNm": "BARRY",
...       "surnameNm": "LUNGPAYNE",
...       "thirdGivenNm": "LARRY",
...       "vipsAddressArray": [
...           {
...           "additionalDeliveryLineTxt": null,
...           "addressFirstLineTxt": "100 Main St",
...           "addressSecondLineTxt": "Green Door",
...           "addressThirdLineTxt": "",
...           "cityNm": "Ashcroft",
...           "countryNm": "CAN",
...           "postalCodeTxt": "V1A2A2",
...           "provinceCd": "BC",
...           "registrationAddressTypeCd": "MAIL"
...           }
...       ],
...       "vipsLicenceCreateObj": {
...           "birthDt": "1975-01-08T00:00:00.000-07:00",
...           "driverLicenceNo": "1975002",
...           "dlJurisdictionCd": "BC"
...       }
...       }
...   ],
...     "vipsVehicleCreate": {
...       "commercialMotorCarrierId": "NSC0123456789",
...       "licencePlateNo": "888HHH",
...       "lpDecalValidYy": 2022,
...       "lpJurisdictionCd": "BC",
...       "manufacturedYy": 1982,
...       "nscJurisdictionTxt": "BC",
...       "registrationNo": "8762133",
...       "vehicleColourTxt": "Brown",
...       "vehicleIdentificationNo": "1G8DC18H4CF114023",
...       "vehicleMakeTxt": "Chevrolet",
...       "vehicleModelTxt": "Blazer",
...       "vehicleStyleTxt": "4DR",
...       "vehicleTypeCd": "1"
...   },
...     "vipsDocumentIdArray": [ 605
...   ],
...     "vipsImpoundmentArray": [ 99999
...   ]
...   }


${body_with_non_existent_document} =  {
...     "vipsImpoundCreate": {
...       "dlJurisdictionCd": "BC",
...       "driverLicenceNo": "1975003",
...       "impoundLotOperatorId": 80, 
...       "impoundmentDt": "2022-11-02T00:01:01.100-07:00",
...       "impoundmentNoticeNo": 22900838,
...       "impoundmentReleaseDt": "six",
...       "noticeSubjectCd": "VEHI",
...       "noticeTypeCd": "IMP",
...       "originalCauseCds": ["STUNT","RACE","BACFAIL"],
...       "policeDetatchmentId": 41,
...       "policeOfficerNm": "RATH",
...       "policeOfficerNo": "DE112",
...       "policeFileNo": "RSI-1234",
...       "projectedReleaseDt": null,
...       "seizureLocationTxt": "Victoria",
...       "vehicleReturnedDt": null
...   },
...     "vipsRegistrationCreateArray": [
...       { 
...       "dataSourceCd": "VIPS",
...       "firstGivenNm": "HARRY",
...       "icbcEnterpriseId": "123",
...       "organizationNm": null,
...       "registrationRoleCd": "REGOWN",
...       "secondGivenNm": "BARRY",
...       "surnameNm": "LUNGPAYNE",
...       "thirdGivenNm": "LARRY",
...       "vipsAddressArray": [
...           {
...           "additionalDeliveryLineTxt": null,
...           "addressFirstLineTxt": "100 Main St",
...           "addressSecondLineTxt": "Green Door",
...           "addressThirdLineTxt": "",
...           "cityNm": "Ashcroft",
...           "countryNm": "CAN",
...           "postalCodeTxt": "V1A2A2",
...           "provinceCd": "BC",
...           "registrationAddressTypeCd": "MAIL"
...           }
...       ],
...       "vipsLicenceCreateObj": {
...           "birthDt": "1975-01-08T00:00:00.000-07:00",
...           "driverLicenceNo": "1975002",
...           "dlJurisdictionCd": "BC"
...       }
...       }
...   ],
...     "vipsVehicleCreate": {
...       "commercialMotorCarrierId": "NSC0123456789",
...       "licencePlateNo": "888HHH",
...       "lpDecalValidYy": 2022,
...       "lpJurisdictionCd": "BC",
...       "manufacturedYy": 1982,
...       "nscJurisdictionTxt": "BC",
...       "registrationNo": "8762133",
...       "vehicleColourTxt": "Brown",
...       "vehicleIdentificationNo": "1G8DC18H4CF114023",
...       "vehicleMakeTxt": "Chevrolet",
...       "vehicleModelTxt": "Blazer",
...       "vehicleStyleTxt": "4DR",
...       "vehicleTypeCd": "1"
...   },
...     "vipsDocumentIdArray": [ 9999
...   ],
...     "vipsImpoundmentArray": [
...   ]
...   }


${body_with_invalid_policeDetachmentId} =  {
...     "vipsImpoundCreate": {
...       "dlJurisdictionCd": "BC",
...       "driverLicenceNo": "1975003",
...       "impoundLotOperatorId": 80, 
...       "impoundmentDt": "2022-11-02T00:01:01.100-07:00",
...       "impoundmentNoticeNo": 22900838,
...       "impoundmentReleaseDt": "six",
...       "noticeSubjectCd": "VEHI",
...       "noticeTypeCd": "IMP",
...       "originalCauseCds": ["STUNT","RACE","BACFAIL"],
...       "policeDetatchmentId": 911,
...       "policeOfficerNm": "RATH",
...       "policeOfficerNo": "DE112",
...       "policeFileNo": "RSI-1234",
...       "projectedReleaseDt": null,
...       "seizureLocationTxt": "Victoria",
...       "vehicleReturnedDt": null
...   },
...     "vipsRegistrationCreateArray": [
...       { 
...       "dataSourceCd": "VIPS",
...       "firstGivenNm": "HARRY",
...       "icbcEnterpriseId": "123",
...       "organizationNm": null,
...       "registrationRoleCd": "REGOWN",
...       "secondGivenNm": "BARRY",
...       "surnameNm": "LUNGPAYNE",
...       "thirdGivenNm": "LARRY",
...       "vipsAddressArray": [
...           {
...           "additionalDeliveryLineTxt": null,
...           "addressFirstLineTxt": "100 Main St",
...           "addressSecondLineTxt": "Green Door",
...           "addressThirdLineTxt": "",
...           "cityNm": "Ashcroft",
...           "countryNm": "CAN",
...           "postalCodeTxt": "V1A2A2",
...           "provinceCd": "BC",
...           "registrationAddressTypeCd": "MAIL"
...           }
...       ],
...       "vipsLicenceCreateObj": {
...           "birthDt": "1975-01-08T00:00:00.000-07:00",
...           "driverLicenceNo": "1975002",
...           "dlJurisdictionCd": "BC"
...       }
...       }
...   ],
...     "vipsVehicleCreate": {
...       "commercialMotorCarrierId": "NSC0123456789",
...       "licencePlateNo": "888HHH",
...       "lpDecalValidYy": 2022,
...       "lpJurisdictionCd": "BC",
...       "manufacturedYy": 1982,
...       "nscJurisdictionTxt": "BC",
...       "registrationNo": "8762133",
...       "vehicleColourTxt": "Brown",
...       "vehicleIdentificationNo": "1G8DC18H4CF114023",
...       "vehicleMakeTxt": "Chevrolet",
...       "vehicleModelTxt": "Blazer",
...       "vehicleStyleTxt": "4DR",
...       "vehicleTypeCd": "1"
...   },
...     "vipsDocumentIdArray": [ 605
...   ],
...     "vipsImpoundmentArray": [
...   ]
...   }


${body_with_bad_dates} =  {
...     "vipsImpoundCreate": {
...       "dlJurisdictionCd": "BC",
...       "driverLicenceNo": "1975003",
...       "impoundLotOperatorId": 80, 
...       "impoundmentDt": "Fri Nov  4 15:35:56 PDT 2022",
...       "impoundmentNoticeNo": 22900838,
...       "impoundmentReleaseDt": "six",
...       "noticeSubjectCd": "VEHI",
...       "noticeTypeCd": "IMP",
...       "originalCauseCds": ["STUNT","RACE","BACFAIL"],
...       "policeDetatchmentId": 41,
...       "policeOfficerNm": "RATH",
...       "policeOfficerNo": "DE112",
...       "policeFileNo": "RSI-1234",
...       "projectedReleaseDt": null,
...       "seizureLocationTxt": "Victoria",
...       "vehicleReturnedDt": null
...   },
...     "vipsRegistrationCreateArray": [
...       { 
...       "dataSourceCd": "VIPS",
...       "firstGivenNm": "HARRY",
...       "icbcEnterpriseId": "123",
...       "organizationNm": null,
...       "registrationRoleCd": "REGOWN",
...       "secondGivenNm": "BARRY",
...       "surnameNm": "LUNGPAYNE",
...       "thirdGivenNm": "LARRY",
...       "vipsAddressArray": [
...           {
...           "additionalDeliveryLineTxt": null,
...           "addressFirstLineTxt": "100 Main St",
...           "addressSecondLineTxt": "Basement Suite",
...           "addressThirdLineTxt": "Green Door",
...           "cityNm": "Ashcroft",
...           "countryNm": "CAN",
...           "postalCodeTxt": "V1A2A2",
...           "provinceCd": "BC",
...           "registrationAddressTypeCd": "MAIL"
...           }
...       ],
...       "vipsLicenceCreateObj": {
...           "birthDt": "1975-01-01",
...           "driverLicenceNo": "1974001",
...           "dlJurisdictionCd": "BC"
...       }
...       }
...   ],
...     "vipsVehicleCreate": {
...       "commercialMotorCarrierId": "NSC0123456789",
...       "licencePlateNo": "888HHH",
...       "lpDecalValidYy": 2022,
...       "lpJurisdictionCd": "BC",
...       "manufacturedYy": 1982,
...       "nscJurisdictionTxt": "BC",
...       "registrationNo": "8762133",
...       "vehicleColourTxt": "Brown",
...       "vehicleIdentificationNo": "1G8DC18H4CF114023",
...       "vehicleMakeTxt": "Chevrolet",
...       "vehicleModelTxt": "Blazer",
...       "vehicleStyleTxt": "4DR",
...       "vehicleTypeCd": "1"
...   },
...     "vipsDocumentIdArray": [ 605
...   ],
...     "vipsImpoundmentArray": [
...   ]
...   }

${body_long_values} =  {
...     "vipsImpoundCreate": {
...       "dlJurisdictionCd": "BC",
...       "driverLicenceNo": "1975003",
...       "impoundLotOperatorId": 80, 
...       "impoundmentDt": "2022-11-02T00:01:01.100-07:00",
...       "impoundmentNoticeNo": 22900838,
...       "impoundmentReleaseDt": "six",
...       "noticeSubjectCd": "VEHI",
...       "noticeTypeCd": "IMP",
...       "originalCauseCds": ["STUNT","RACE","BACFAIL"],
...       "policeDetatchmentId": 41,
...       "policeOfficerNm": "RATH",
...       "policeOfficerNo": "DE112",
...       "policeFileNo": "THIS IS A VERY LONG FILE NUMBER",
...       "projectedReleaseDt": null,
...       "seizureLocationTxt": "Victoria",
...       "vehicleReturnedDt": null
...   },
...     "vipsRegistrationCreateArray": [
...       { 
...       "dataSourceCd": "VIPS",
...       "firstGivenNm": "HARRY",
...       "icbcEnterpriseId": "123",
...       "organizationNm": null,
...       "registrationRoleCd": "REGOWN",
...       "secondGivenNm": "BARRY",
...       "surnameNm": "LUNGPAYNE",
...       "thirdGivenNm": "LARRY",
...       "vipsAddressArray": [
...           {
...           "additionalDeliveryLineTxt": null,
...           "addressFirstLineTxt": "100 Main St",
...           "addressSecondLineTxt": "Basement Suite",
...           "addressThirdLineTxt": "Green Door",
...           "cityNm": "Ashcroft",
...           "countryNm": "CAN",
...           "postalCodeTxt": "V1A2A2",
...           "provinceCd": "BC",
...           "registrationAddressTypeCd": "MAIL"
...           }
...       ],
...       "vipsLicenceCreateObj": {
...           "birthDt": "1975-01-08T00:00:00.000-07:00",
...           "driverLicenceNo": "1975002",
...           "dlJurisdictionCd": "BC"
...       }
...       }
...   ],
...     "vipsVehicleCreate": {
...       "commercialMotorCarrierId": "NSC0123456789",
...       "licencePlateNo": "888HHH",
...       "lpDecalValidYy": 2022,
...       "lpJurisdictionCd": "BC",
...       "manufacturedYy": 1982,
...       "nscJurisdictionTxt": "BC",
...       "registrationNo": "8762133",
...       "vehicleColourTxt": "Brown",
...       "vehicleIdentificationNo": "1G8DC18H4CF114023",
...       "vehicleMakeTxt": "Chevrolet",
...       "vehicleModelTxt": "Blazer",
...       "vehicleStyleTxt": "4DR",
...       "vehicleTypeCd": "1"
...   },
...     "vipsDocumentIdArray": [ 605
...   ],
...     "vipsImpoundmentArray": [
...   ]
...   }


${body_with_missing_impoundmentNoticeNo} =  {
...     "vipsImpoundCreate": {
...       "dlJurisdictionCd": "BC",
...       "driverLicenceNo": "1975003",
...       "impoundLotOperatorId": 80, 
...       "impoundmentDt": "2022-11-02T00:01:01.100-07:00",
...       "impoundmentReleaseDt": "six",
...       "noticeSubjectCd": "VEHI",
...       "noticeTypeCd": "IMP",
...       "originalCauseCds": ["STUNT","RACE","BACFAIL"],
...       "policeDetatchmentId": 41,
...       "policeOfficerNm": "RATH",
...       "policeOfficerNo": "DE112",
...       "policeFileNo": "RSI-1234",
...       "projectedReleaseDt": null,
...       "seizureLocationTxt": "Victoria",
...       "vehicleReturnedDt": null
...   },
...     "vipsRegistrationCreateArray": [
...       { 
...       "dataSourceCd": "VIPS",
...       "firstGivenNm": "HARRY",
...       "icbcEnterpriseId": "123",
...       "organizationNm": null,
...       "registrationRoleCd": "REGOWN",
...       "secondGivenNm": "BARRY",
...       "surnameNm": "LUNGPAYNE",
...       "thirdGivenNm": "LARRY",
...       "vipsAddressArray": [
...           {
...           "additionalDeliveryLineTxt": null,
...           "addressFirstLineTxt": "100 Main St",
...           "addressSecondLineTxt": "Basement Suite",
...           "addressThirdLineTxt": "Green Door",
...           "cityNm": "Ashcroft",
...           "countryNm": "CAN",
...           "postalCodeTxt": "V1A2A2",
...           "provinceCd": "BC",
...           "registrationAddressTypeCd": "MAIL"
...           }
...       ],
...       "vipsLicenceCreateObj": {
...           "birthDt": "1975-01-08T00:00:00.000-07:00",
...           "driverLicenceNo": "1975002",
...           "dlJurisdictionCd": "BC"
...       }
...       }
...   ],
...     "vipsVehicleCreate": {
...       "commercialMotorCarrierId": "NSC0123456789",
...       "licencePlateNo": "888HHH",
...       "lpDecalValidYy": 2022,
...       "lpJurisdictionCd": "BC",
...       "manufacturedYy": 1982,
...       "nscJurisdictionTxt": "BC",
...       "registrationNo": "8762133",
...       "vehicleColourTxt": "Brown",
...       "vehicleIdentificationNo": "1G8DC18H4CF114023",
...       "vehicleMakeTxt": "Chevrolet",
...       "vehicleModelTxt": "Blazer",
...       "vehicleStyleTxt": "4DR",
...       "vehicleTypeCd": "1"
...   },
...     "vipsDocumentIdArray": [ 605
...   ],
...     "vipsImpoundmentArray": [
...   ]
...   }

${body_with_missing_vipsImpoundCreate} =  {
...     "vipsRegistrationCreateArray": [
...       { 
...       "dataSourceCd": "VIPS",
...       "firstGivenNm": "HARRY",
...       "icbcEnterpriseId": "123",
...       "organizationNm": null,
...       "registrationRoleCd": "REGOWN",
...       "secondGivenNm": "BARRY",
...       "surnameNm": "LUNGPAYNE",
...       "thirdGivenNm": "LARRY",
...       "vipsAddressArray": [
...           {
...           "additionalDeliveryLineTxt": null,
...           "addressFirstLineTxt": "100 Main St",
...           "addressSecondLineTxt": "Basement Suite",
...           "addressThirdLineTxt": "Green Door",
...           "cityNm": "Ashcroft",
...           "countryNm": "CAN",
...           "postalCodeTxt": "V1A2A2",
...           "provinceCd": "BC",
...           "registrationAddressTypeCd": "MAIL"
...           }
...       ],
...       "vipsLicenceCreateObj": {
...           "birthDt": "1975-01-08T00:00:00.000-07:00",
...           "driverLicenceNo": "1975002",
...           "dlJurisdictionCd": "BC"
...       }
...       }
...   ],
...     "vipsVehicleCreate": {
...       "commercialMotorCarrierId": "NSC0123456789",
...       "licencePlateNo": "888HHH",
...       "lpDecalValidYy": 2022,
...       "lpJurisdictionCd": "BC",
...       "manufacturedYy": 1982,
...       "nscJurisdictionTxt": "BC",
...       "registrationNo": "8762133",
...       "vehicleColourTxt": "Brown",
...       "vehicleIdentificationNo": "1G8DC18H4CF114023",
...       "vehicleMakeTxt": "Chevrolet",
...       "vehicleModelTxt": "Blazer",
...       "vehicleStyleTxt": "4DR",
...       "vehicleTypeCd": "1"
...   },
...     "vipsDocumentIdArray": [ 605
...   ],
...     "vipsImpoundmentArray": [
...   ]
...   }

${empty_body} =  {}