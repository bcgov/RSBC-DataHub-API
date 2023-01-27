import rsiStore from "@/store"
import constants from "../config/constants";


export function copyIfExists([form_path, source_attribute, destination_attribute]) {
    if (rsiStore.getters.doesAttributeExist(form_path, source_attribute)) {
        rsiStore.commit("updateFormAttribute", [
            form_path,
            destination_attribute,
            rsiStore.getters.getAttributeValue(form_path, source_attribute)])
    }
}


// copy some driver fields to the registered owner fields
// in the event the driver field is null or does not exist, do not copy
export function populateOwnerFromDriver(form_path) {
    // trigger the following mutation
    rsiStore.commit("updateFormAttribute", [form_path, "corp_owner_false", {}])
    copyIfExists([form_path, "last_name", "corp_owner_false/owners_last_name"])
    copyIfExists([form_path, "first_name", "corp_owner_false/owners_first_name"])
    copyIfExists([form_path, "address1", "owners_address1"])
    copyIfExists([form_path, "city", "owners_city"])
    copyIfExists([form_path, "province", "owners_province"])
    copyIfExists([form_path, "postal", "owners_postal"])
    copyIfExists([form_path, "dob", "corp_owner_false/owner_dob"])
    rsiStore.commit("deleteFormAttribute", [form_path, "corp_owner_true" ])
}

export function getArrayOfVehicleYears(){
    const start = Number(constants.MIN_VEHICLE_YEAR);
    const end = Number(constants.MAX_VEHICLE_YEAR);
    const years = []
    for (let i = start; i <= end; i++) {
        years.push(String(i))
    }
    return years.reverse();
}

export function getArrayOfPlateYears(){
    const start = Number(constants.MIN_PLATE_YEAR);
    const end = Number(constants.MAX_PLATE_YEAR);
    const years = []
    for (let i = start; i <= end; i++) {
        years.push(String(i))
    }
    return years.reverse();
}

export function isLicenceJurisdictionBC(){
    const form_object = rsiStore.state.Common.currently_editing_form_object;
    const root = rsiStore.state.forms[form_object.form_type][form_object.form_id].data;
    if (root['drivers_licence_jurisdiction']) {
        if ("objectDsc" in root['drivers_licence_jurisdiction']) {
            return root['drivers_licence_jurisdiction'].objectCd === "BC"
        }
    }

    return false;
}

    