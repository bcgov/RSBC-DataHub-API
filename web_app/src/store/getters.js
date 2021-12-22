import xfdf from "@/helpers/xfdf_generator"

export default {

    getAllAvailableForms: state => {
      return state.form_schemas.forms;
    },

    getAllEditedProhibitions: state => {
        return state.edited_forms;
    },

    isFormBeingEdited: state => {
        return state.currently_editing_prohibition_index !== null
    },

    getCurrentlyEditedProhibitionIndex: state => {
        return state.currently_editing_prohibition_index;
    },

    getCurrentlyEditedProhibitionNumber: state => {
        return state.edited_forms[state.currently_editing_prohibition_index].data.prohibition_number;
    },

    getSelectedFormComponent: state => {
        let prohibition_index = state.currently_editing_prohibition_index;
        if (prohibition_index == null) {
            return null;
        }
        console.log("check edited_forms: " + JSON.stringify(state.edited_forms))
        return state.edited_forms[prohibition_index].component;
    },

    getCurrentlyEditedForm: state => {
        console.log('inside getCurrentlyEditedForm')
        let prohibition_index = state.currently_editing_prohibition_index;
        if (prohibition_index == null) {
            return null;
        }
        return state.edited_forms[prohibition_index];
    },

    getAttributeValue: state => id => {
        let prohibition_index = state.currently_editing_prohibition_index
        let root = state.edited_forms[prohibition_index].data;
        if (!(id in root)) {
            return '';
        }
        return root[id];
    },

    checkBoxStatus: state => (id, value) => {
        let prohibition_index = state.currently_editing_prohibition_index
        let root = state.edited_forms[prohibition_index].data;
        if (!(id in root)) {
            return false;
        }
        return root[id].includes(value);
    },


    getArrayOfBCCityNames: state => {
        return state.bc_city_names.city_names;
    },

    getArrayOfCommonCarColors: state => {
        return state.car_colors.car_colors;
    },

    isRecentProhibitions: state => {
        return state.edited_forms.length > 0;
    },

    getSpecificForm: state => prohibition_index => {
        return state.edited_forms[prohibition_index];
    },

    isNetworkOnline: state => {
        return state.isOnline;
    },

    isFormEditable: state => prohibition_index => {
        return state.edited_forms[prohibition_index].data.served === false;
    },

    getServedStatus: state => prohibition_index => {
        if (state.edited_forms[prohibition_index].data.served) {
            return "Served";
        }
        return "Not Served"
    },

    generateXFDF: state => prohibition_index => {
        let key_value_pairs = getKeyValuePairs(state, prohibition_index);
        let pdf_template_name = state.edited_forms[prohibition_index].pdf_template;
        let xml_file = xfdf.generate(pdf_template_name, key_value_pairs)
        console.log('xfdf_xml', xml_file)
        return xml_file
    },

    getXdfFileName: state => prohibition_index => {
        let file_extension = ".xdp"
        let last_name = state.edited_forms[prohibition_index].data.last_name;
        let prohibition_number = state.edited_forms[prohibition_index].data.prohibition_number;
        let file_name = last_name + "_" + prohibition_number + file_extension;
        console.log('filename', file_name)
        return file_name
    },

    getArrayOfProvinces: state => {
        return state.provinces;
    },

    isPlateJurisdictionBC: state => {
        let prohibition_index = state.currently_editing_prohibition_index
        let root = state.edited_forms[prohibition_index].data;
        return root['plate_province'] === "BC"
    },

    isLicenceJurisdictionBC: state => {
        let prohibition_index = state.currently_editing_prohibition_index
        let root = state.edited_forms[prohibition_index].data;
        return root['drivers_licence_jurisdiction'] === "BC"
    },

    driverIsNotRegisteredOwner: state => {
        let prohibition_index = state.currently_editing_prohibition_index
        let root = state.edited_forms[prohibition_index].data;
        if( ! root['owner_is_driver']) {
            return false;
        }
        return ! root['owner_is_driver'].includes("Driver is the vehicle owner")
    },

    corporateOwner: state => {
        let prohibition_index = state.currently_editing_prohibition_index
        let root = state.edited_forms[prohibition_index].data;
        if( ! root['corporate_owner']) {
            return false;
        }
        return root['corporate_owner'].includes("Owned by corporate entity")
    },

}

function getKeyValuePairs (state, prohibition_index) {
    console.log("getKeyValuePairs(): ", prohibition_index)
    let form_data = state.edited_forms[prohibition_index].data;
    console.log("getFormKeyValuePairs()", form_data)
    let key_value_pairs = Array();
    for( let object in form_data) {
        key_value_pairs[object] = form_data[object];
    }
    console.log('getKeyValuePairs()', key_value_pairs)
    return key_value_pairs;
}
