import { ulid } from 'ulid'
import Vue from 'vue'

export default {

    setNewFormToEdit (state, form) {
        console.log('inside setNewFormToEdit')
        let new_index = state.edited_forms.push(JSON.parse(JSON.stringify(form))) - 1;
        let root = state.edited_forms[new_index]
        console.log("root", root)
        Vue.set( root, "data", Object())
        Vue.set( root.data, "served", false);
        Vue.set( root.data, "submitted", false);
        Vue.set( root.data, "prohibition_number", ulid().substr(0,12))
        state.currently_editing_prohibition_index = new_index;
        console.log("check edited_forms: " + JSON.stringify(state.edited_forms));
    },

    editExistingForm (state, prohibition_index) {
       console.log("inside editExistingForm: " + prohibition_index)
       state.currently_editing_prohibition_index = prohibition_index;

    },

    updateFormField (state, payload) {
        console.log("inside mutations.js updateFormField(): " + JSON.stringify(payload))
        console.log("ID: " + payload.target.id)
        console.log("value: " + payload.target.value)
        let id = payload.target.id;
        let value = payload.target.value;
        let prohibition_index = state.currently_editing_prohibition_index
        Vue.set(state.edited_forms[prohibition_index].data, id, value);
    },

    updateCheckBox (state, payload) {
        console.log("inside mutations.js updateCheckBox():", payload)
        console.log("ID: " + payload.target.id)
        console.log("value: " + payload.target.value)
        let id = payload.target.id;
        let value = payload.target.value;
        let prohibition_index = state.currently_editing_prohibition_index
        let root = state.edited_forms[prohibition_index].data
        if (root[id]) {
            if ((root[id].includes(value)) ) {
                // item exists; remove it
                console.log(value, 'exists, remove it')
                let indexOfValue = root[id].indexOf(value)
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

    saveFormsToLocalStorage (state) {
         console.log("inside mutations.js saveFormsToLocalStorage()");
         localStorage.setItem("digitalProhibitions", JSON.stringify(state.edited_forms) );
    },

    retrieveFormsFromLocalStorage (state) {
        let digitalProhibitions = localStorage.getItem("digitalProhibitions");
        if (digitalProhibitions) {
            let local_data = JSON.parse(digitalProhibitions);
            console.log("localStorage.digitalProhibitions does exists");
            local_data.forEach( form => {
                state.edited_forms.push(form);
            })
        } else {
            console.log("localStorage.digitalProhibitions does not exist")
        }
    },

    deleteForm(state, prohibition_index) {
        console.log("inside mutations.js deleteForm()")
        Vue.delete(state.edited_forms, prohibition_index)
    },

    stopEditingCurrentForm(state) {
        state.currently_editing_prohibition_index = null;
    },

    markFormStatusAsServed(state) {
        let prohibition_index = state.currently_editing_prohibition_index
        Vue.set(state.edited_forms[prohibition_index].data, "served", true)
    },

    networkBackOnline(state) {
        state.isOnline = true;
    },

    networkOffline(state) {
        state.isOnline = false;
    },

    populateDriversFromICBC(state, prohibition_index) {
        // TODO - remove before flight
        // TODO - populates Driver's information using fictitious data
        console.log("inside mutations.js populateDriversFromICBC(): " + prohibition_index)
        populateDriver(state,prohibition_index)
    },

    populateFromICBCPlateLookup(state) {
        // TODO - remove before flight
        // TODO - populates Driver's information using fictitious data
        let prohibition_index = state.currently_editing_prohibition_index;
        console.log("inside mutations.js populateFromICBCPlateLookup(): " + prohibition_index)
        populateDriver(state,prohibition_index);
        populateRegisteredOwner(state,prohibition_index);
        populateVehicleInfo(state,prohibition_index);
    }
}

function populateVehicleInfo(state, prohibition_index) {
    Vue.set(state.edited_forms[prohibition_index].data, "plate_year", "2021");
    Vue.set(state.edited_forms[prohibition_index].data, "plate_val_tag", "1234567");
    Vue.set(state.edited_forms[prohibition_index].data, "registration_number", "1234567");
    Vue.set(state.edited_forms[prohibition_index].data, "vehicle_year", "2014");
    Vue.set(state.edited_forms[prohibition_index].data, "vehicle_make", "Honda");
    Vue.set(state.edited_forms[prohibition_index].data, "vehicle_model", "Civic");
    Vue.set(state.edited_forms[prohibition_index].data, "vehicle_color", "Red");
}


function populateRegisteredOwner(state,prohibition_index) {
    Vue.set(state.edited_forms[prohibition_index].data, "owners_drivers_number", "1234567");
    Vue.set(state.edited_forms[prohibition_index].data, "owners_last_name", "Smith");
    Vue.set(state.edited_forms[prohibition_index].data, "owners_first_name", "Fictitious");
    Vue.set(state.edited_forms[prohibition_index].data, "owners_address1", "123 Imaginary Street");
    Vue.set(state.edited_forms[prohibition_index].data, "owners_city", "Vanderhoof");
    Vue.set(state.edited_forms[prohibition_index].data, "owners_province", "BC");
    Vue.set(state.edited_forms[prohibition_index].data, "owners_postal", "V8R 5A5");
    Vue.set(state.edited_forms[prohibition_index].data, "drivers_number", "1234567");
}


function populateDriver(state, prohibition_index) {
    Vue.set(state.edited_forms[prohibition_index].data, "last_name", "Smith");
    Vue.set(state.edited_forms[prohibition_index].data, "first_name", "Fictitious");
    Vue.set(state.edited_forms[prohibition_index].data, "address1", "123 Imaginary Street");
    Vue.set(state.edited_forms[prohibition_index].data, "city", "Vanderhoof");
    Vue.set(state.edited_forms[prohibition_index].data, "province", "BC");
    Vue.set(state.edited_forms[prohibition_index].data, "postal", "V8R 5A5");
    Vue.set(state.edited_forms[prohibition_index].data, "dob", "2002-01-15");
}