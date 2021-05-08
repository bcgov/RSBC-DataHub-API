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
        console.log("inside mutations.js updateFormField(): " + JSON.stringify(payload))
        console.log("ID: " + payload.target.id)
        console.log("value: " + payload.target.value)
        const id = payload.target.id;
        const value = payload.target.value;
        const prohibition_number = state.currently_editing_prohibition_number;
        Vue.set(state.edited_forms[prohibition_number].data, id, value);
    },

    updateCheckBox (state, payload) {
        console.log("inside mutations.js updateCheckBox():", payload)
        console.log("ID: " + payload.target.id)
        console.log("value: " + payload.target.value)
        const id = payload.target.id;
        const value = payload.target.value;
        const prohibition_number = state.currently_editing_prohibition_number;
        const root = state.edited_forms[prohibition_number].data
        if (root[id]) {
            if ((root[id].includes(value)) ) {
                // item exists; remove it
                console.log(value, 'exists, remove it')
                const indexOfValue = root[id].indexOf(value)
                root[id].splice(indexOfValue, 1)
            } else {
                // item doesn't exist; so add it
                console.log(value, 'does not exist, add it')
                root[id].push(value);
            }
        } else {
            console.log('initial push', value)
            Vue.set(root, id, [value])
        }


    },

    saveDoNotPrint (state) {
        console.log("inside mutations.js stopEditingForm()")
        state.currently_editing_prohibition_number = null;
    },

    deleteEditedForm(state, prohibition_number) {
        console.log("inside mutations.js deleteEditedForm()", prohibition_number)
        const indexToDelete = state.edited_prohibition_numbers.indexOf(prohibition_number);
        Vue.delete(state.edited_prohibition_numbers, indexToDelete)
        Vue.delete(state.edited_forms, prohibition_number)
        state.currently_editing_prohibition_number = null;
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
        console.log("inside mutations.js populateDriversFromICBC(): " + prohibition_number)
        populateDriver(state,prohibition_number)
    },

    populateFromICBCPlateLookup(state) {
        // TODO - remove before flight
        // TODO - populates Driver's information using fictitious data
        const prohibition_number = state.currently_editing_prohibition_number;
        console.log("inside mutations.js populateFromICBCPlateLookup(): " + prohibition_number)
        populateDriver(state,prohibition_number);
        populateRegisteredOwner(state,prohibition_number);
        populateVehicleInfo(state,prohibition_number);
    }
}

function populateVehicleInfo(state, prohibition_number) {
    Vue.set(state.edited_forms[prohibition_number].data, "plate_year", "2021");
    Vue.set(state.edited_forms[prohibition_number].data, "plate_val_tag", "1234567");
    Vue.set(state.edited_forms[prohibition_number].data, "registration_number", "1234567");
    Vue.set(state.edited_forms[prohibition_number].data, "vehicle_year", "2014");
    Vue.set(state.edited_forms[prohibition_number].data, "vehicle_make", "Honda");
    Vue.set(state.edited_forms[prohibition_number].data, "vehicle_model", "Civic");
    Vue.set(state.edited_forms[prohibition_number].data, "vehicle_color", "Red");
}


function populateRegisteredOwner(state,prohibition_number) {
    Vue.set(state.edited_forms[prohibition_number].data, "owners_drivers_number", "1234567");
    Vue.set(state.edited_forms[prohibition_number].data, "owners_last_name", "Smith");
    Vue.set(state.edited_forms[prohibition_number].data, "owners_first_name", "Fictitious");
    Vue.set(state.edited_forms[prohibition_number].data, "owners_address1", "123 Imaginary Street");
    Vue.set(state.edited_forms[prohibition_number].data, "owners_city", "Vanderhoof");
    Vue.set(state.edited_forms[prohibition_number].data, "owners_province", "BC");
    Vue.set(state.edited_forms[prohibition_number].data, "owners_postal", "V8R 5A5");
    Vue.set(state.edited_forms[prohibition_number].data, "drivers_number", "1234567");
}


function populateDriver(state, prohibition_number) {
    Vue.set(state.edited_forms[prohibition_number].data, "last_name", "Smith");
    Vue.set(state.edited_forms[prohibition_number].data, "first_name", "Fictitious");
    Vue.set(state.edited_forms[prohibition_number].data, "address1", "123 Imaginary Street");
    Vue.set(state.edited_forms[prohibition_number].data, "city", "Vanderhoof");
    Vue.set(state.edited_forms[prohibition_number].data, "province", "BC");
    Vue.set(state.edited_forms[prohibition_number].data, "postal", "V8R 5A5");
    Vue.set(state.edited_forms[prohibition_number].data, "dob", "2002-01-15");
}