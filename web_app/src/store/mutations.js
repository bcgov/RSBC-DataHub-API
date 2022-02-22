import Vue from 'vue'

export const mutations = {

    editExistingForm (state, payload) {
        console.log("editExistingForm()", state.currently_editing_form_object, payload)
        Vue.set(state.currently_editing_form_object, "form_id", payload.form_id)
        Vue.set(state.currently_editing_form_object, "form_type", payload.form_type)

    },

    updateFormField (state, payload) {
        let id = payload.target.id;
        let value = payload.target.value;
        let form_object = state.currently_editing_form_object
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, id, value);
    },

    addItemToCheckboxList (state, payload) {
        console.log("inside addItemToCheckboxList()", state, payload)
        let root = state.forms[payload.form_object.form_type][payload.form_object.form_id].data
        let tenant = {id: payload.event.id, value: payload.event.value}
        if(payload.id in root) {
            root[payload.id].push(tenant);
        } else {
            root[payload.id] = [tenant];
        }
    },

    removeItemFromCheckboxList (state, payload) {
        console.log("inside removeItemFromCheckboxList()", state, payload)
        let root = state.forms[payload.form_object.form_type][payload.form_object.form_id].data
        let tenant = {id: payload.event.id, value: payload.event.value}
        let indexOfValue = root[payload.id].indexOf(tenant)
        root[payload.id].splice(indexOfValue, 1)
    },

    updateCheckBox (state, payload) {
        let id = payload.target.id;
        let value = payload.target.value;
        let form_object = state.currently_editing_form_object
        let root = state.forms[form_object.form_type][form_object.form_id].data
        if (root[id]) {
            if (root[id].includes(value) && typeof root[id] === "object") {
                // item exists; remove it
                let indexOfValue = root[id].indexOf(value)
                root[id].splice(indexOfValue, 1)
            } else {
                // item doesn't exist; so add it
                root[id].push(value);
            }
        } else {
            Vue.set(root, id, [value])
        }
    },

    deleteForm(state, payload) {
        // TODO - add business logic to ensure user is permitted to delete a form
        Vue.delete(state.forms[payload.form_type][payload.form_id], "data")
    },

    stopEditingCurrentForm(state) {
        state.currently_editing_form_object.form_type = null;
        state.currently_editing_form_object.form_id = null;
    },

    markFormStatusAsServed(state, date) {
        let form_object = state.currently_editing_form_object
        Vue.set(state.forms[form_object.form_type][form_object.form_id], "printed_timestamp", date)
    },

    setNewFormDefaults(state, form_object) {
        console.log("inside setNewFormDefaults()", form_object)
        let root = state.forms[form_object.form_type][form_object.form_id]
        if(! ("data" in root)) {
            Vue.set( root, "data", Object())
            Vue.set( root.data, "submitted", false);
            for (let form_property in state.form_schemas.forms[form_object.form_type]) {
                Vue.set(root, form_property, state.form_schemas.forms[form_object.form_type][form_property])
            }
        }
        if(state.keycloak.idTokenParsed) {
            Vue.set( root.data, "logged_in_user", state.keycloak.idTokenParsed.preferred_username);
            Vue.set( root.data, "officer_name", state.users.last_name);
            Vue.set( root.data, "agency", state.users.agency);
            Vue.set( root.data, "badge_number", state.users.badge_number);
        }
    },

    populateStaticLookupTables(state, payload) {
        Vue.set(state, payload.type, payload.data)
    },

    populateDriverFromICBC(state, data) {
        let form_object = state.currently_editing_form_object
        const address = data['party']['addresses'][0]
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "drivers_number", data['dlNumber']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "last_name", data['party']['lastName']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "first_name", data['party']['firstName']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "address1", address['addressLine1']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "city", address['city']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "province", address['region']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "postal", address['postalCode']);
        const dob_string = data['birthDate'].split("-").join('')
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "dob", dob_string);
    },

    saveICBCVehicleToStore(state, data) {
        Vue.set(state, 'icbc_vehicle_lookup', data)
    },

    populateVehicleFromICBC(state, payload) {
        let data = payload[0]
        let form_object = state.currently_editing_form_object
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "registration_number", data['registrationNumber']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "vehicle_year", data['vehicleModelYear']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "vehicle_make", data['vehicleMake']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "vehicle_model", data['vehicleModel']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "vehicle_type", data['vehicleStyle']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "vehicle_color", data['vehicleColour']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "vin_number", data['vehicleIdNumber']);

        const owner = data['vehicleParties'][0]['party']
        const address = owner['addresses'][0]

        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "owner_is_driver", []);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "owners_last_name", owner['lastName']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "owners_first_name", owner['firstName']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "owners_address1", address['addressLine1']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "owners_city", address['city']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "owners_province", address['region']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "owners_postal", address['postalCode']);
    },

    populateOwnerFromDriver(state) {
        let form_object = state.currently_editing_form_object
        let root = state.forms[form_object.form_type][form_object.form_id].data
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "owners_last_name", root.last_name);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "owners_first_name", root.first_name);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "owners_address1", root.address1);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "owners_city", root.city);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "owners_province", root.province);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "owners_postal", root.postal);
    },

    pushFormToStore(state, form_object) {
        console.log("inside pushFormToStore()", form_object)
        Vue.set(state.forms[form_object.form_type], form_object.form_id, form_object)
    },

    setKeycloak(state, keycloak_object) {
        Vue.set(state, "keycloak", keycloak_object)
    },

    setFormAsPrinted(state, payload) {
        let root = state.forms[payload.form_object.form_type][payload.form_object.form_id]
        Vue.set(root, "printed_timestamp", payload.timestamp)
    },

    updateUsers(state, p) {
        const index = state.users.findIndex( u => u.user_guid === p.user_guid && u.role_name === p.role_name)
        Vue.set(state.users, index, p)
    },

    deleteUser(state, p) {
        const index = state.users.findIndex( u => u.user_guid === p.user_guid && u.role_name === p.role_name)
        Vue.delete(state.users, index)
    },

    addUsers(state, payload) {
        state.users.push(payload)
    },

    pushInitialUserRole(state, payload) {
        Vue.set(state, "user_roles", [payload])
    },

    networkIsOnline(state) {
        Vue.set(state, "isOnline", true)
    },

    networkIsOffline(state) {
        Vue.set(state, "isOnline", false)
    },

    populateDriverFromBarCode(state, data) {
        console.log("inside populateDriverFromBarCode()", data)
        let form_object = state.currently_editing_form_object
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "drivers_number", data['number']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "address1", data['address']['street']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "city", data['address']['city']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "province", data['address']['province']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "postal", data['address']['postalCode']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "dob", data['dob']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "first_name", data['name']['given']);
        Vue.set(state.forms[form_object.form_type][form_object.form_id].data, "last_name", data['name']['surname']);
    },
}





