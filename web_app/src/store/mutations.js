import { ulid } from 'ulid'
import Vue from 'vue'

export default {

    setNewFormToEdit (state, form) {
        console.log('inside setNewFormToEdit')
        const prohibition_number = ulid().substr(0,12)
        const form_copy = JSON.parse(JSON.stringify(form))
        state.currently_editing_prohibition_number = prohibition_number
        form_copy.prohibition_number = prohibition_number;
        state.edited_prohibition_numbers.push(prohibition_number);
        Vue.set(state.edited_forms, prohibition_number, form_copy)
        console.log("check edited_forms: " + JSON.stringify(state.edited_forms))
    },

    editExistingForm (state, prohibition_number) {
       console.log("inside editExistingForm: " + prohibition_number)
       state.currently_editing_prohibition_number = prohibition_number;

    },

    updateFormField (state, payload) {
        console.log("inside updateFormField: " + JSON.stringify(payload))
        const id = payload.id;
        const value = payload.value;
        const prohibition_number = state.currently_editing_prohibition_number;
        Vue.set(state.edited_forms[prohibition_number].data[id], "value", value);
    },

    stopEditingForm (state) {
        console.log("inside stopEditingForm()")
        state.currently_editing_prohibition_number = null;
    },

    deleteEditedForm(state, prohibition_number) {
        const indexToDelete = state.edited_prohibition_numbers.indexOf(prohibition_number)
        Vue.delete(state.edited_prohibition_numbers, indexToDelete)
        Vue.delete(state.edited_forms, prohibition_number)
    },

    networkBackOnline(state) {
        state.isOnline = true;
    },

    networkOffline(state) {
        state.isOnline = false;
    },

    populateDriversFromICBC(state, prohibition_number) {
        // TODO - remove before flight
        // TODO - populates Driver's information using fictitious data
        console.log("inside populateDriversFromICBC: " + prohibition_number)
        Vue.set(state.edited_forms[prohibition_number].data["last_name"], "value", "Smith");
        Vue.set(state.edited_forms[prohibition_number].data["first_name"], "value", "Fictitious");
        Vue.set(state.edited_forms[prohibition_number].data["address1"], "value", "123 Imaginary Street");
        Vue.set(state.edited_forms[prohibition_number].data["address2"], "value", "");
        Vue.set(state.edited_forms[prohibition_number].data["city"], "value", "Vanderhoof");
        Vue.set(state.edited_forms[prohibition_number].data["province"], "value", "BC");
        Vue.set(state.edited_forms[prohibition_number].data["postal"], "value", "V8R 5A5");
        Vue.set(state.edited_forms[prohibition_number].data["dob"], "value", "2002-01-15");
    }
}