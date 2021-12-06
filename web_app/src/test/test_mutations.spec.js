import { mutations } from '../store/mutations.js';
import moment from "moment";

test('test stopEditingCurrentForm()', () => {
    // mock state
    const state = { currently_editing_form_object: {
        form_id: "AA-222222",
        form_type: "24Hour"
      }}
    // apply mutation
    mutations.stopEditingCurrentForm(state)
    // assert result
    expect(state.currently_editing_form_object.form_id).toEqual(null)
    expect(state.currently_editing_form_object.form_type).toEqual(null)

})

test('test editExistingForm()', () => {

    const payload = {
        form_id: "AA-111111",
        form_type: "12Hour"
    }
    // mock state
    const state = { currently_editing_form_object: {
        form_id: null,
        form_type: null
      }}
    // apply mutation
    mutations.editExistingForm(state, payload)
    // assert result
    expect(state.currently_editing_form_object.form_id).toEqual("AA-111111")
    expect(state.currently_editing_form_object.form_type).toEqual("12Hour")

})

test('test updateFormField when data attribute exists in store', () => {

    const payload = {
        target: {
            id: "driver_last_name",
            value: "Smith"
        }
    }
    // mock state
    const state = {
        currently_editing_form_object: {
            form_id: "AA-111111",
            form_type: "12Hour"
          },
        forms: {
            "12Hour": {
                "AA-111111": {
                    "data": {
                        "driver_first_name": "Dan",
                        "driver_last_name": "Jones"
                    }
                }
            }
        }
    }
    // apply mutation
    mutations.updateFormField(state, payload)
    // assert result
    const root = state.forms["12Hour"]["AA-111111"].data
    expect(root.driver_last_name).toEqual("Smith") // Updated from payload
    expect(root.driver_first_name).toEqual("Dan")  // Unchanged

})

test('test updateFormField when data attribute does not exist in store', () => {

    const payload = {
        target: {
            id: "driver_last_name",
            value: "Smith"
        }
    }
    // mock state
    const state = {
        currently_editing_form_object: {
            form_id: "AA-111111",
            form_type: "12Hour"
          },
        forms: {
            "12Hour": {
                "AA-111111": {
                    "data": {
                        "driver_first_name": "Dan",
                    }
                }
            }
        }
    }
    // apply mutation
    mutations.updateFormField(state, payload)
    // assert result
    const root = state.forms["12Hour"]["AA-111111"].data
    expect(root.driver_last_name).toEqual("Smith") // Updated from payload

})

test('test adding first item to checkbox values using updateCheckBox()', () => {

    const payload = {
        target: {
            id: "checkbox_list",
            value: "Selected A"
        }
    }
    // mock state
    const state = {
        currently_editing_form_object: {
            form_id: "AA-111111",
            form_type: "12Hour"
          },
        forms: {
            "12Hour": {
                "AA-111111": {
                    "data": {
                        "driver_first_name": "Dan",
                    }
                }
            }
        }
    }
    // apply mutation
    mutations.updateCheckBox(state, payload)
    // assert result
    const root = state.forms["12Hour"]["AA-111111"].data
    expect(root.checkbox_list).toContain("Selected A") // Updated from payload

})

test('test adding a second item of checkbox values using updateCheckBox()', () => {

    const payload = {
        target: {
            id: "checkbox_list",
            value: "Selected B"
        }
    }
    // mock state
    const state = {
        currently_editing_form_object: {
            form_id: "AA-111111",
            form_type: "12Hour"
          },
        forms: {
            "12Hour": {
                "AA-111111": {
                    "data": {
                        "checkbox_list": ['Selected A'],
                    }
                }
            }
        }
    }
    // apply mutation
    mutations.updateCheckBox(state, payload)
    // assert result
    const root = state.forms["12Hour"]["AA-111111"].data
    expect(root.checkbox_list).toEqual(["Selected A", "Selected B"]) // Updated from payload

})

test('test removing an item that already exists using updateCheckBox()', () => {

    const payload = {
        target: {
            id: "checkbox_list",
            value: "Selected A"
        }
    }
    // mock state
    const state = {
        currently_editing_form_object: {
            form_id: "AA-111111",
            form_type: "12Hour"
          },
        forms: {
            "12Hour": {
                "AA-111111": {
                    "data": {
                        "checkbox_list": ['Selected A'],
                    }
                }
            }
        }
    }
    // apply mutation
    mutations.updateCheckBox(state, payload)
    // assert result
    const root = state.forms["12Hour"]["AA-111111"].data
    expect(root.checkbox_list).toEqual([]) // Updated from payload

})

test('test that deleteForm() removes the "data" attribute from a specific form', () => {

    const payload = {
        form_id: "AA-111111",
        form_type: "12Hour"
    }
    // mock state
    const state = {
        forms: {
            "12Hour": {
                "AA-111111": {
                    "form_id": "AA-111111",
                    "form_type": "12Hour",
                    "data": {
                        "some_attribute": "some value",
                    }
                }
            }
        }
    }
    // apply mutation
    mutations.deleteForm(state, payload)
    // assert result
    const root = state.forms["12Hour"]["AA-111111"]
    expect(root).not.toContain("data")
    expect(root).toHaveProperty("form_type")
    expect(root).toHaveProperty("form_id")
})

test('test when form is served, served status is updated', () => {
    const current_timestamp = moment.now()
    // mock state
    const state = {
        currently_editing_form_object: {
            form_id: "AA-111111",
            form_type: "12Hour"
          },
        forms: {
            "12Hour": {
                "AA-111111": {
                    "form_id": "AA-111111",
                    "form_type": "12Hour",
                    "printed_timestamp": null,
                    "data": {
                        "some_attribute": "some value",
                    }
                }
            }
        }
    }
    // apply mutation
    mutations.markFormStatusAsServed(state, current_timestamp)
    // assert result
    const root = state.forms["12Hour"]["AA-111111"]
    expect(root.printed_timestamp).toEqual(current_timestamp)
})
