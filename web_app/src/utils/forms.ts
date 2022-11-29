import constants from "../config/constants";
import rsiStore from "@/store"
import persistence from "../helpers/persistence";
import moment from "moment";
import {apiHeader} from "@/utils/auth"

export async function deleteFormFromDB(form_id) {
    await persistence.del(form_id);
}

export async function getAllFormsFromDB() {
    await persistence.all()
        .then( forms => {
            console.log("inside getAllFormsFromDB()", forms)
            forms.forEach( form => {
                rsiStore.commit("pushFormToStore", form)
            });
        })
}

export async function saveCurrentFormToDB(form_object) {
    const form_object_to_save = rsiStore.state.forms[form_object.form_type][form_object.form_id]
    if (form_object_to_save) {
        await persistence.updateOrCreate(form_object.form_id, form_object_to_save)
    }
}


export function getCurrentlyEditedFormData(){
    const form_object = rsiStore.state.Common.currently_editing_form_object;
    const root = rsiStore.state.forms[form_object.form_type][form_object.form_id]
    return root.data;
}

export function getCurrentlyEditedForm(){
    const form_object = rsiStore.state.Common.currently_editing_form_object;
    return rsiStore.state.forms[form_object.form_type][form_object.form_id]
}



export async function tellApiFormIsPrinted (payload) {
    
    console.log("inside tellApiFormIsPrinted()", payload)
    const url = constants.API_ROOT_URL + "/api/v1/forms/" +
        payload.form_type + "/" + payload.form_id

    return await new Promise((resolve, reject) => {
        fetch(url, {
            "method": "PATCH",
            "headers": apiHeader(),
            "credentials": "same-origin",
            body: JSON.stringify(rsiStore.state.forms[payload.form_type][payload.form_id])})
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
}


export function deleteSpecificForm(form_object ) {
    deleteFormFromDB(form_object.form_id)
    rsiStore.commit('deleteForm', form_object)
    rsiStore.commit('Common/stopEditingCurrentForm');
}

export async function renewFormFromApiById (form_type, form_id) {
    console.log("inside renewFormFromApiById()")
    const url = constants.API_ROOT_URL + "/api/v1/forms/" + form_type + "/" + form_id
    return await fetch(url, {
        "method": "PATCH",
        "headers": apiHeader(),
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
}


function arrayOfFormsRequiringRenewal() {
    const forms = [];
    for (const form_type in rsiStore.state.forms) {
        for (const form_id in rsiStore.state.forms[form_type]) {
            const form_object = rsiStore.state.forms[form_type][form_id]
            const days_to_expiry = moment(form_object.lease_expiry).diff(moment(), 'days')
            if (! form_object.printed_timestamp && days_to_expiry < constants.UNIQUE_ID_REFRESH_DAYS) {
                forms.push(form_object)
            }
        }
    }
    return forms
}

export async function renewFormLeasesFromApiIfNecessary () {
    console.log("inside renewFormLeasesFromApiIfNecessary()")
    for( const form in arrayOfFormsRequiringRenewal()) {
        let number_of_attempts = 0
        while (number_of_attempts < constants.MAX_NUMBER_UNIQUE_ID_FETCH_ATTEMPTS) {
            number_of_attempts++;
            await renewFormFromApiById(form['form_type'], form['form_id'])
                .then(data => {
                    if (data) {
                        rsiStore.commit("pushFormToStore", data)
                        saveCurrentFormToDB(data)
                    }
                })
                .catch(function (error) {
                    console.log('Unable to renew form lease for ' + form['form_id'])
                    console.log(error)
                })
       }
    }
}


export async function getFormIdsFromApiByType (form_type) {
    const url = constants.API_ROOT_URL + "/api/v1/forms/" + form_type
    return await fetch(url, {
        "method": "POST",
        "headers": apiHeader(),
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
}



function getArrayOfAllFormNames(){
    const formNames = [];
    for (const form in rsiStore.state.form_schemas.forms) {
        formNames.push(form)
    }
    return formNames
}

export function getFormTypeCount(){
    const FormTypeCount = {}
    for (const form_type in rsiStore.state.forms) {
        FormTypeCount[form_type] = 0;
        for (const form_id in rsiStore.state.forms[form_type]) {
            if ( ! ("data" in rsiStore.state.forms[form_type][form_id])) {
                FormTypeCount[form_type]++
            }

        }
    }
    return FormTypeCount;
}

export function getArrayOfRecentViNumbers() {
    const localViNumbers = Object.keys(rsiStore.state.forms.VI);
    const optionsArray = [];
    for (const viNumber of localViNumbers) {
        const viInfo = rsiStore.state.forms.VI[viNumber]
        if (viInfo.data?.lastName && viInfo.data?.givenName) {
            optionsArray.push({
                viNumber: viNumber,
                label: viInfo.data.lastName +
                    ", " + viInfo.data.givenName+ " (" + viNumber + ")"
            })
        }

    }    
    return optionsArray
}


function getNumberOfUniqueIdsRequired(form_type){
    // Business rules state that X number of forms must be available to use offline
    const numberRequired = constants.MINIMUM_NUMBER_OF_UNIQUE_IDS_PER_TYPE - getFormTypeCount()[form_type];
    if (rsiStore.state.form_schemas.forms[form_type].disabled || numberRequired <= 0) {
        return 0
    } else {
        return numberRequired
    }
}

export async function getMoreFormsFromApiIfNecessary () {
    console.log("inside getMoreFormsFromApiIfNecessary()")
    for(const form_type of getArrayOfAllFormNames() ){ //Object.keys(rsiStore.state.form_schemas.forms)){
        for (let i = 0; i < getNumberOfUniqueIdsRequired(form_type); i++) {
            getFormIdsFromApiByType(form_type)
                .then(data => {
                    if (data) {
                        rsiStore.commit("pushFormToStore", data)
                        saveCurrentFormToDB(data)
                    }
                })
                .catch(function (error) {
                    console.log('Unable to retrieve UniqueIDs for ' + form_type)
                    console.log(error)
                })
       }
    }
}





