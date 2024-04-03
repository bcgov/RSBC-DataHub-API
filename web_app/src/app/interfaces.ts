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
    dateOfService: Date;
    hasError: boolean;
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
    consentFile: string | null;
    consentFileName: string | null;
    hasError: boolean;
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
    fileUploadErrorText?: string;
}

export interface Step3InputProps {
    controlIsUl: boolean;
    controlIsIrp: boolean;
    controlIsAdp: boolean;
    isEnabled: boolean;
    hasError: boolean;
    step3DatatoSend: (data: Step3Data) => void;
}

export interface Step3Data {
    ulGrounds: number[];
    irpGroundsList: number[];
    adpGroundsAlcohol: number[];
    adpGroundsDrugs: number[];
    adpGroundsAlcoholDrugs: number[];
    adpGroundsDrugExpert: number[];
    adpGroundsRefusal: number[];
    control6: number;
    hearingRequest: string;
    hasError: boolean;
}

export interface Step4Data {
    signatureApplicantName: string;
    signedDate?: string;
    signatureApplicantErrorText: string;
}

export interface AvailableReviewDates{
    time_slots?: [ { 
        label: string;
        value: string;
    }]
    is_success: boolean;
    error?: string;
}

export interface ActionResponse {
    data: {
        error: string;
        is_success: boolean;
        data?: any;
      }
}

export interface Form3Data {
    controlProhibitionNumber: string;
    isProhibitionNumberValid: boolean;
    controlIsUl: boolean;
    controlIsIrp: boolean;
    controlIsAdp: boolean;
    prohibitionNumberClean: string;
    controlDriverLastName: string;
    applicantRoleSelect: string;
    applicantEmailAddress: string;
    applicantEmailConfirm: string;
    signatureApplicantName: string;
}
