import moment from "moment";
import constants from "../config/constants";


export const getters = {

    getAllAvailableForms: state => {
        return state.form_schemas.forms;
    },

    getArrayOfAllFormNames: state => {
        let formNames = [];
        for (let form in state.form_schemas.forms) {
            formNames.push(form)
        }
        return formNames
    },

    getAppVersion: state => {
      return state.version;
    },

    getAllEditedForms: state => {
        let edited_forms = Array();
        for (let form_type in state.forms) {
            for (let form_id in state.forms[form_type]) {
                if ("data" in state.forms[form_type][form_id]) {
                    edited_forms.push(state.forms[form_type][form_id])
                }
            }
        }
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

    getCurrentlyEditedFormData: state => {
        let form_object = state.currently_editing_form_object;
        let root = state.forms[form_object.form_type][form_object.form_id]
        return root.data;
    },

    getAttributeValue: state => id => {
        let form_object = state.currently_editing_form_object;
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!(id in root)) {
            return '';
        }
        return root[id];
    },

    checkBoxStatus: state => (id, value) => {
        let form_object = state.currently_editing_form_object;
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!(id in root)) {
            return false;
        }
        return root[id].includes(value);
    },

    getArrayOfBCCityNames: state => {
        return state.cities;
    },

    getArrayOfAgencies: state => {
        return state.agencies;
    },

    getArrayOfCommonCarColors: state => {
        return state.colors;
    },

    getArrayOfVehicleYears: () => {
        const start = constants.MIN_VEHICLE_YEAR;
        const end = constants.MAX_VEHICLE_YEAR;
        let years = []
        for (var i = start; i <= end; i++) {
            years.push(String(i))
        }
        return years;
    },

    getArrayOfVehicleMakes: state => {
        return state.vehicles.map(v => v.make).filter(_onlyUnique);
    },

    getArrayOfVehicleModels: state => {
        let form_object = state.currently_editing_form_object;
        let make = state.forms[form_object.form_type][form_object.form_id].data.vehicle_make
        let results = state.vehicles.filter( v => v.make === make);
        if (results.length > 0) {
            return results.map( v => String(v.model) )
        } else {
            return []
        }
    },

    getArrayOfVehicleStyles: state => {
        return state.vehicle_styles;
    },

    isRecentProhibitions: state => {
        for (let form_type in state.forms) {
            // console.log('form_type', form_type)
            for (let form_object in state.forms[form_type]) {
                if("data" in state.forms[form_type][form_object]) {
                    // the 'data' attribute is added when the form is first edited
                    return true
                }
            }
        }
        return false
    },

    isFormEditable: state => form_object => {
        return ! (state.forms[form_object.form_type][form_object.form_id].printed_timestamp)
    },

    hasFormBeenPrinted: state => {
        const form_object = state.currently_editing_form_object;
        return Boolean(state.forms[form_object.form_type][form_object.form_id].printed_timestamp)
    },

    getServedStatus: state => form_object => {
        if (state.forms[form_object.form_type][form_object.form_id].printed_timestamp) {
            return "Printed";
        }
        return "Not Printed"
    },

    getPdfFileNameString: state => (form_object, document_type) => {
        let file_extension = ".pdf"
        let root = state.forms[form_object.form_type][form_object.form_id]
        let last_name = root.data.last_name;
        let form_id = root.form_id;
        return last_name + "_" + form_id + "_" + document_type + file_extension;
    },

    getPDFTemplateFileName: state => document_type => {
        let form_object = state.currently_editing_form_object;
        return state.form_schemas.forms[form_object.form_type].documents[document_type].pdf;
    },

    getPagesToPrint: (state, getters) => form_object => {
        let variantList = state.form_schemas.forms[form_object.form_type].documents['all'].variants;
        if ( ! getters.isVehicleImpounded(form_object)) {
            // remove page for impound lot operator if vehicle not impounded
            const index = variantList.indexOf("ilo");
            if (index > -1) {
              variantList.splice(index, 1);
            }
            return variantList
        }
        return variantList
    },

    isVehicleImpounded: state => form_object => {
        return state.forms[form_object.form_type][form_object.form_id].data.vehicle_impounded === "Yes"
    },

    getArrayOfJurisdictions: state => {
        return state.jurisdictions;
    },

    getArrayOfProvinces: state => {
        return state.provinces;
    },

    getArrayOfImpoundLotOperators: state => {
        return state.impound_lot_operators.map( o => o.name + ", " + o.lot_address + ", " + o.city + ", " + o.phone);
    },

    getArrayOfPickupLocations: state => {
        return state.pickup_locations.map( o => o.address + ", " + o.city);
    },

    isDisplayIcbcPlateLookup: (state, getters) => {
        let form_object = state.currently_editing_form_object;
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        return root['plate_province'] === "British Columbia" && getters.isUserAuthorized
    },

    isDisplayIcbcLicenceLookup: (state, getters) => {
        return getters.isLicenceJurisdictionBC && getters.isUserAuthorized;
    },

    isLicenceJurisdictionBC: (state) => {
        let form_object = state.currently_editing_form_object;
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        return root['drivers_licence_jurisdiction'] === "British Columbia"
    },

    corporateOwner: state => {
        let form_object = state.currently_editing_form_object;
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        if( ! root['corporate_owner']) {
            return false;
        }
        return root['corporate_owner'].includes("Owned by corporate entity")
    },

    areNewUniqueIdsRequiredByType: (state, getters) => form_type => {
        console.log("inside areNewUniqueIdsRequiredByType", form_type)
        // Business rules state that X number of forms must be available to use offline
        if (getters.getFormTypeCount[form_type] < constants.MINIMUM_NUMBER_OF_UNIQUE_IDS_PER_TYPE) {
            return true;
        }
        return false
    },

    getFormTypeCount: state => {
        let FormTypeCount = {}
        for (let form_type in state.forms) {
            FormTypeCount[form_type] = 0;
            for (let form_id in state.forms[form_type]) {
                if ( ! ("data" in state.forms[form_type][form_id])) {
                    FormTypeCount[form_type]++
                }

            }
        }
        return FormTypeCount;
    },

    getNextAvailableUniqueIdByType: state => form_type => {
        console.log("inside getNextAvailableUniqueIdByType()", form_type)
        for (let form_id in state.forms[form_type]) {
            if( ! ("data" in state.forms[form_type][form_id])) {
                return form_id
            }
        }
    },

    arrayOfFormsRequiringRenewal: state => {
        let forms = Array();
        for (let form_type in state.forms) {
            for (let form_id in state.forms[form_type]) {
                let form_object = state.forms[form_type][form_id]
                let days_to_expiry = moment(form_object.lease_expiry).diff(moment(), 'days')
                if (! form_object.printed_timestamp && days_to_expiry < constants.UNIQUE_ID_REFRESH_DAYS) {
                    forms.push(form_object)
                }
            }
        }
        return forms
    },

    apiHeader: state => {
        const headers = new Headers();
        headers.set('Content-Type', 'application/json')
        if (state.keycloak.token) {
            headers.set('Authorization', 'Bearer ' + state.keycloak.token)
        }
        return headers
    },

    getKeycloakUsername: state => {
        if (state.keycloak) {
            return state.keycloak.userName;
        }
        return ''
    },

    getAgencyName: state => {
        if (state.keycloak) {
            if (state.keycloak.idTokenParsed) {
                if (state.keycloak.idTokenParsed.bceid_business_name) {
                    return state.keycloak.idTokenParsed.bceid_business_name;
                }
            }
        }
        return ''
    },

    getFormPrintValue: state => (form_object, attribute) => {
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!(attribute in root)) {
            return '';
        }
        return root[attribute].toUpperCase();
    },

    getFormDateTimeString: state => (form_object, [dateString, timeString]) => {
        const root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!(dateString in root && timeString in root)) {
            return '';
        }
        const date_time = moment.tz(root[dateString] + " " + root[timeString], 'YYYYMMDD HHmm', true, constants.TIMEZONE)
        return date_time.format("YYYY-MM-DD HH:mm").toUpperCase()
    },

    getFormDateTime: state => (form_object, [dateString, timeString]) => {
        const root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!(dateString in root && timeString in root)) {
            return '';
        }
        return moment.tz(root[dateString] + " " + root[timeString], 'YYYYMMDD HHmm', true, constants.TIMEZONE)
    },
    getFormPrintRadioValue: state => (form_object, attribute, checked_value) => {
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!(attribute in root)) {
            return false;
        }
        return (root[attribute] === checked_value);
    },

    getFormPrintCheckedValue: state => (form_object, attribute, checked_value) => {
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!(attribute in root)) {
            return '';
        }
        return (root[attribute].includes(checked_value))
    },

    getFormPrintJurisdiction: state => (form_object, attribute) => {
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!(attribute in root)) {
            return '';
        }
        let filteredObject = state.jurisdictions.filter( j => j['objectDsc'] === root[attribute]);
        return filteredObject[0]['objectCd'].toUpperCase()
    },

    isUserAnAdmin: state => {
        if (Array.isArray(state.user_roles)) {
            for (const role of state.user_roles) {
                if ('role_name' in role) {
                    if (role.role_name === 'administrator') {
                        return true
                    }
                }
            }
        }
        return false
    },

    isUserAuthenticated: state => {
        return state.keycloak.authenticated && state.keycloak.ready
    },

    isUserAuthorized: state => {
        if (Array.isArray(state.user_roles)) {
            for (const role of state.user_roles) {
                if ('approved_dt' in role) {
                    if (role.approved_dt) {
                        return true
                    }
                }
            }
        }
        return false
    },

    getAllUsers: state => {
        return state.admin_users
    },


    hasUserApplied: state => {
        if (Array.isArray(state.user_roles)) {
            if (state.user_roles[0].approved_dt === null) {
                return true
            }
        }
        return false
    },

    isAppAvailableToWorkOffline: (state, getters) => {
        return getters.isUserHasAtLeastOneFormId && getters.getArrayOfCommonCarColors.length > 0;
    },

    isUserHasAtLeastOneFormId: (state, getters) => {
        const form_types = getters.getFormTypeCount;
        for (let row in form_types) {
                if (form_types[row] > 0) {
                    return true
                }
            }
        return false
    },

    isDisplayUserNotAuthorizedBanner: (state, getters) => {
        return getters.isUserAuthenticated && ! getters.isUserAuthorized && state.keycloak.ready;
    },

    isDisplayIssueProhibitions: (state, getters) => {
        return getters.isUserAuthorized || getters.isAppAvailableToWorkOffline;
    },

    isDisplayFeedbackBanner: (state, getters) => {
        return getters.isUserAuthorized;
    },

    isDisplayNotLoggedInBanner: (state, getters) => {
        return ! getters.isUserAuthenticated && state.isOnline && getters.isAppAvailableToWorkOffline;
    },

    isDisplaySearchRecentProhibition: (state, getters) => {
        return getters.isUserAuthorized;
    },

    isDisplayWelcomeLoginCard: (state, getters) => {
        return ! getters.isAppAvailableToWorkOffline && ! getters.isUserAuthenticated && state.keycloak.ready;
    },

    isTestAdministeredADSE: (state, getters) => {
      const root = getters.getAttributeValue('test_administered_adse')
      if (Array.isArray(root)) {
        return root.includes("Approved Drug Screening Equipment")
      }
      return false;
    },
    isTestAdministeredSFST: (state, getters) => {
      const root = getters.getAttributeValue('test_administered_sfst')
      if (Array.isArray(root)) {
        return root.includes("Prescribed Physical Coordination Test (SFST)")
      }
      return false;
    },
    isTestAdministeredDRE: (state, getters) => {
      const root = getters.getAttributeValue('test_administered_dre')
      if (Array.isArray(root)) {
        return root.includes("Prescribed Physical Coordination Test (DRE)")
      }
      return false;
    },

    isTestAdministeredASD: (state, getters) => {
      const root = getters.getAttributeValue('test_administered_asd')
      if (Array.isArray(root)) {
        return root.includes("Alco-Sensor FST (ASD)")
      }
      return false;
    },
    isTestAdministeredApprovedInstrument: (state, getters) => {
      const root = getters.getAttributeValue('test_administered_instrument')
      if (Array.isArray(root)) {
        return root.includes("Approved Instrument")
      }
      return false;
    },

    locationOfVehicle: state => (form_object) => {
        let root = state.forms[form_object.form_type][form_object.form_id].data;
        if (!("vehicle_impounded" in root)) {
            return '';
        }
        if (root["vehicle_impounded"] === 'Yes') {
            if(form_object.form_type === '24Hour') {
                return "IMPOUNDED"
            }
            return ''
        }
        if (root["vehicle_impounded"] === 'No') {
            if ("reason_for_not_impounding" in root) {
                return root['reason_for_not_impounding'].toUpperCase()
            }
            return ''
        }
    },


}

function _onlyUnique(value, index, self) {
  return self.indexOf(value) === index;
}

