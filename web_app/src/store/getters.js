import xfdf from "@/helpers/xfdf_generator"

export default {

    getAllAvailableForms: state => {
      return state.form_schemas.forms;
    },

    getAllEditedProhibitionNumbers: state => {
        return state.edited_prohibition_numbers;
    },

    isFormBeingEdited: state => {
        return state.currently_editing_prohibition_number !== null
    },

    getCurrentlyEditedProhibitionNumber: state => {
        return state.currently_editing_prohibition_number;
    },

    getSelectedFormComponent: state => {
        const prohibition_number = state.currently_editing_prohibition_number;
        if (prohibition_number == null) {
            return null;
        }
        console.log("check edited_forms: " + JSON.stringify(state.edited_forms))
        return state.edited_forms[prohibition_number].component;
    },

    getCurrentlyEditedForm: state => {
        console.log('inside getCurrentlyEditedForm')
        const prohibition_number = state.currently_editing_prohibition_number;
        if (prohibition_number == null) {
            return null;
        }
        return state.edited_forms[prohibition_number];
    },

    getAttributeValue: state => id => {
        const root = state.edited_forms[state.currently_editing_prohibition_number].data;
        if (!(id in root)) {
            return '';
        }
        return root[id];
    },

    getArrayOfBCCityNames: state => {
        return state.bc_city_names.city_names;
    },

    getArrayOfCommonCarColors: state => {
        return state.car_colors.car_colors;
    },

    isRecentProhibitions: state => {
        return state.edited_prohibition_numbers.length > 0;
    },

    getSpecificForm: state => prohibition_number => {
        return state.edited_forms[prohibition_number];
    },

    isNetworkOnline: state => {
        return state.isOnline;
    },

    generateXFDF: state => prohibition_number => {
        const key_value_pairs = getKeyValuePairs(state, prohibition_number);
        const pdf_template_name = state.edited_forms[prohibition_number].pdf_template;
        const xml_file = xfdf.generate(pdf_template_name, key_value_pairs)
        console.log('xfdf_xml', xml_file)
        return xml_file
    },

    getXdfFileName: state => prohibition_number => {
        const file_extension = ".xdp"
        const last_name = state.edited_forms[prohibition_number].data.last_name;
        const file_name = last_name + "_" + prohibition_number + file_extension;
        console.log('filename', file_name)
        return file_name
    },

    // getDataValue: state => (prohibition_number, attribute) => {
    //     return state.edited_forms[prohibition_number].data[attribute];
    // },

    getArrayOfProvinces: state => {
        return state.provinces;
    },

    isJurisdictionBC: state => {
        const root = state.edited_forms[state.currently_editing_prohibition_number].data;
        return root['plate_province'] === "BC"
    }

}

function getKeyValuePairs (state, prohibition_number) {
    const form_data = state.edited_forms[prohibition_number].data;
    console.log("getFormKeyValuePairs()", form_data)
    let key_value_pairs = Array();
    for( const object in form_data) {
        key_value_pairs[object] = form_data[object];
    }
    console.log('getKeyValuePairs()', key_value_pairs)
    return key_value_pairs;
}