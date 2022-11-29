/* eslint-disable @typescript-eslint/class-name-casing */

import { provinceInfoType, jurisdictionInfoType, vehicleInfoType, vehicleColourInfoType, vehicleStyleInfoType, impoundLotOperatorsInfoType, cityInfoType } from "@/types/Common";

export interface irpFormJsonInfoType {
    component: string;
    form_type: string;
    form_id: string;
    label: string;
    lease_expiry: string;
    description: string;
    data?: irpFormDataInfoType;
    full_name: string;
    printed_timestamp: string;
    documents: irpFormDocumentsInfoType;
    disabled: boolean;
    adminOnly: boolean;
    showCertificate: boolean;
    check_digit: boolean;
}

export interface irpFormDocumentsInfoType {
    all: irpFormAllDocumentsInfoType;
}

export interface irpFormAllDocumentsInfoType {
    name: string;
    reprint: boolean;
    variants: string[];
}


export interface irpFormDataInfoType {

    driversNumber?: string;
    givenName: string;
    lastName: string;
    driverGender: string;
    licenseExpiryYear: string;
    bcdlClass: string;
    dob: string;
    driversLicenceJurisdiction: jurisdictionInfoType;
    address: string;
    driverCity: string;
    driverProvince?: provinceInfoType;
    driverPostalCode: string;

    offenceAddress: string; 
    offenceCity: cityInfoType;   
    prohibitionStartDate: string;
    prohibitionStartTime: string;
    prohibitionTypePeriod: string;

    vehicleImpounded: boolean; 
    viNumber?: string;
    dlSeized: boolean; 
    agency: string;
    badge_number: string;
    officer_name: string;
    submitted: boolean;
}

export interface irpFormStatesInfoType {    
    driversNumber: null | boolean;
    givenName: null | boolean;
    lastName: null | boolean;
    driverGender: null | boolean;
    licenseExpiryYear: null | boolean;
    bcdlClass: null | boolean;
    dob: null | boolean;
    driversLicenceJurisdiction: null | boolean;
    address: null | boolean;
    driverCity: null | boolean;
    driverProvince: null | boolean;
    driverPostalCode: null | boolean;
    offenceAddress: null | boolean;
    offenceCity: null | boolean; 
    prohibitionStartDate: null | boolean;
    prohibitionStartTime: null | boolean;
    prohibitionTypePeriod: null | boolean;
    vehicleImpounded: null | boolean;
    viNumber: null | boolean;
    dlSeized: null | boolean;
    agency: null | boolean;
    badge_number: null | boolean;
    officer_name: null | boolean;
    submitted: null | boolean;
}