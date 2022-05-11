import { getters } from '../store/getters.js';
import moment from "moment";
import constants from "../config/constants";


test('test getAppVersion() displays current version', () => {
    // mock state
    const state = {
       version: "0.0.13"
      }
    let result = getters.getAppVersion(state)
    expect(result).toEqual("0.0.13")

})


test('test getAllEditedForm() returns an array of edited forms', () => {
    // mock state
    const state = {
       forms: {
           "12Hour": {
               "AA-111111": {
                   "form_id": "AA-111111",
                   "lease_expiry": "2021-10-02",
                   "data": {
                       "driver_last_name": "Smith"
                   }
               },
               "AA-111112": {
                   "form_id":  "AA-111112",
                   "lease_expiry": "2021-10-02",
               }
           },
           "24Hour": {
               "BB-111112": {
                   "form_id":  "BB-111112",
                   "lease_expiry": "2021-10-02",
               },
               "BB-111113": {
                   "form_id":  "BB-111113",
                   "lease_expiry": "2021-10-02",
               }

           }
       }
      }
    let result = getters.getAllEditedFormsNotPrinted(state)
    expect(result).toEqual([
        {
           "form_id": "AA-111111",
           "lease_expiry": "2021-10-02",
           "data": {
               "driver_last_name": "Smith"
           }
       }
    ])

})

test('test arrayOfFormsRequiringRenewal() returns an array of forms requiring lease renewal', () => {

    const future_date = moment().add(constants.UNIQUE_ID_REFRESH_DAYS + 1, "days").format("YYYY-MM-DD")
    const state = {
       forms: {
           "12Hour": {
               "AA-111111": {
                   "form_id": "AA-111111",
                   "form_type": "12Hour",
                   "printed_timestamp": "2021-09-02",
                   "lease_expiry": "2021-09-02",
                   "data": {
                       "driver_last_name": "Smith"
                   }
               },
               "AA-111112": {
                   "form_id":  "AA-111112",
                   "form_type": "12Hour",
                   "printed_timestamp": null,
                   "lease_expiry": future_date,
               }
           },
           "24Hour": {
               "BB-111112": {
                   "form_id":  "BB-111112",
                   "form_type": "24Hour",
                   "printed_timestamp": null,
                   "lease_expiry": future_date,
               },
               "BB-111113": {
                   "form_id":  "BB-111113",
                   "form_type": "24Hour",
                   "lease_expiry": "2021-09-17",
                   "printed_timestamp": null,
               }

           }
       }
      }
    let result = getters.arrayOfFormsRequiringRenewal(state)
    expect(result).toHaveLength(1)
    expect(result[0]).toHaveProperty("form_id")
    expect(result[0]).toHaveProperty("lease_expiry")
    expect(result[0].form_id).toEqual("BB-111113")

})


test('test isFormEditable() returns true when form has not been served', () => {

    const state = {
        "forms": {
            "12Hour": {
                "AA-111111": {
                    "form_id": "AA-111111",
                    "form_type": "12Hour",
                    "printed_timestamp": null,
                    "lease_expiry": "2021-09-02",
                    "data": {
                        "driver_last_name": "Smith"
                    }
                }
            }
        }
    };
    const form_object = {
       "form_id": "AA-111111",
       "form_type": "12Hour",
      }
    let result = getters.isFormEditable(state)(form_object)
    expect(result).toEqual(true)

})

test('test isFormEditable() returns false when form has been served', () => {

    const state = {
        "forms": {
            "12Hour": {
                "AA-111111": {
                    "form_id": "AA-111111",
                    "form_type": "12Hour",
                    "printed_timestamp": "2021-08-15",
                    "lease_expiry": "2021-09-02",
                    "data": {
                        "driver_last_name": "Smith"
                    }
                }
            }
        }
    };
    const form_object = {
       "form_id": "AA-111111",
       "form_type": "12Hour",
      }
    let result = getters.isFormEditable(state)(form_object)
    expect(result).toEqual(false)

})