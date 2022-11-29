/* eslint-disable @typescript-eslint/class-name-casing */

export interface adminUserInfoType {
    userGuid: string;
    roleName: string;
}

export interface loadedInfoType {    
    agencies: boolean;
    impoundLotOperators: boolean;
    countries: boolean;
    jurisdictions: boolean;
    provinces: boolean;
    cities: boolean;
    vehicles: boolean;
    vehicleStyles: boolean;
    configuration: boolean;      
}

export interface userInfoType {    
    agency: string;
    badgeNumber: string;
    firstName: string;
    lastName: string;
    userGuid: string;
    username: string;      
}

export interface jurisdictionInfoType {    
    objectCd: string;
    objectDsc: string;
}

export interface cityInfoType {    
    objectCd: string;
    objectDsc: string;
}

export interface provinceInfoType {    
    objectCd: string;
    objectDsc: string;
}

export interface countryInfoType {    
    objectCd: string;
    objectDsc: string;
}

export interface configurationInfoType {
    environment: string;
}

export interface currentlyEditingFormObjectInfoType {
    form_type: string;
    form_id: string;
}

export interface formsInfoType {
    IRP: any;
    TwentyFourHour: any;
    TwelveHour: any;
    VI: any;
}

export interface impoundLotOperatorsInfoType {
    city: string;
    lot_address: string;
    name: string;
    phone: string;
}

export interface pickupLocationInfoType {
    city: string;
    address: string;
    name?: string;
    phone?: string;
}

export interface userRoleInfoType {
    approvedDate: string;
    roleName: string;
    submittedDate: string;
    userGuid: string;
}

export interface vehicleInfoType {
    md: string;
    mk: string;
    search: string;
}

export interface vehicleStyleInfoType {
    code: string;
    name: string;   
}

export interface vehicleColourInfoType {
    code: string;
    display_name: string;
    colour_class?: string;
}