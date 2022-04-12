import { getters } from '../store/getters.js';
import { actions } from '../store/actions.js';
import { createLocalVue } from "@vue/test-utils";
import Vuex from 'vuex';
import { mutations } from "../store/mutations";

let state = {
    "currently_editing_form_object": {
        "form_id": "AA111111",
        "form_type": "24Hour",
    },
    "forms": {
        "24Hour": {
            "AA111111": {
                "form_id": "AA111111",
                "form_type": "24Hour",
                "printed_timestamp": "2021-08-15",
                "lease_expiry": "2021-09-02",
                "data": {}
            }
        }
    },
    jurisdictions: [
      {
        "objectCd": "BC",
        "objectDsc": "British Columbia",
        "activeYN": "Y",
        "internalYN": null
      },
      {
        "objectCd": "CA",
        "objectDsc": "California",
        "activeYN": "Y",
        "internalYN": null
      },
    ]
};

createLocalVue().use(Vuex)
const store = new Vuex.Store({state, mutations, getters, actions})

jest.mock('../helpers/persistence', () => {
    // bare bones mock to prevent: "ReferenceError: indexedDB is not defined"
})


test('test prohibition number, without the prefix, is shown on driver copy', () => {
store.dispatch("getPrintMappings", state.currently_editing_form_object)
    .then((data) => {
        expect(data['VIOLATION_NUMBER']).toEqual("AA111111")
    })

})


test('test driver surname is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "Smith", "id": "last_name"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (data) => {
            expect(data['DRIVER_SURNAME']).toEqual("SMITH")
        })

})

test('test driver first name is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "Brian", "id": "first_name"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (data) => {
            expect(data['DRIVER_GIVEN']).toEqual("BRIAN")
        })

})

test('test driver licence number is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "5123456", "id": "drivers_number"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (data) => {
            expect(data['DRIVER_DL_NUMBER']).toEqual("5123456")
        })
})

test('test driver date of birth is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "19991231", "id": "dob"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['DRIVER_DOB']).toEqual("1999 12 31")
        })
})

test('test driver province / state is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "British Columbia", "id": "drivers_licence_jurisdiction"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
             expect(actual['DRIVER_DL_PROVINCE']).toEqual("BC")
        })
})


test('test driver city is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "123 Byng St", "id": "address1"}})
    store.commit("updateFormField", { "target": { "value": "Oak Bay", "id": "city"}})
    store.commit("updateFormField", { "target": { "value": "BC", "id": "province"}})
    store.commit("updateFormField", { "target": { "value": "V7R 4R5", "id": "postal"}})

    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
             expect(actual['DRIVER_ADDRESS']).toEqual("123 BYNG ST, OAK BAY, BC, V7R 4R5")
        })
})


test('test prohibition reason alcohol is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "Alcohol 215(2)", "id": "prohibition_type"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['REASON_ALCOHOL_215']).toEqual(true)
            expect(actual['REASON_DRUGS_215']).toEqual(false)
        })
        .catch( (error) => {
            console.debug(error)
        })

})

test('test prohibition reason drugs is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "Drugs 215(3)", "id": "prohibition_type"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['REASON_ALCOHOL_215']).toEqual(false)
            expect(actual['REASON_DRUGS_215']).toEqual(true)
        })

})

test('test the date and time of care and control is shown on drivers copy', () => {
    store.commit("updateFormField", { "target": { "value": "20210922", "id": "prohibition_start_date"}})
    store.commit("updateFormField", { "target": { "value": "2259", "id": "prohibition_start_time"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['NOTICE_TIME']).toEqual("22:59")
            expect(actual['NOTICE_DAY']).toEqual("22nd")
            expect(actual['NOTICE_MONTH']).toEqual("September")
            expect(actual['NOTICE_YEAR']).toEqual("2021")
        })
})

test('test licence surrender location is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "123 Main Street", "id": "offence_address"}})
    store.commit("updateFormField", {"target": {"value": "Saanich", "id": "offence_city"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['DL_SURRENDER_LOCATION']).toEqual("123 MAIN STREET, SAANICH")
        })

})

test('test officer badge number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "4444", "id": "badge_number"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['OFFICER_BADGE_NUMBER']).toEqual("4444")
        })

})

test('test dl officer agency name is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "WVPD", "id": "agency"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['AGENCY_NAME']).toEqual("WVPD")
        })

})

test('test agency file number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "2021-1234", "id": "file_number"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['AGENCY_FILE_NUMBER']).toEqual("2021-1234")
        })

})

test('test owner name is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "Jim", "id": "owners_first_name"}})
    store.commit("updateFormField", {"target": {"value": "Andres", "id": "owners_last_name"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['OWNER_NAME']).toEqual("ANDRES, JIM")
        })

})

test('test owner address is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "1234 Main Street", "id": "owners_address1"}})
    store.commit("updateFormField", {"target": {"value": "Victoria", "id": "owners_city"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['OWNER_ADDRESS']).toEqual("1234 MAIN STREET, VICTORIA")
        })
})


test('test owner province is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "BC", "id": "owners_province"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['OWNER_PROVINCE']).toEqual("BC")
        })

})

test('test owner postal is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "V8R1B1", "id": "owners_postal"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['OWNER_POSTAL_CODE']).toEqual("V8R1B1")
        })

})

test('test owner phone number is formatted and shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "2505551212", "id": "owners_phone"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['OWNER_PHONE_AREA_CODE']).toEqual("250")
            expect(actual['OWNER_PHONE_NUMBER']).toEqual("555-1212")
        })

})

test('test that the selected impound lot operator is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "Yes", "id": "vehicle_impounded"}})
    store.commit("updateFormField", {"target": {"value": "With vehicle", "id": "location_of_keys"}})
    store.commit("updateFormField", {"target": {
        "value": "Buster's Towing Ltd, 435 Industrial Avenue, Vancouver, 604-685-7246", "id": "impound_lot_operator"}})
    // console.debug("ILO: " + store.getters.getAttributeValue("impound_lot_operator"))
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['NOT_IMPOUNDED']).toEqual(false)
            expect(actual['IMPOUNDED']).toEqual(true)
            expect(actual['RELEASE_LOCATION_KEYS']).toEqual("WITH VEHICLE")
            expect(actual['IMPOUNDED_LOT']).toEqual("BUSTER'S TOWING LTD")
            expect(actual['IMPOUNDED_ADDRESS']).toEqual("435 INDUSTRIAL AVENUE, VANCOUVER")
            expect(actual['IMPOUNDED_PHONE_AREA_CODE']).toEqual("604")
            expect(actual['IMPOUNDED_PHONE_NUMBER']).toEqual("685-7246")
        })

})

test('test when vehicle impounded the status is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "Yes", "id": "vehicle_impounded"}})
    store.commit("updateFormField", {"target": {"value": "With Vehicle", "id": "location_of_keys"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['IMPOUNDED']).toEqual(true)
            expect(actual['NOT_IMPOUNDED']).toEqual(false)
            expect(actual['RELEASE_LOCATION_KEYS']).toEqual("WITH VEHICLE")
        })

})

test('test when vehicle NOT impounded the status is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "No", "id": "vehicle_impounded"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['IMPOUNDED']).toEqual(false)
            expect(actual['NOT_IMPOUNDED']).toEqual(true)
            expect(actual['RELEASE_LOCATION_KEYS']).toEqual(undefined)
        })

})

test('test location of vehicle keys is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "Dad Smith", "id": "vehicle_released_to"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['RELEASE_PERSON']).toEqual("DAD SMITH")
        })

})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "RHL123", "id": "plate_number"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['VEHICLE_LICENSE_NUMBER']).toEqual("RHL123")
        })

})

test('test vehicle licence jurisdiction is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "British Columbia", "id": "plate_province"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['VEHICLE_PROVINCE']).toEqual("BC")
        })

})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "2021", "id": "plate_year"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['VEHICLE_LICENSE_YEAR']).toEqual("2021")
        })

})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "6029101", "id": "plate_val_tag"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['VEHICLE_TAG_NUMBER']).toEqual("6029101")
        })

})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "0292020292114", "id": "registration_number"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['VEHICLE_REGISTRATION_NUMBER']).toEqual("0292020292114")
        })

})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "2DR", "id": "vehicle_type"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['VEHICLE_TYPE']).toEqual("2DR")
        })

})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "HONDA", "id": "vehicle_make"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['VEHICLE_MAKE']).toEqual("HONDA")
        })

})

test('test vehicle licence jurisdiction is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "ACCO", "id": "vehicle_model"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['VEHICLE_MODEL']).toEqual("ACCO")
        })

})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "2021", "id": "vehicle_year"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['VEHICLE_YEAR']).toEqual("2021")
        })

})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "BLU", "id": "vehicle_color"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['VEHICLE_COLOR']).toEqual("BLU")
        })

})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "BC", "id": "puj_code"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['VEHICLE_NSC_PUJ']).toEqual("BC")
        })

})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "610029", "id": "nsc_number"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['VEHICLE_NSC_NUMBER']).toEqual("610029")
        })

})

test('test vehicle licence number is shown on drivers copy', () => {
    store.commit("updateFormField", {"target": {"value": "2C3CCAGT1DH646504", "id": "vin_number"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['VEHICLE_VIN']).toEqual("2C3CCAGT1DH646504")
        })

})

test('test officers report populates witnessed by officer checkbox', () => {
    store.commit("updateCheckBox", { "target": { "value": "Witnessed by officer", "id": "operating_grounds"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['DRIVER_WITNESSED_BY_OFFICER']).toEqual(true)
        })
})

test('test officers report populates admission by driver checkbox', () => {
    store.commit("updateCheckBox", { "target": { "value": "Admission by driver", "id": "operating_grounds"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['DRIVER_ADMISSION_BY_DRIVER']).toEqual(true)
        })
})

test('test officers report populates independent witnessed checkbox', () => {
    store.commit("updateCheckBox", { "target": { "value": "Independent witness", "id": "operating_grounds"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['DRIVER_INDEPENDENT_WITNESS']).toEqual(true)
        })
})

test('test officers report populates other evidence checkbox', () => {
    store.commit("updateCheckBox", { "target": { "value": "Other", "id": "operating_grounds"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['DRIVER_OTHER']).toEqual(true)
        })
})

test('test officers report populates other memo if other is checked', () => {
    store.commit("updateFormField", { "target": { "value": "", "id": "operating_grounds"}})
    store.commit("updateCheckBox", { "target": { "value": "Other", "id": "operating_grounds"}})
    store.commit("updateFormField", { "target": { "value": "Some descriptive text", "id": "operating_ground_other"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['DRIVER_ADDITIONAL_INFORMATION']).toEqual("ADDITIONAL INFORMATION:SOME DESCRIPTIVE TEXT")
        })
})

test('test officers report does NOT populate other memo if other is NOT checked', () => {
    store.commit("updateFormField", { "target": { "value": "", "id": "operating_grounds"}})
    store.commit("updateCheckBox", { "target": { "value": "Independent Witness", "id": "operating_grounds"}})
    store.commit("updateFormField", { "target": { "value": "Some descriptive text", "id": "operating_ground_other"}})
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['DRIVER_ADDITIONAL_INFORMATION']).toEqual("")
        })
})

test('test alcohol alco-sensor test results displayed when selected', () => {
    store.commit("updateFormField", { "target": { "value": "Alcohol 215(2)", "id": "prohibition_type"}})
    store.commit("updateFormField", { "target": { "value": "Yes", "id": "prescribed_device"}})
    store.commit("updateFormField", { "target": { "value": "Alco-Sensor FST (ASD)", "id": "test_administered_asd"}})
    store.commit("updateFormField", { "target": { "value": "20501231", "id": "asd_expiry_date"}})
    store.commit("updateFormField", { "target": { "value": "51-99 mg%", "id": "result_alcohol"}})
    store.commit("updateFormField", { "target": { "value": "20220412", "id": "test_date"}})
    store.commit("updateFormField", { "target": { "value": "1442", "id": "test_time"}})

    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['REASON_ALCOHOL_215']).toEqual(true)
            expect(actual['REASONABLE_GROUNDS_YES']).toEqual(true)
            expect(actual['REASONABLE_GROUNDS_TEST_ALCO_SENSOR']).toEqual(true)
            expect(actual['REASONABLE_GROUNDS_TEST_ASD_EXPIRY_DATE']).toEqual("20501231")
            expect(actual['REASONABLE_GROUNDS_ALCOHOL_51-99']).toEqual(true)
            expect(actual['REASONABLE_GROUNDS_ALCOHOL_OVER_99']).toEqual(false)
            expect(actual['REASONABLE_GROUNDS_TEST_TIME']).toEqual("2022-04-12 14:42")
        })
})

test('test alcohol alco-sensor test results not displayed when not selected', () => {
    store.commit("updateFormField", { "target": { "value": "Alcohol 215(2)", "id": "prohibition_type"}})
    store.commit("updateFormField", { "target": { "value": "Yes", "id": "prescribed_device"}})
    store.commit("updateFormField", { "target": { "value": "", "id": "test_administered_asd"}})
    store.commit("updateFormField", { "target": { "value": "20501231", "id": "asd_expiry_date"}})
    store.commit("updateFormField", { "target": { "value": "51-99 mg%", "id": "result_alcohol"}})
    store.commit("updateFormField", { "target": { "value": "20220412", "id": "test_date"}})
    store.commit("updateFormField", { "target": { "value": "1442", "id": "test_time"}})

    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['REASON_ALCOHOL_215']).toEqual(true)
            expect(actual['REASONABLE_GROUNDS_YES']).toEqual(true)
            expect(actual['REASONABLE_GROUNDS_TEST_ALCO_SENSOR']).toEqual(false)
            expect(actual['REASONABLE_GROUNDS_TEST_ASD_EXPIRY_DATE']).toEqual(undefined)
            expect(actual['REASONABLE_GROUNDS_ALCOHOL_51-99']).toEqual(undefined)
            expect(actual['REASONABLE_GROUNDS_ALCOHOL_OVER_99']).toEqual(undefined)
            expect(actual['REASONABLE_GROUNDS_TEST_TIME']).toEqual("2022-04-12 14:42")
        })
})

test('test when vehicle not impounded, previously selected impounded options are not shown', () => {
    store.commit("updateFormField", {"target": {"value": "No", "id": "vehicle_impounded"}})
    store.commit("updateFormField", {"target": {"value": "With vehicle", "id": "location_of_keys"}})
    store.commit("updateFormField", {"target": {
        "value": "Buster's Towing Ltd, 435 Industrial Avenue, Vancouver, 604-685-7246", "id": "impound_lot_operator"}})
    // console.debug("ILO: " + store.getters.getAttributeValue("impound_lot_operator"))
    store.dispatch("getPrintMappings", state.currently_editing_form_object)
        .then( (actual) => {
            expect(actual['NOT_IMPOUNDED']).toEqual(true)
            expect(actual['IMPOUNDED']).toEqual(false)
            expect(actual['RELEASE_LOCATION_KEYS']).toEqual(undefined)
            expect(actual['IMPOUNDED_LOT']).toEqual(undefined)
            expect(actual['IMPOUNDED_ADDRESS']).toEqual(undefined)
            expect(actual['IMPOUNDED_PHONE_AREA_CODE']).toEqual(undefined)
            expect(actual['IMPOUNDED_PHONE_NUMBER']).toEqual(undefined)
        })

})