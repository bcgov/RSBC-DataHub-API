import constants from "../config/constants";
import persistence from "../helpers/persistence";
import moment from "moment-timezone";
import fuzzysort from 'fuzzysort'


export const actions = {

    deleteSpecificForm(context, form_object ) {
        context.dispatch('deleteFormFromDB', form_object.form_id)
        context.commit('deleteForm', form_object)
        context.commit('stopEditingCurrentForm');
    },

    async renewFormLeasesFromApiIfNecessary (context) {
        console.log("inside renewFormLeasesFromApiIfNecessary()")
        for( let form in context.getters.arrayOfFormsRequiringRenewal) {
            let number_of_attempts = 0
            while (number_of_attempts < constants.MAX_NUMBER_UNIQUE_ID_FETCH_ATTEMPTS) {
                number_of_attempts++;
                await context.dispatch("renewFormFromApiById", form.form_type, form.form_id)
                    .then(data => {
                        if (data) {
                            context.commit("pushFormToStore", data)
                            context.dispatch("saveCurrentFormToDB", data)
                        }
                    })
                    .catch(function (error) {
                        console.log('Unable to renew form lease for ' + form.form_id)
                        console.log(error)
                    })
           }
        }
    },

    async getMoreFormsFromApiIfNecessary (context) {
        console.log("inside getMoreFormsFromApiIfNecessary()")
        context.getters.getArrayOfAllFormNames.forEach( form_type => {
            for (let i = 0; i < context.getters.getNumberOfUniqueIdsRequired(form_type); i++) {
                context.dispatch("getFormIdsFromApiByType", form_type)
                    .then(data => {
                        if (data) {
                            context.commit("pushFormToStore", data)
                            context.dispatch("saveCurrentFormToDB", data)
                        }
                    })
                    .catch(function (error) {
                        console.log('Unable to retrieve UniqueIDs for ' + form_type)
                        console.log(error)
                    })
           }
        })
    },

    async getFormIdsFromApiByType (context, form_type) {
        const url = constants.API_ROOT_URL + "/api/v1/forms/" + form_type
        return await fetch(url, {
            "method": "POST",
            "headers": context.getters.apiHeader,
            "credentials": "same-origin"})
            .then(response => response.json())
            .then(data => {
                return {
                    form_id: data.id,
                    form_type: data.form_type,
                    lease_expiry: data.lease_expiry,
                    printed_timestamp: data.printed_timestamp
                }
            })
            .catch(function (error) {
                console.log(error)
            });
    },

    async renewFormFromApiById (context, form_type, form_id) {
        console.log("inside renewFormFromApiById()")
        const url = constants.API_ROOT_URL + "/api/v1/forms/" + form_type + "/" + form_id
        return await fetch(url, {
            "method": "PATCH",
            "headers": context.getters.apiHeader,
            "credentials": "same-origin"})
            .then(response => response.json())
            .then(data => {
                return {
                    form_id: data.id,
                    form_type: data.form_type,
                    lease_expiry: data.lease_expiry,
                    printed_timestamp: data.printed_timestamp
                }
            })
            .catch(function (error) {
                console.log(error)
            });
    },

    async tellApiFormIsPrinted (context, payload) {
        console.log("inside tellApiFormIsPrinted()", payload)
        const url = constants.API_ROOT_URL + "/api/v1/forms/" +
            payload.form_type + "/" + payload.form_id
        return await new Promise((resolve, reject) => {
            fetch(url, {
                "method": "PATCH",
                "headers": context.getters.apiHeader,
                "credentials": "same-origin",
                body: JSON.stringify(context.state.forms[payload.form_type][payload.form_id])})
                .then(response => response.json())
                .then((data) => {
                    resolve(data)
                })
                .catch(function (error) {
                    console.log(error)
                    reject({error: error})
                });
            }
        )
    },

    // call to action that looks up the province code from the data that ICBC provides
    // if promise resolves successfully then mutate province field with jurisdiction object
    // if promise fails, do nothing
    async lookupDriverProvince(context, [pathString, provinceCode]) {
        console.log("inside actions.js lookupDriverProvince(): ", pathString, provinceCode)
        const jurisdictionArray = context.state.jurisdictions.filter(o => o.objectCd === provinceCode)
        return await new Promise((resolve, reject) => {
            if (jurisdictionArray.length > 0) {
                const event = {
                    "target": {
                        "value": jurisdictionArray[0],
                        "path": pathString,
                        "id": "province"
                    }
                }
                resolve(context.commit("updateFormField", event))
            } else {
                reject({"error": "Can't find " + provinceCode + " in list of jurisdictions"})
            }
        })
    },

    async lookupDriverFromICBC(context, [pathString, icbcPayload]) {
        console.log("inside actions.js lookupDriverFromICBC():", pathString, icbcPayload)
        let dlNumber = icbcPayload['dlNumber']
        const url = constants.API_ROOT_URL + "/api/v1/icbc/drivers/" + dlNumber
        return await new Promise((resolve, reject) => {
             fetch(url, {
                "method": 'GET',
                "headers": context.getters.apiHeader
            })
                .then(response => response.json())
                .then(data => {
                    console.log("ICBC driver data", data)
                    if ("error" in data) {
                        reject("message" in data['error'] ? {"description": data['error'].message }: {"description": "No valid response"})
                    } else {
                        const provinceCode = data['party']['addresses'][0]['region']
                        context.dispatch("lookupDriverProvince", [pathString, provinceCode])
                        resolve(context.commit("populateDriverFromICBC", data ))
                    }
                })
                .catch( (error) => {
                    if (error) {
                        reject("error" in error ? error.error : {"description": "No valid response"})
                    }
                    reject({"description": "Server did not respond"})
                });
            })
    },

    async lookupPlateFromICBC(context, [icbcPayload, path]) {
        console.log("inside actions.js lookupPlateFromICBC(): ")
        console.log("icbcPayload", icbcPayload)
        let plate_number = icbcPayload['plateNumber']
        const url = constants.API_ROOT_URL + "/api/v1/icbc/vehicles/" + plate_number
        return await new Promise((resolve, reject) => {
            fetch(url, {
            "method": 'GET',
            "headers": context.getters.apiHeader
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log("data", data)
                        if ("error" in data) {
                            reject("description" in data['error'] ? {"description": data['error'].description }: {"description": "No valid response"})
                        } else {
                            context.dispatch("findVehicleByFuzzySearch", data)
                                .then( (result) => {
                                    const payload = {"target": {
                                            "id": "vehicle_make",
                                            "path": path,
                                            "value": result
                                        }
                                    }
                                    console.log("preparing to updateFormField()", result, payload)
                                    context.commit("updateFormField", payload)
                                })
                                .catch( (error) => {
                                    console.log("findVehicleByFuzzySearch() - error", error)
                                })
                            resolve(context.commit("populateVehicleFromICBC", data))
                        }
                    })
                    .catch((error) => {
                        console.log("error", error)
                        if (error) {
                            reject("message" in error ? {"description": error.message }: {"description": "No valid response"})
                        }
                        reject({"description": "Server did not respond"})
                        });
                })
    },

    async fetchStaticLookupTables(context, payload) {
        let url = ''
        if (payload.admin) {
            url = constants.API_ROOT_URL + "/api/v1/admin/" + payload.resource
        } else if (payload.static) {
            url = constants.API_ROOT_URL + "/api/v1/static/" + payload.resource
        } else {
            url = constants.API_ROOT_URL + "/api/v1/" + payload.resource
        }
        console.log("fetchStaticLookupTables()", url)
        return await new Promise((resolve, reject) => {
            fetch(url, {
            "method": 'GET',
            "headers": context.getters.apiHeader})
            .then( response => {
                return response.json()
            })
            .then( data => {
                const admin_prefix = payload.admin ? 'admin_' : ''
                context.commit("populateStaticLookupTables", { "type": admin_prefix + payload.resource, "data": data })
                resolve(data)
            })
            .catch((error) => {
                console.log("fetchStaticLookupTables network fetch failed")
                reject(error)
            })
        })

    },

    async deleteFormFromDB(context, form_id) {
        await persistence.del(form_id);
    },

    async getAllFormsFromDB(context) {
        await persistence.all()
            .then( forms => {
                console.log("inside getAllFormsFromDB()", forms)
                forms.forEach( form => {
                    context.commit("pushFormToStore", form)
                });
            })
    },

    async saveCurrentFormToDB(context, form_object) {
        let form_object_to_save = context.state.forms[form_object.form_type][form_object.form_id]
        if (form_object_to_save) {
            await persistence.updateOrCreate(form_object.form_id, form_object_to_save)
        }
    },


    async applyToUnlockApplication(context, application) {
        console.log("inside actions.js applyToUnlockApplication(): ")
        const url = constants.API_ROOT_URL + "/api/v1/users"
        return await new Promise((resolve, reject) => {
            fetch(url, {
                "method": 'POST',
                "body": JSON.stringify(application),
                "headers": context.getters.apiHeader,
                    })
                        .then(response => {
                            return response
                        })
                        .then( (response) => {
                            const data = response.json()
                            if (response.status === 201) {
                                console.log("applyToUnlockApplication() - success", data)
                                resolve(data)
                            } else {
                                reject(data)
                            }
                        })
                        .catch((error) => {
                            console.log("error", error)
                            if (error) {
                                reject("message" in error ? {"description": error.message }: {"description": "No valid response"})
                            }
                            reject({"description": "Server did not respond"})
                            });
                    })
    },

    async adminApproveUserRole(context, new_user) {
        console.log("inside actions.js adminApproveUserRole(): ")
        const url = constants.API_ROOT_URL + "/api/v1/admin/users/" + new_user.user_guid + "/roles/officer"
        return await new Promise((resolve, reject) => {
            fetch(url, {
            "method": 'PATCH',
            "headers": context.getters.apiHeader,
                })
                    .then(response => {
                        if (response.status === 200) {
                            return response.json()
                        }
                    })
                    .then( data => {
                        new_user.role_name = data.role_name
                        new_user.approved_dt = data.approved_dt
                        new_user.submitted_dt = data.submitted_dt
                        resolve(context.commit("updateAdminUserRole", new_user))
                    })
                    .catch((error) => {
                        console.log("error", error)
                        if (error) {
                            reject("message" in error ? {"description": error.message }: {"description": "No valid response"})
                        }
                        reject({"description": "Server did not respond"})
                        });
                })
    },

    async adminDeleteUserRole(context, payload) {
        console.log("inside actions.js adminDeleteUserRole(): ", payload)
        const url = constants.API_ROOT_URL + "/api/v1/admin/users/" + payload.user_guid + "/roles/" + payload.role_name
        return await new Promise((resolve, reject) => {
            fetch(url, {
            "method": 'DELETE',
            "headers": context.getters.apiHeader,
                })
                    .then(response => {
                        console.log(response)
                        if (response.status === 200) {
                            resolve(context.commit("deleteAdminUserRole", payload))
                        }
                    })
                    .catch(error => {
                        console.log("error", error)
                        if (error) {
                            reject("message" in error ? {"description": error.message }: {"description": "No valid response"})
                        }
                        reject({"description": "Server did not respond"})
                        });
                })
    },

    async adminAddUserRole(context, new_user) {
        console.log("inside actions.js adminAddUserRole()", new_user)
        const url = constants.API_ROOT_URL + "/api/v1/admin/users/" + new_user.user_guid + "/roles"
        const payload = {"role_name": "administrator"}
        return await new Promise((resolve, reject) => {
            fetch(url, {
                "method": 'POST',
                "body": JSON.stringify(payload),
                "headers": context.getters.apiHeader,
                })
                    .then(response => {
                        if (response.status === 200) {
                            return response.json()
                        }
                    })
                    .then( () => {
                        return resolve(context.commit("addAdminUserRole", {
                            username: new_user.username,
                            user_guid: new_user.user_guid,
                            first_name: new_user.first_name,
                            last_name: new_user.last_name,
                            badge_number: new_user.badge_number,
                            agency: new_user.agency,
                            role_name: payload.role_name,
                            approved_dt: moment().tz("America/Vancouver"),
                            submitted_dt: moment().tz("America/Vancouver")
                        }))
                    })
                    .catch((error) => {
                        console.log("error", error)
                        if (error) {
                            return reject("message" in error ? {"description": error.message }: {"description": "No valid response"})
                        }
                        return reject({"description": "Server did not respond"})
                        });
                })
    },

    downloadLookupTables(context) {

        context.dispatch("fetchStaticLookupTables", {"resource": "agencies", "admin": false, "static": true})
            .then(() => {
                context.commit("resourceLoaded", "agencies")
            })
        context.dispatch("fetchStaticLookupTables", {"resource": "impound_lot_operators", "admin": false, "static": true})
            .then(() => {
                context.commit("resourceLoaded", "impound_lot_operators")
            })
        context.dispatch("fetchStaticLookupTables", {"resource": "countries", "admin": false, "static": true})
            .then(() => {
                context.commit("resourceLoaded", "countries")
            })
        context.dispatch("fetchStaticLookupTables", {"resource": "jurisdictions", "admin": false, "static": true})
            .then(() => {
                context.commit("resourceLoaded", "jurisdictions")
            })
        context.dispatch("fetchStaticLookupTables", {"resource": "provinces", "admin": false, "static": true})
            .then(() => {
                context.commit("resourceLoaded", "provinces")
            })
        context.dispatch("fetchStaticLookupTables", {"resource": "cities", "admin": false, "static": true})
            .then(() => {
                context.commit("resourceLoaded", "cities")
            })
        context.dispatch("fetchStaticLookupTables", {"resource": "vehicles", "admin": false, "static": true})
            .then(() => {
                context.commit("resourceLoaded", "vehicles")
            })
        context.dispatch("fetchStaticLookupTables", {"resource": "vehicle_styles", "admin": false, "static": true})
            .then(() => {
                context.commit("resourceLoaded", "vehicle_styles")
            })
        context.dispatch("fetchStaticLookupTables", {"resource": "configuration", "admin": false, "static": true})
            .then(() => {
                context.commit("resourceLoaded", "configuration")
            })

    },

    updateRichCheckBox (context, payload) {
        console.log("inside updateRichCheckBox()", payload)
        if(payload.event.checked) {
            context.commit('addItemToCheckboxList', payload)
        } else {
            context.commit('removeItemFromCheckboxList', payload)
        }
    },

    // When the vehicle queried from ICBC's API, the returned vehicle make and model
    // may not exactly match the vehicle list from PrimeCorp that contains the make
    // and model abbreviations used on the printouts. We use a fuzzy search
    // algorithm to find the best match.
    async findVehicleByFuzzySearch(context, payload) {
        console.log("findVehicleByFuzzySearch()", payload[0])
        const icbcData = payload[0]
        const primeCorpVehicleList = context.getters.getArrayOfVehicleSearchString
        const results = fuzzysort.go(icbcData['vehicleMake'] + " - " + icbcData['vehicleModel'], primeCorpVehicleList)
        return await new Promise((resolve, reject) => {
            console.log("findVehicleByFuzzySearch() - results", results, payload)
            if (results.length >= 1) {
                const vehicleObject = context.getters.getArrayOfVehicleMakeModel.filter(v => v.search === results[0].target)
                resolve(vehicleObject[0])
            } else {
                reject({
                    "description": "no match found",
                    "result": results
                })
            }
        })
    },

    // copy some driver fields to the registered owner fields
    // in the event the driver field is null or does not exist, do not copy
    populateOwnerFromDriver(context, form_path) {
        // trigger the following mutation
        context.commit("updateFormAttribute", [form_path, "corp_owner_false", {}])
        context.dispatch("copyIfExists", [form_path, "last_name", "corp_owner_false/owners_last_name"])
        context.dispatch("copyIfExists", [form_path, "first_name", "corp_owner_false/owners_first_name"])
        context.dispatch("copyIfExists", [form_path, "address1", "owners_address1"])
        context.dispatch("copyIfExists", [form_path, "city", "owners_city"])
        context.dispatch("copyIfExists", [form_path, "province", "owners_province"])
        context.dispatch("copyIfExists", [form_path, "postal", "owners_postal"])
        context.dispatch("copyIfExists", [form_path, "dob", "corp_owner_false/owner_dob"])
        context.commit("deleteFormAttribute", [form_path, "corp_owner_true" ])
    },

    copyIfExists(context, [form_path, source_attribute, destination_attribute]) {
        if (context.getters.doesAttributeExist(form_path, source_attribute)) {
            context.commit("updateFormAttribute", [
                form_path,
                destination_attribute,
                context.getters.getAttributeValue(form_path, source_attribute)])
        }
    },

    updateUserIsAuthenticated(context, payload) {
        if (Array.isArray(payload)) {
            for (const role of payload) {
                if ('approved_dt' in role) {
                    if (role.approved_dt) {
                        context.commit("userIsAuthenticated", true)
                    }
                }
            }
        } else {
            context.commit("userIsAuthenticated", false)
        }

    }
}
