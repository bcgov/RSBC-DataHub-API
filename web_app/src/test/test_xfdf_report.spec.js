import { getters } from '../store/getters.js';
import { createLocalVue } from "@vue/test-utils";
import Vuex from 'vuex';
import { mutations } from "../store/mutations";

const state = {
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
const document_type = 'report'

test('test officers report populates witnessed by officer checkbox', () => {
    store.commit("updateCheckBox", { "target": { "value": "Witnessed by officer", "id": "operating_grounds"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['DRIVER_WITNESSED_BY_OFFICER']).toEqual("Yes")
})

test('test officers report populates admission by driver checkbox', () => {
    store.commit("updateCheckBox", { "target": { "value": "Admission by driver", "id": "operating_grounds"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['DRIVER_ADMISSION_BY_DRIVER']).toEqual("Yes")
})

test('test officers report populates independent witnessed checkbox', () => {
    store.commit("updateCheckBox", { "target": { "value": "Independent witness", "id": "operating_grounds"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['DRIVER_INDEPENDENT_WITNESS']).toEqual("Yes")
})

test('test officers report populates other evidence checkbox', () => {
    store.commit("updateCheckBox", { "target": { "value": "Other", "id": "operating_grounds"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['DRIVER_OTHER']).toEqual("Yes")
})

test('test officers report populates other memo if other is checked', () => {
    store.commit("updateFormField", { "target": { "value": "", "id": "operating_grounds"}})
    store.commit("updateCheckBox", { "target": { "value": "Other", "id": "operating_grounds"}})
    store.commit("updateFormField", { "target": { "value": "Some descriptive text", "id": "operating_ground_other"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['DRIVER_ADDITIONAL_INFORMATION_1']).toEqual("Some descriptive text")
})

test('test officers report does NOT populate other memo if other is NOT checked', () => {
    store.commit("updateFormField", { "target": { "value": "", "id": "operating_grounds"}})
    store.commit("updateCheckBox", { "target": { "value": "Independent Witness", "id": "operating_grounds"}})
    store.commit("updateFormField", { "target": { "value": "Some descriptive text", "id": "operating_ground_other"}})
    const actual = store.getters.getPrintMappings(state.currently_editing_form_object, document_type)
    expect(actual['DRIVER_ADDITIONAL_INFORMATION_1']).toEqual("")
})

