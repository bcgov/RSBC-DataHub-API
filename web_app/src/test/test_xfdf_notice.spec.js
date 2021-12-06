import { getters } from '../store/getters.js';
import { createLocalVue } from "@vue/test-utils";
import Vuex from 'vuex';
import { mutations } from "../store/mutations";

let state = {
    "currently_editing_form_object": {
        "form_id": "AA-111111",
        "form_type": "24Hour",
    },
    "forms": {
        "24Hour": {
            "AA-111111": {
                "form_id": "AA-111111",
                "form_type": "24Hour",
                "printed_timestamp": "2021-08-15",
                "lease_expiry": "2021-09-02",
                "data": {}
            }
        }
    }
};

createLocalVue().use(Vuex)
const store = new Vuex.Store({state, mutations, getters})
const document_type = 'notice'

test('test prohibition number, without the prefix, is shown on driver copy', () => {
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['VIOLATION_NUMBER']).toEqual("111111")
})

test('test driver surname is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "Smith", "id": "last_name"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['DRIVER_SURNAME']).toEqual("Smith")
})

test('test driver first name is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "Brian", "id": "first_name"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['DRIVER_GIVEN']).toEqual("Brian")
})

test('test driver licence number is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "5123456", "id": "drivers_number"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['DRIVER_DL_NUMBER']).toEqual("5123456")
})

test('test driver province / state is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "BC", "id": "drivers_licence_jurisdiction"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['DRIVER_DL_PROVINCE']).toEqual("BC")
})

test('test driver date of birth is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "19991231", "id": "dob"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['DRIVER_DOB_YYYY']).toEqual("1999")
    expect(actual['DRIVER_DOB_MM']).toEqual("12")
    expect(actual['DRIVER_DOB_DD']).toEqual("31")
})

test('test driver address is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "123 Main Street", "id": "address1"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['DRIVER_ADDRESS']).toEqual("123 Main Street")
})

test('test driver city is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "Oak Bay", "id": "city"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['DRIVER_CITY']).toEqual("Oak Bay")
})

test('test driver province is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "BC", "id": "province"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['DRIVER_PROVINCE']).toEqual("BC")
})

test('test driver postal code is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "V1A1A1", "id": "postal"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['DRIVER_POSTAL_CODE']).toEqual("V1A1A1")
})

test('test prohibition reason alcohol is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "Alcohol 215(2)", "id": "prohibition_type"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['REASON_ALCOHOL']).toEqual("Yes")
    expect(actual['REASON_DRUGS']).toEqual("")
})

test('test prohibition reason drugs is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "Drugs 215(3)", "id": "prohibition_type"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['REASON_ALCOHOL']).toEqual("")
    expect(actual['REASON_DRUGS']).toEqual("Yes")
})

test('test the date and time of care and control is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "20210922 225900", "id": "prohibition_start_time"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['NOTICE_TIME']).toEqual("22:59")
    expect(actual['NOTICE_DAY']).toEqual("22nd")
    expect(actual['NOTICE_MONTH']).toEqual("September")
    expect(actual['NOTICE_YEAR']).toEqual("2021")
})

test('test licence surrender location is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "Saanich", "id": "offence_city"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['DL_SURRENDER_LOCATION']).toEqual("Saanich")
})

test('test officer badge number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "4444", "id": "badge_number"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['OFFICER_BADGE_NUMBER']).toEqual("4444")
})

test('test dl officer agency name is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "WVPD", "id": "agency"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['AGENCY_NAME']).toEqual("WVPD")
})

test('test agency file number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "2021-1234", "id": "file_number"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['AGENCY_FILE_NUMBER']).toEqual("2021-1234")
})

test('test owner last name is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "Andres", "id": "owners_last_name"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['OWNER_SURNAME']).toEqual("Andres")
})

test('test owner first name is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "Jim", "id": "owners_first_name"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['OWNER_GIVEN']).toEqual("Jim")
})

test('test owner address is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "1234 Main Street", "id": "owners_address1"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['OWNER_ADDRESS']).toEqual("1234 Main Street")
})

test('test owner city is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "Victoria", "id": "owners_city"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['OWNER_CITY']).toEqual("Victoria")
})

test('test owner province is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "BC", "id": "owners_province"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['OWNER_PROVINCE']).toEqual("BC")
})

test('test owner postal is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "V8R1B1", "id": "owners_postal"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['OWNER_POSTAL_CODE']).toEqual("V8R1B1")
})

test('test owner phone number is formatted and shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "2505551212", "id": "owners_phone"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['OWNER_PHONE_AREA_CODE']).toEqual("250")
    expect(actual['OWNER_PHONE_NUMBER']).toEqual("555-1212")
})

test('test that the selected impound lot operator is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {
        "value": "Buster's Towing Ltd, 435 Industrial Avenue, Vancouver, 604-685-7246", "id": "impound_lot_operator"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['IMPOUNDED_LOT']).toEqual("Buster's Towing Ltd")
    expect(actual['IMPOUNDED_ADDRESS']).toEqual("435 Industrial Avenue")
    expect(actual['IMPOUNDED_CITY']).toEqual("Vancouver")
    expect(actual['IMPOUNDED_PHONE_AREA_CODE']).toEqual("604")
    expect(actual['IMPOUNDED_PHONE_NUMBER']).toEqual("685-7246")
})

test('test when vehicle impounded the status is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "Yes", "id": "vehicle_impounded"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['IMPOUNDED']).toEqual("Yes")
    expect(actual['NOT_IMPOUNDED']).toEqual("")
})

test('test when vehicle NOT impounded the status is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "No", "id": "vehicle_impounded"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['IMPOUNDED']).toEqual("")
    expect(actual['NOT_IMPOUNDED']).toEqual("Yes")
})

test('test location of vehicle keys is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "With Vehicle", "id": "location_of_keys"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['RELEASE_LOCATION_KEYS']).toEqual("With Vehicle")
})

test('test location of vehicle keys is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "Dad Smith", "id": "vehicle_released_to"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['RELEASE_PERSON']).toEqual("Dad Smith")
})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "RHL123", "id": "plate_number"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['VEHICLE_LICENSE_NUMBER']).toEqual("RHL123")
})

test('test vehicle licence jurisdiction is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "BC", "id": "plate_province"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['VEHICLE_PROVINCE']).toEqual("BC")
})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "2021", "id": "plate_year"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['VEHICLE_LICENSE_YEAR']).toEqual("2021")
})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "6029101", "id": "plate_val_tag"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['VEHICLE_TAG_NUMBER']).toEqual("6029101")
})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "0292020292114", "id": "registration_number"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['VEHICLE_REGISTRATION_NUMBER']).toEqual("0292020292114")
})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "2DR", "id": "vehicle_type"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['VEHICLE_TYPE']).toEqual("2DR")
})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "HONDA", "id": "vehicle_make"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['VEHICLE_MAKE']).toEqual("HONDA")
})

test('test vehicle licence jurisdiction is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "ACCO", "id": "vehicle_model"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['VEHICLE_MODEL']).toEqual("ACCO")
})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "2021", "id": "vehicle_year"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['VEHICLE_YEAR']).toEqual("2021")
})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "BLU", "id": "vehicle_color"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['VEHICLE_COLOUR']).toEqual("BLU")
})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "BC", "id": "puj_code"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['VEHICLE_NSC_PUJ']).toEqual("BC")
})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "610029", "id": "nsc_number"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['VEHICLE_NSC_NUMBER']).toEqual("610029")
})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "2C3CCAGT1DH646504", "id": "vin_number"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['VEHICLE_VIN']).toEqual("2C3CCAGT1DH646504")
})

