import nestedFunctions from "@/helpers/nestedFunctions";


export const getters = {

    getAttributeValue: state => (path, id) => {
        const pathArray = path.split("/")
        pathArray.push(id)
        return nestedFunctions.getProp(state, pathArray)
    },

    doesAttributeExist: state => (path, id) => {
        const pathArray = path.split("/")
        pathArray.push(id)
        const value = nestedFunctions.getProp(state, pathArray)
        return value !== undefined
    },

    hasFormBeenPrinted: state => {
        const form_object = state.Common.currently_editing_form_object;
        return Boolean(state.forms[form_object.form_type][form_object.form_id].printed_timestamp)
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

}

