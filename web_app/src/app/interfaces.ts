export interface Step1Data {
    controlProhibitionNumber: string;
    controlIsUl: boolean;
    controlIsIrp: boolean;
    controlIsAdp: boolean;
    prohibitionNumberClean: string;
    licenseSeized: string;
    licenseNoSurrendered: boolean;
    licenseLostOrStolen: boolean;
    licenseNotIssued: boolean;
    irpProhibitionTypeLength: string;
    dateOfService?: Date;
}

export interface Step1DataErrors {
    controlProhibitionNumber?: string;
    controlIsUl?: boolean;
    controlIsIrp?: boolean;
    controlIsAdp?: boolean;
    prohibitionNumberClean?: string;
    licenseSeized?: string;
    licenseNoSurrendered?: boolean;
    licenseLostOrStolen?: boolean;
    licenseNotIssued?: boolean;
    irpProhibitionTypeLength?: string;
    dateOfService?: Date;
}
export interface Step2Data {
    applicantRoleSelect: string;
    representedByLawyer: string;
    applicantFirstName: string;
    applicantLastName: string;
    applicantPhoneNumber: string;
    applicantEmailAddress: string;
    applicantEmailConfirm: string;
    driverFirstName: string;
    driverLastName: string;
    driverBcdl: string;
    bcDriverLicenseNo: string;
    streetAddress: string;
    controlDriverCityTown: string;
    controlDriverProvince?: string;
    controlDriverPostalCode: string;
}

export interface Step2DataErrors {
    applicantRoleSelect?: string;
    representedByLawyer?: string;
    applicantFirstName?: string;
    applicantLastName?: string;
    applicantPhoneNumber?: string;
    applicantEmailAddress?: string;
    applicantEmailConfirm?: string;
    driverFirstName?: string;
    driverLastName?: string;
    driverBcdl?: string;
    bcDriverLicenseNo?: string;
    streetAddress?: string;
    controlDriverCityTown?: string;
    controlDriverProvince?: string;
    controlDriverPostalCode?: string;
}

export interface Step3InputProps {
    controlIsUl: boolean;
    controlIsIrp: boolean;
    controlIsAdp: boolean;
    licenseSeized: boolean;
    step3DatatoSend: (data: Step2Data) => void;
}

export interface AvailableReviewDates{
    label: string
    value: string    
}
