import moment from "moment";
import constants from "../config/constants";
import nestedFunctions from "@/helpers/nestedFunctions";
import checkDigit from "@/helpers/checkDigit";
export const getters = {

    getAllAvailableForms: state => {
        return state.form_schemas.forms;
    },

    getArrayOfAllFormNames: state => {
        let formNames = [];
        for (let form in state.form_schemas.forms) {
            formNames.push(form);
        }
        return formNames;
    },

    getAppVersion: state => {
        return state.version;
    },

    getAllEditedForms: state => {
        let edited_forms = Array();
        for (let form_type in state.forms) {
            for (let form_id in state.forms[form_type]) {
                // if ("data" in state.forms[form_type][form_id] && !state.forms[form_type][form_id].printed_timestamp) {
                if ("data" in state.forms[form_type][form_id]) {
                    edited_forms.push(state.forms[form_type][form_id]);
                }
            }
        }
        // display incomplete forms first
        edited_forms.sort(function(a, b){
            return new Date(a.printed_timestamp) - new Date(b.printed_timestamp);
        });
        return edited_forms;
    },

    getCurrentlyEditedFormObject: state => {
        return state.currently_editing_form_object;
    },

    getCurrentlyEditedFormId: state => {
        return state.currently_editing_form_object.form_id;
    },

    getFormData: state => (form_type, form_id) => {
        return state.forms[form_type][form_id].data;
    },

    getForm: state => (form_type, form_id) => {
        return state.forms[form_type][form_id];
    },

    getCurrentlyEditedFormData: state => {
        let form_object = state.currently_editing_form_object;
        let root = state.forms[form_object.form_type][form_object.form_id];
        return root.data;
    },

    getCurrentlyEditedForm: state => {
        let form_object = state.currently_editing_form_object;
        return state.forms[form_object.form_type][form_object.form_id];
    },

    getAttributeValue: state => (path, id) => {
        let pathArray = path.split("/");
        pathArray.push(id);
        return nestedFunctions.getProp(state, pathArray);
    },

    doesAttributeExist: state => (path, id) => {
        let pathArray = path.split("/");
        pathArray.push(id);
        const value = nestedFunctions.getProp(state, pathArray);
        return value !== undefined;
    },

    checkBoxStatus: state => (path, id, value) => {
        let pathArray = path.split("/");
        pathArray.push(id);
        const stateValue = nestedFunctions.getProp(state, pathArray);
        if (stateValue) {
            return stateValue.includes(value);
        }
        return false;
    },

    getArrayOfBCCityObjects: state => {
        return state.cities;
    },

    getArrayOfAgencies: state => {
        return state.agencies;
    },

    getArrayOfVehicleYears: () => {
        const start = constants.MIN_VEHICLE_YEAR;
        const end = constants.MAX_VEHICLE_YEAR;
        let years = [];
        for (let i = start; i <= end; i++) {
            years.push(String(i));
        }
        return years.reverse();
    },

    getArrayOfVehicleSearchString: state => {
        return state.vehicles.map(v => v.search);
    },

    getArrayOfVehicleMakeModel: state => {
        return state.vehicles;
    },

    getArrayOfVehicleStyles: state => {
        return state.vehicle_styles;
    },

    isRecentProhibitions: state => {
        for (let form_type in state.forms) {
            for (let form_object in state.forms[form_type]) {
                if ("data" in state.forms[form_type][form_object]) {
                    // the 'data' attribute is added when the form is first edited
                    return true;
                }
            }
        }
        return false;
    },

    isFormEditable: state => form_object => {
        return !state.forms[form_object.form_type][form_object.form_id].printed_timestamp;
    },

    hasFormBeenPrinted: state => {
        const form_object = state.currently_editing_form_object;
        return Boolean(state.forms[form_object.form_type][form_object.form_id].printed_timestamp);
    },

    getServedStatus: state => form_object => {
        if (state.forms[form_object.form_type][form_object.form_id].printed_timestamp) {
            return "Printed";
        }
        return "Not Printed";
    },

    getPdfFileNameString: state => (form_object, document_type) => {
        let file_extension = ".pdf";
        let root = state.forms[form_object.form_type][form_object.form_id];
        let last_name = root.data.last_name;
        let form_id = root.form_id;
        return last_name + "_" + form_id + "_" + document_type + file_extension;
    },

    getPDFTemplateFileName: state => document_type => {
        let form_object = state.currently_editing_form_object;
        return state.form_schemas.forms[form_object.form_type].documents[document_type].pdf;
    },

    getDocumentsToPrint: state => form_type => {
        return state.form_schemas.forms[form_type].documents;
    },

    isVehicleImpounded: (state, getters) => path => {
        return getters.doesAttributeExist(path, "vehicle_impounded_yes");
    },

    getArrayOfJurisdictions: state => {
        return state.jurisdictions;
    },

    getArrayOfProvinces: state => {
        return state.provinces;
    },

    getArrayOfProvinceNames: state => {
        return state.provinces.map(o => o.objectDsc);
    },

    getProvinceObjectByName: state => name => {
        const results = state.provinces.filter(o => o.objectDsc === name);
        if (results.length > 0) {
            return results[0];
        }
        return {};
    },

    getImpoundLotOperatorObject: state => ilo_string => {
        const results = state.impound_lot_operators.filter(o =>
            o.name + ", " + o.lot_address + ", " + o.city + ", " + o.phone === ilo_string
        );
        if (results.length > 0) {
            return results[0];
        }
        return {};
    },

    getJurisdictionByFullName: state => name => {
        const results = state.jurisdictions.filter(o =>
            o.objectDsc === name
        );
        if (results.length > 0) {
            return results[0];
        }
        return {};
    },

    getArrayOfImpoundLotOperators: state => {
        return state.impound_lot_operators.map(o => o.name + ", " + o.lot_address + ", " + o.city + ", " + o.phone);
    },

    getArrayOfPickupLocations: state => {
        return state.pickup_locations.map(o => o.address + ", " + o.city);
    },

    isDisplayIcbcPlateLookup: (state, getters) => {
        let form_object = state.currently_editing_form_object;
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        if ('plate_province' in root) {
            if ('objectDsc' in root['plate_province']) {
                return root['plate_province'].objectCd === "BC" && getters.isUserAuthorized;
            }
        }
    },

    isDisplayIcbcLicenceLookup: (state, getters) => {
        return getters.isLicenceJurisdictionBC && getters.isUserAuthorized;
    },

    isLicenceJurisdictionBC: (state) => {
        let form_object = state.currently_editing_form_object;
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        if (root['drivers_licence_jurisdiction']) {
            if ("objectDsc" in root['drivers_licence_jurisdiction']) {
                return root['drivers_licence_jurisdiction'].objectCd === "BC";
            }
        }

        return false;
    },

    getNumberOfUniqueIdsRequired: (state, getters) => form_type => {
        const numberRequired = constants.MINIMUM_NUMBER_OF_UNIQUE_IDS_PER_TYPE - getters.getFormTypeCount[form_type];
        if (state.form_schemas.forms[form_type].disabled || numberRequired <= 0) {
            return 0;
        } else {
            return numberRequired;
        }
    },

    getFormTypeCount: state => {
        let FormTypeCount = {};
        for (let form_type in state.forms) {
            FormTypeCount[form_type] = 0;
            for (let form_id in state.forms[form_type]) {
                if (!("data" in state.forms[form_type][form_id])) {
                    FormTypeCount[form_type]++;
                }

            }
        }
        return FormTypeCount;
    },

    getNextAvailableUniqueIdByType: state => form_type => {
        for (let form_id in state.forms[form_type]) {
            if (!("data" in state.forms[form_type][form_id])) {
                return form_id;
            }
        }
    },

    arrayOfFormsRequiringRenewal: state => {
        let forms = Array();
        for (let form_type in state.forms) {
            for (let form_id in state.forms[form_type]) {
                let form_object = state.forms[form_type][form_id];
                let days_to_expiry = moment(form_object.lease_expiry).diff(moment(), 'days');
                if (!form_object.printed_timestamp && days_to_expiry < constants.UNIQUE_ID_REFRESH_DAYS) {
                    forms.push(form_object);
                }
            }
        }
        return forms;
    },

    apiHeader: state => {
        const headers = new Headers();
        headers.set('Content-Type', 'application/json');
        if (state.keycloak.token) {
            headers.set('Authorization', 'Bearer ' + state.keycloak.token);
        }
        return headers;
    },

    getKeycloakUsername: state => {
        if (state.keycloak) {
            return state.keycloak.fullName;
        }
        return '';
    },

    getAgencyName: state => {
        if (state.keycloak) {
            if (state.keycloak.idTokenParsed) {
                if (state.keycloak.idTokenParsed.bceid_business_name) {
                    return state.keycloak.idTokenParsed.bceid_business_name;
                }
            }
        }
        return '';
    },

    getFormPrintValue: state => (form_object, attribute) => {
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!(attribute in root)) {
            return '';
        }
        return root[attribute].toUpperCase();
    },

    getFormPrintListValues: state => (form_object, attribute) => {
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!(attribute in root)) {
            return '';
        }
        return root[attribute].join(" and ").toUpperCase();
    },

    getFormDateTimeString: state => (form_object, [dateString, timeString]) => {
        const root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!(dateString in root && timeString in root)) {
            return '';
        }
        const date_time = moment.tz(root[dateString] + " " + root[timeString], 'YYYYMMDD HHmm', true, constants.TIMEZONE);
        return date_time.format("YYYY-MM-DD HH:mm");
    },

    getFormPrintDate: state => (form_object, dateString) => {
        const root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!(dateString in root)) {
            return '';
        }
        const date_time = moment(root[dateString], 'YYYYMMDD', true);
        return date_time.format("YYYY-MM-DD");
    },

    getFormDateTime: state => (form_object, [dateString, timeString]) => {
        const root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!(dateString in root && timeString in root)) {
            return '';
        }
        return moment.tz(root[dateString] + " " + root[timeString], 'YYYYMMDD HHmm', true, constants.TIMEZONE);
    },
    getFormPrintRadioValue: state => (form_object, attribute, checked_value) => {
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!(attribute in root)) {
            return false;
        }
        return root[attribute] === checked_value;
    },

    getFormPrintCheckedValue: state => (form_object, attribute, checked_value) => {
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!(attribute in root)) {
            return '';
        }
        return root[attribute].includes(checked_value);
    },

    getFormPrintJurisdiction: state => (form_object, attribute) => {
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!(attribute in root)) {
            return '';
        }
        let filteredObject = state.jurisdictions.filter(j => j === root[attribute]);
        return filteredObject[0]['objectCd'].toUpperCase();
    },

    isUserAnAdmin: state => {
        if (Array.isArray(state.user_roles)) {
            for (const role of state.user_roles) {
                if ('role_name' in role) {
                    if (role.role_name === 'administrator') {
                        return true;
                    }
                }
            }
        }
        return false;
    },

    isUserAuthenticated: state => {
        return state.keycloak.authenticated && state.keycloak.ready;
    },

    isUserAuthorized: state => {
        return state.isUserAuthorized;
    },

    getAllUsers: state => {
        return state.admin_users;
    },

    hasUserApplied: state => {
        if (Array.isArray(state.user_roles)) {
            if (state.user_roles[0].approved_dt === null) {
                return true;
            }
        }
        return false;
    },

    isAppAvailableToWorkOffline: (state, getters) => {
        return getters.isUserHasAtLeastOneFormId;
    },

    isUserHasAtLeastOneFormId: (state, getters) => {
        const form_types = getters.getFormTypeCount;
        for (let row in form_types) {
            if (form_types[row] > 0) {
                return true;
            }
        }
        return false;
    },

    isDisplayUserNotAuthorizedBanner: (state, getters) => {
        return getters.isUserAuthenticated && getters.isUserAuthorized === false && state.keycloak.ready;
    },

    isDisplayIssueProhibitions: (state, getters) => {
        return getters.allResourcesLoaded && (getters.isUserAuthorized || getters.isAppAvailableToWorkOffline);
    },

    isDisplayFeedbackBanner: (state, getters) => {
        return getters.isUserAuthorized;
    },

    isDisplayNotLoggedInBanner: (state, getters) => {
        return !getters.isUserAuthenticated && state.isOnline && getters.isAppAvailableToWorkOffline;
    },

    isDisplaySearchRecentProhibition: (state, getters) => {
        return getters.isUserAuthorized;
    },

    isDisplayWelcomeLoginCard: (state, getters) => {
        return !getters.isAppAvailableToWorkOffline && !getters.isUserAuthenticated && state.keycloak.ready;
    },

    isTestAdministeredADSE: (state, getters) => (path) => {
        const root = getters.getAttributeValue(path, 'test_administered_adse');
        if (Array.isArray(root)) {
            return root.includes("Approved Drug Screening Equipment");
        }
        return false;
    },
    isTestAdministeredSFST: (state, getters) => (path) => {
        const root = getters.getAttributeValue(path, 'test_administered_sfst');
        if (Array.isArray(root)) {
            return root.includes("Prescribed Physical Coordination Test (SFST)");
        }
        return false;
    },
    isTestAdministeredDRE: (state, getters) => (path) => {
        const root = getters.getAttributeValue(path, 'test_administered_dre');
        if (Array.isArray(root)) {
            return root.includes("Prescribed Physical Coordination Test (DRE)");
        }
        return false;
    },

    isTestAdministeredASD: (state, getters) => (path) => {
        const root = getters.getAttributeValue(path, 'test_administered_asd');
        if (Array.isArray(root)) {
            return root.includes("Alco-Sensor FST (ASD)");
        }
        return false;
    },
    isTestAdministeredApprovedInstrument: (state, getters) => (path) => {
        const root = getters.getAttributeValue(path, 'test_administered_instrument');
        if (Array.isArray(root)) {
            return root.includes("Approved Instrument");
        }
        return false;
    },

    locationOfVehicle: state => (form_object) => {
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!("vehicle_impounded" in root)) {
            return '';
        }
        if (root["vehicle_impounded"] === 'Yes') {
            if (form_object.form_type === '24Hour') {
                return "IMPOUNDED";
            }
            return '';
        }
        if (root["vehicle_impounded"] === 'No') {
            if ("reason_for_not_impounding" in root) {
                return root['reason_for_not_impounding'].toUpperCase();
            }
            return '';
        }
    },

    getCurrentUserObject: state => {
        return state.users;
    },

    getEnvironment: state => {
        return state.configuration.environment;
    },

    getFormIdCheckDigit: state => form_object => {
        if (state.form_schemas.forms[form_object.form_type].check_digit) {
            const sixDigitString = form_object.form_id.substr(2, 7);
            return checkDigit.checkDigit(sixDigitString).toString();
        } else {
            return '';
        }
    },

    allResourcesLoaded: state => {
        let status = true;
        for (const key in state.loaded) {
            if (!state.loaded[key]) {
                status = false;
            }
        }
        return status;
    },

};