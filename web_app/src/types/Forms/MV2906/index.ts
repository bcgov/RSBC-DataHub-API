import { cityInfoType, impoundLotOperatorsInfoType, jurisdictionInfoType, provinceInfoType, vehicleColourInfoType, vehicleInfoType, vehicleStyleInfoType } from "@/types/Common";

/* eslint-disable @typescript-eslint/class-name-casing */
export interface twelveHourFormDataInfoType {
    
    driversNumber?: string;//drivers_number?: string;
    givenName: string; //first_name: string;
    lastName: string; //last_name: string;
    dob: string;
    driversLicenceJurisdiction: jurisdictionInfoType; //drivers_licence_jurisdiction: jurisdictionInfoType;
    address: string; // address1: string;    
    driverPhoneNumber?: string; //driver_phone?: string;
    driverCity: string; //city: string;
    prohibitionType: string; //Drugs || Alcohol //prohibition_type_12hr_drugs?: any; //prohibition_type_12hr_alcohol?: any;
    driverProvince?: provinceInfoType; //province: provinceInfoType;
    driverPostalCode: string; //postal: string;
    plateProvince: provinceInfoType;//plate_province: provinceInfoType;
    plateNumber: string; //plate_number: string;
    puj_code: provinceInfoType;
    nscNumber: string; //nsc_number: string;
 
    vehicleYear: string; //vehicle_year: string;
    vehicleMake: vehicleInfoType; //vehicle_make: vehicleInfoType;
    vehicleColor: vehicleColourInfoType[]; //vehicle_color: vehicleColourInfoType[];
    
    vehicleImpounded: boolean; 
    impoundLot?: impoundLotOperatorsInfoType;
    locationOfKeys?: string; // With vehicle￼|| With driver
    notImpoundingReason?: string; //Released to other driver || Left at roadside
    releasedDate?: string;
    releasedTime?: string;
    vehicleReleasedTo?: string;
    // vehicle_impounded_yes?:{
    //     impounded_lot_operator: impoundLotOperatorsInfoType;
    //     location_of_keys_vehicle: string;        
    // } ;

    // vehicle_impounded_no?: {
    //    reason_for_not_impounding_roadside,
    //    reason_for_not_impounding_released:
    //    {
    //      released_date: string;
    //      released_time: string;
    //      vehicle_released_to: string;
    //    }
    // };

    
    offenceAddress: string; //offence_address: string;
    offenceCity: cityInfoType; //offence_city: cityInfoType;
    agencyFileNumber: string; //file_number: string;
    prohibitionStartDate: string; //prohibition_start_date: string;
    prohibitionStartTime: string; //prohibition_start_time: string;
    
    agency: string;
    badge_number: string;
    officer_name: string;
  
    submitted: boolean;    
}

export interface twelveHourFormJsonInfoType {
    component: string;
    form_type: string;
    form_id: string;
    label: string;
    lease_expiry: string;
    description: string;
    data?: twelveHourFormDataInfoType;
    full_name: string;
    printed_timestamp: string;
    documents: twelveHourFormDocumentsInfoType;
    disabled: boolean;
    adminOnly: boolean;
    showCertificate: boolean;
    check_digit: boolean;
}

export interface twelveHourFormDocumentsInfoType {
    all: twelveHourFormAllDocumentsInfoType;
}

export interface twelveHourFormAllDocumentsInfoType {
    name: string;
    reprint: boolean;
    variants: string[];
}

export interface twelveHourFormStatesInfoType {
    driversNumber: null | boolean;
    givenName: null | boolean;
    lastName: null | boolean;
    dob: null | boolean;   
    address: null | boolean;
    driverPhoneNumber: null | boolean;
    driverCity: null | boolean;
    driverProvince: null | boolean;
    driverPostalCode: null | boolean;
    agency: null | boolean;
    badgeNumber: null | boolean;
    driversLicenceJurisdiction: null | boolean;
    officerName: null | boolean;
    plateProvince: null | boolean;    
    plateNumber: null | boolean;
    puj_code: null | boolean; 
    nscNumber: null | boolean; 
    registrationNumber: null | boolean; 
    vehicleYear: null | boolean;
    vehicleMake: null | boolean; 
    vehicleColor: null | boolean;
    vehicleImpounded: null | boolean;    
    locationOfKeys: null | boolean;
    impoundLotName: null | boolean;
    impoundLotAddress: null | boolean;
    impoundLotCity: null | boolean;
    impoundLotPhone: null | boolean;
    notImpoundingReason: null | boolean;    
    vehicleReleasedTo: null | boolean;    
    releasedDate: null | boolean;
    releasedTime: null | boolean;
    prohibitionType: null | boolean;
    offenceAddress: null | boolean;
    offenceCity: null | boolean;
    agencyFileNumber: null | boolean;
    prohibitionStartDate: null | boolean;
    prohibitionStartTime: null | boolean;
    submitted: null | boolean;    
}