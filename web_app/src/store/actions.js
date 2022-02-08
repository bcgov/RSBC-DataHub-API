import constants from "@/config/constants";
import persistence from "@/helpers/persistence";
import print_layout from "@/config/print_layout.json";
import moment from "moment";
import pdfMerge from "@/helpers/pdfMerge";


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
            let number_of_attempts = 0
            while (context.getters.areNewUniqueIdsRequiredByType(form_type)
            && number_of_attempts < constants.MAX_NUMBER_UNIQUE_ID_FETCH_ATTEMPTS) {
                number_of_attempts++;
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

    async lookupDriverFromICBC(context, icbcPayload) {
        console.log("inside actions.js lookupDriverFromICBC(): " + icbcPayload)
        let dlNumber = icbcPayload['dlNumber']
        const url = constants.API_ROOT_URL + "/api/v1/icbc/drivers/" + dlNumber
        return await new Promise((resolve, reject) => {
             fetch(url, {
                "method": 'GET',
                "headers": context.getters.apiHeader
            })
                .then(response => response.json())
                .then(data => {
                    console.log("data", data)
                    if ("error" in data) {
                        reject("message" in data['error'] ? {"description": data['error'].message }: {"description": "No valid response"})
                    } else {
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

    async lookupPlateFromICBC(context, icbcPayload) {
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

    async fetchStaticLookupTables(context, type) {
        const admin = type === 'users' ? 'admin/' : ''
        const url = constants.API_ROOT_URL + "/api/v1/" + admin + type
        console.log("fetchStaticLookupTables()", url)
        fetch(url, {
            "method": 'GET',
            "headers": context.getters.apiHeader})
            .then( response => {
                return response.json()
            })
            .then( data => {
                context.commit("populateStaticLookupTables", { "type": type, "data": data })
            })
            .catch(() => {
                console.log("fetchStaticLookupTables network fetch failed")
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
        await persistence.updateOrCreate(form_object.form_id, form_object_to_save)
    },

    async createPDF (context, payload) {
        return new Promise((resolve) => {
            console.log("inside createPDF()", payload)
            context.dispatch("getPrintMappings", payload.form_object)
            .then((key_value_pairs) => {
                resolve(pdfMerge.generatePDF(
                    print_layout[payload.form_object.form_type],
                    payload.variants,
                    key_value_pairs,
                    payload.filename
                ))
            })
        })
    },


    // the print templates use different field names from the form
    // TODO - refactor this method.  Suggest calling appropriate getters from print_layout.json
    async getPrintMappings(context, form_object) {
        return new Promise(resolve => {
            let key_value_pairs = Array();

            key_value_pairs['VIOLATION_NUMBER'] = form_object.form_id

            key_value_pairs['REASON_ALCOHOL_215'] = context.getters.getFormPrintRadioValue(form_object, 'prohibition_type', 'Alcohol 215(2)')
            key_value_pairs['REASON_DRUGS_215'] = context.getters.getFormPrintRadioValue(form_object, 'prohibition_type', 'Drugs 215(3)')

            key_value_pairs['REASON_ALCOHOL_90'] = context.getters.getFormPrintRadioValue(form_object, 'prohibition_type_12hr', 'Alcohol 90.3(2)')
            key_value_pairs['REASON_DRUGS_90'] = context.getters.getFormPrintRadioValue(form_object, 'prohibition_type_12hr', 'Drugs 90.3(2.1)')

            let prohibition_start_time = moment(context.getters.getFormPrintValue(form_object, 'prohibition_start_time'))
            key_value_pairs['NOTICE_TIME'] = prohibition_start_time.format("HH:mm")
            key_value_pairs['NOTICE_DAY'] = prohibition_start_time.format("Do")
            key_value_pairs['NOTICE_MONTH'] = prohibition_start_time.format("MMMM")
            key_value_pairs['NOTICE_YEAR'] = prohibition_start_time.format("YYYY")

            key_value_pairs['DL_SURRENDER_LOCATION'] = context.getters.getFormPrintValue(form_object, 'offence_address') +
                ", " + context.getters.getFormPrintValue(form_object, 'offence_city')
            key_value_pairs['OFFICER_BADGE_NUMBER'] = context.getters.getFormPrintValue(form_object, 'badge_number')
            key_value_pairs['AGENCY_NAME'] = context.getters.getFormPrintValue(form_object, 'agency')
            key_value_pairs['AGENCY_FILE_NUMBER'] = context.getters.getFormPrintValue(form_object, 'file_number')
            key_value_pairs['OFFICER_LAST_NAME'] = context.getters.getFormPrintValue(form_object, 'officer_name')

            key_value_pairs['OWNER_NAME'] = context.getters.getFormPrintValue(form_object, 'owners_last_name')
                + ", " + context.getters.getFormPrintValue(form_object, 'owners_first_name')

            key_value_pairs['OWNER_ADDRESS'] = context.getters.getFormPrintValue(form_object, 'owners_address1')
                    + ", " + context.getters.getFormPrintValue(form_object, 'owners_city')
            key_value_pairs['OWNER_PROVINCE'] = context.getters.getFormPrintValue(form_object, 'owners_province')
            key_value_pairs['OWNER_POSTAL_CODE'] = context.getters.getFormPrintValue(form_object, 'owners_postal')
            key_value_pairs['OWNER_PHONE_AREA_CODE'] = context.getters.getFormPrintValue(form_object, 'owners_phone').substr(0, 3)

            let phone_number = context.getters.getFormPrintValue(form_object, 'owners_phone')
            key_value_pairs['OWNER_PHONE_NUMBER'] = phone_number.substr(3, 3) + '-' + phone_number.substr(6, 9)

            key_value_pairs['VEHICLE_LICENSE_NUMBER'] = context.getters.getFormPrintValue(form_object, 'plate_number')
            key_value_pairs['VEHICLE_PROVINCE'] = context.getters.getFormPrintJurisdiction(form_object, 'plate_province')
            key_value_pairs['VEHICLE_LICENSE_YEAR'] = context.getters.getFormPrintValue(form_object, 'plate_year')
            key_value_pairs['VEHICLE_TAG_NUMBER'] = context.getters.getFormPrintValue(form_object, 'plate_val_tag')
            key_value_pairs['VEHICLE_REGISTRATION_NUMBER'] = context.getters.getFormPrintValue(form_object, 'registration_number')
            key_value_pairs['VEHICLE_TYPE'] = context.getters.getFormPrintValue(form_object, 'vehicle_type')
            key_value_pairs['VEHICLE_MAKE'] = context.getters.getFormPrintValue(form_object, 'vehicle_make')
            key_value_pairs['VEHICLE_MODEL'] = context.getters.getFormPrintValue(form_object, 'vehicle_model')
            key_value_pairs['VEHICLE_YEAR'] = context.getters.getFormPrintValue(form_object, 'vehicle_year')
            key_value_pairs['VEHICLE_COLOR'] = context.getters.getFormPrintValue(form_object, 'vehicle_color')
            key_value_pairs['VEHICLE_NSC_PUJ'] = context.getters.getFormPrintValue(form_object, 'puj_code')
            key_value_pairs['VEHICLE_NSC_NUMBER'] = context.getters.getFormPrintValue(form_object, 'nsc_number')
            key_value_pairs['VEHICLE_VIN'] = context.getters.getFormPrintValue(form_object, 'vin_number')

            key_value_pairs['NOT_IMPOUNDED'] = context.getters.getFormPrintRadioValue(form_object, 'vehicle_impounded', 'No')
            key_value_pairs['IMPOUNDED'] = context.getters.getFormPrintRadioValue(form_object, 'vehicle_impounded', 'Yes')

            // TODO - don't print the following if the vehicle is impounded
            key_value_pairs['NOT_IMPOUNDED_REASON'] = context.getters.getFormPrintValue(form_object, 'reason_for_not_impounding')

            let ilo = context.getters.getFormPrintValue(form_object, 'impound_lot_operator').split(", ")
            if (ilo.length > 1) {
                key_value_pairs['IMPOUNDED_LOT'] = ilo[0]
                key_value_pairs['IMPOUNDED_ADDRESS'] = ilo[1] + ", " + ilo[2]
                key_value_pairs['IMPOUNDED_PHONE_AREA_CODE'] = ilo[3].substr(0, 3)
                key_value_pairs['IMPOUNDED_PHONE_NUMBER'] = ilo[3].substr(4)
            }

            key_value_pairs['RELEASE_LOCATION_VEHICLE'] = context.getters.locationOfVehicle(form_object)

            key_value_pairs['RELEASE_LOCATION_KEYS'] = context.getters.getFormPrintValue(form_object, 'location_of_keys')
            key_value_pairs['RELEASE_PERSON'] = context.getters.getFormPrintValue(form_object, 'vehicle_released_to')

            key_value_pairs['DRIVER_SURNAME'] = context.getters.getFormPrintValue(form_object,"last_name")
            key_value_pairs['DRIVER_GIVEN'] = context.getters.getFormPrintValue(form_object,'first_name')
            key_value_pairs['DRIVER_DL_NUMBER'] = context.getters.getFormPrintValue(form_object,'drivers_number')
            key_value_pairs['DRIVER_DL_PROVINCE'] = context.getters.getFormPrintJurisdiction(form_object,'drivers_licence_jurisdiction')

            let dob = moment(context.getters.getFormPrintValue(form_object,'dob'))
            key_value_pairs['DRIVER_DOB'] = dob.format("YYYY MM DD")

            key_value_pairs['DRIVER_ADDRESS'] =
                context.getters.getFormPrintValue(form_object,'address1') + ", " +
                context.getters.getFormPrintValue(form_object,'city') + ", " +
                context.getters.getFormPrintValue(form_object,'province') + ", " +
                context.getters.getFormPrintValue(form_object,'postal')

            key_value_pairs['DRIVER_WITNESSED_BY_OFFICER'] = context.getters.getFormPrintCheckedValue(
                form_object, 'operating_grounds', "Witnessed by officer")
            key_value_pairs['DRIVER_INDEPENDENT_WITNESS'] = context.getters.getFormPrintCheckedValue(
                form_object, 'operating_grounds', "Independent witness")
            key_value_pairs['DRIVER_ADMISSION_BY_DRIVER'] = context.getters.getFormPrintCheckedValue(
                form_object, 'operating_grounds', "Admission by driver")
            key_value_pairs['VIDEO_SURVEILLANCE'] = context.getters.getFormPrintCheckedValue(
                form_object, 'operating_grounds', "Video surveillance")

            let operating_grounds_other = context.getters.getFormPrintCheckedValue(
                form_object, 'operating_grounds', "Other")
            key_value_pairs['DRIVER_OTHER'] = operating_grounds_other

            if (operating_grounds_other) {
                key_value_pairs['DRIVER_ADDITIONAL_INFORMATION'] = context.getters.getFormPrintValue(
                    form_object, 'operating_ground_other')
            } else {
                key_value_pairs['DRIVER_ADDITIONAL_INFORMATION'] = ''
            }

            key_value_pairs['REASONABLE_GROUNDS_YES'] = context.getters.getFormPrintCheckedValue(
                form_object, 'prescribed_device', "Yes")
            key_value_pairs['REASONABLE_GROUNDS_NO'] = context.getters.getFormPrintCheckedValue(
                form_object, 'prescribed_device', "No")

            key_value_pairs['REASON_PRESCRIBED_TEST_NOT_USED'] = context.getters.getFormPrintValue(
                    form_object, 'reason_prescribed_test_not_used')


            // Alcohol - 215
            if (key_value_pairs['REASON_ALCOHOL_215']) {

                key_value_pairs['REASONABLE_GROUNDS_TEST_ALCO_SENSOR'] = context.getters.getFormPrintCheckedValue(
                    form_object, 'test_administered_asd', 'Alco-Sensor FST (ASD)')

                key_value_pairs['REASONABLE_GROUNDS_TEST_ASD_EXPIRY_DATE'] = context.getters.getFormPrintValue(
                    form_object, 'asd_expiry_date')

                key_value_pairs['REASONABLE_GROUNDS_TEST_TIME'] = context.getters.getFormPrintDateTime(
                    form_object, 'time_of_test')

                key_value_pairs['REASONABLE_GROUNDS_ALCOHOL_51-99'] = context.getters.getFormPrintCheckedValue(
                    form_object, 'result_alcohol', '51-99 mg%')

                key_value_pairs['REASONABLE_GROUNDS_ALCOHOL_OVER_99'] = context.getters.getFormPrintCheckedValue(
                    form_object, 'result_alcohol', 'Over 99 mg%')


                key_value_pairs['REASONABLE_GROUNDS_TEST_APPROVED_INSTRUMENT'] = context.getters.getFormPrintCheckedValue(
                    form_object, 'test_administered_instrument', 'Approved Instrument')

                key_value_pairs['REASONABLE_GROUNDS_ALCOHOL_BAC'] = context.getters.getFormPrintCheckedValue(
                        form_object, 'result_alcohol_approved_instrument', "BAC")

                if (key_value_pairs['REASONABLE_GROUNDS_ALCOHOL_BAC']) {

                    key_value_pairs['REASONABLE_GROUNDS_ALCOHOL_BAC_VALUE'] = context.getters.getFormPrintValue(
                        form_object, 'test_result_bac')
                }
            }

            // Drugs - 215
            if (key_value_pairs['REASON_DRUGS_215']) {

                let prescribed_test = []

                key_value_pairs['REASONABLE_GROUNDS_TEST_TIME'] = context.getters.getFormPrintDateTime(
                    form_object, 'time_of_test')

                if (context.getters.getFormPrintCheckedValue(
                        form_object, 'test_administered_adse', "Approved Drug Screening Equipment")) {
                    key_value_pairs['REASONABLE_GROUNDS_TEST_APPROVED_INSTRUMENT'] = true
                    key_value_pairs['REASONABLE_GROUNDS_TEST_APPROVED_INSTRUMENT_SPECIFY'] = 'ADSE'
                    key_value_pairs['ADSE_RESULTS'] = context.getters.getFormPrintValue(form_object,"positive_adse").join(" and ")
                }

                if (context.getters.getFormPrintCheckedValue(form_object, "test_administered_sfst", "Prescribed Physical Coordination Test (SFST)")) {
                    prescribed_test.push("SFST")
                    key_value_pairs['REASONABLE_GROUNDS_TEST_PHYSICAL_COORDINATION'] = true
                }

                if (context.getters.getFormPrintCheckedValue(form_object, "test_administered_dre", "Prescribed Physical Coordination Test (DRE)")) {
                    prescribed_test.push("DRE")
                    key_value_pairs['REASONABLE_GROUNDS_TEST_PHYSICAL_COORDINATION'] = true
                }

                key_value_pairs['PHYSICAL_TEST_SPECIFICS'] = prescribed_test.join(" and ")

                key_value_pairs['REASONABLE_GROUNDS_DRUG_ABILITY_TO_DRIVE_AFFECTED'] = context.getters.getFormPrintCheckedValue(
                    form_object, "result_drug", "Ability to drive affected by a drug")


            }
            resolve(key_value_pairs);

        })

    },

    async applyToUnlockApplication(context) {
        console.log("inside actions.js applyToUnlockApplication(): ")
        const url = constants.API_ROOT_URL + "/api/v1/user_roles"
        return await new Promise((resolve, reject) => {
            fetch(url, {
            "method": 'POST',
            "headers": context.getters.apiHeader,
                })
                    .then(response => {
                        return response.json()
                    })
                    .then( (data) => {
                        console.log("applyToUnlockApplication()", data)
                        resolve(context.commit("pushInitialUserRole", data))
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

    async adminApproveUserRole(context, username) {
        console.log("inside actions.js adminApproveUserRole(): ")
        const url = constants.API_ROOT_URL + "/api/v1/admin/users/" + username + "/roles/officer"
        return await new Promise((resolve, reject) => {
            fetch(url, {
            "method": 'PATCH',
            "headers": context.getters.apiHeader,
                })
                    .then(response => {
                        return response.json()
                    })
                    .then( data => {
                        resolve(context.commit("updateUsers", data))
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
        const url = constants.API_ROOT_URL + "/api/v1/admin/users/" + payload.username + "/roles/" + payload.role_name
        return await new Promise((resolve, reject) => {
            fetch(url, {
            "method": 'DELETE',
            "headers": context.getters.apiHeader,
                })
                    .then(response => {
                        console.log(response)
                        if (response.status === 200) {
                            resolve(context.commit("deleteUser", payload))
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

    async adminAddUserRole(context, username) {
        console.log("inside actions.js adminAddUserRole(): ")
        const url = constants.API_ROOT_URL + "/api/v1/admin/users/" + username + "/roles"
        const payload = {"role_name": "administrator"}
        return await new Promise((resolve, reject) => {
            fetch(url, {
                "method": 'POST',
                "body": JSON.stringify(payload),
                "headers": context.getters.apiHeader,
                })
                    .then(response => {
                        return response.json()
                    })
                    .then( data => {
                        return resolve(context.commit("addUsers", data))
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

    async saveFormAndGeneratePDF(context, form_object) {
        const current_timestamp = moment.now()
        console.log("inside saveAndPrint()", current_timestamp)
        let payload = {}
        payload['form_object'] = form_object
        payload['filename'] = context.getters.getPdfFileNameString(form_object, "all");
        payload['variants'] = context.getters.getPagesToPrint(form_object);
        await context.dispatch("saveCurrentFormToDB", form_object)
        await context.dispatch("createPDF", payload)
        payload['timestamp'] = current_timestamp
        await context.dispatch("tellApiFormIsPrinted", form_object)
          .then( (response) => {
              console.log("response from tellApiFormIsPrinted()", response)
              context.commit("setFormAsPrinted", payload)
              context.dispatch("saveCurrentFormToDB", form_object)
              context.commit("stopEditingCurrentForm")
          })
    },

    async downloadLookupTables(context) {

        await context.dispatch("fetchStaticLookupTables", "agencies")
        await context.dispatch("fetchStaticLookupTables", "impound_lot_operators")
        await context.dispatch("fetchStaticLookupTables", "countries")
        await context.dispatch("fetchStaticLookupTables", "jurisdictions")
        await context.dispatch("fetchStaticLookupTables", "provinces")
        await context.dispatch("fetchStaticLookupTables", "cities")
        await context.dispatch("fetchStaticLookupTables", "colors")
        await context.dispatch("fetchStaticLookupTables", "vehicles")
        await context.dispatch("fetchStaticLookupTables", "vehicle_styles")

    },

    updateRichCheckBox (context, payload) {
        console.log("inside updateRichCheckBox()", payload)
        if(payload.event.checked) {
            context.commit('addItemToCheckboxList', payload)
        } else {
            context.commit('removeItemFromCheckboxList', payload)
        }
    },
}
