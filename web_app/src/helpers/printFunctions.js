import checkDigit from "./checkDigit";
import moment from "moment-timezone";
import constants from "../config/constants";


export default {

    getFormattedFormId(form_data) {
        if ("form_id" in form_data) {
            const sixDigitString = form_data.form_id.substr(2,7)
            const digit = checkDigit.checkDigit(sixDigitString)
            return form_data.form_id.substr(0,2) + "-" + sixDigitString + digit
        }
        return ''
    },

    getFormIdForBarCode(form_data) {
        if ("form_id" in form_data) {
            const sixDigitString = form_data.form_id.substr(2,7)
            const digit = checkDigit.checkDigit(sixDigitString)
            return "*" + sixDigitString + digit + "*"
        }
        return ''
    },

    getStringValue(form_data, attribute) {
        if (attribute in form_data.data) {
            return form_data.data[attribute].toUpperCase()
        }
        return ''
    },

    getDateValue(form_data, attribute) {
        if (attribute in form_data.data) {
            const date_time = moment(form_data.data[attribute], 'YYYYMMDD', true)
            return date_time.format("YYYY-MM-DD")
        }
        return ''
    },

    getDateFormat(form_data, [attribute, format]) {
        if (attribute in form_data.data) {
            const date_time = moment(form_data.data[attribute], 'YYYYMMDD', true)
            return date_time.format(format)
        }
        return ''
    },


    getTimeFormat(form_data, [attribute, format]) {
        if (attribute in form_data.data) {
            const date_time = moment(form_data.data[attribute], 'HHmm', true)
            return date_time.format(format)
        }
        return ''
    },

    getDateTimeValue(form_data, date_and_time_array) {
        if (date_and_time_array[0] in form_data.data && date_and_time_array[1] in form_data.data) {
            const date_time_string = form_data.data[date_and_time_array[0]] + " " + form_data.data[date_and_time_array[1]]
            const date_time = moment.tz(date_time_string, 'YYYYMMDD HHmm', true, constants.TIMEZONE)
            return date_time.format("YYYY-MM-DD")
        }
        return ''
    },

    getJurisdictionCode(form_data, attribute) {
        if (attribute in form_data.data) {
            if ('objectCd' in form_data.data[attribute]) {
                return form_data.data[attribute].objectCd
            }
        }
        return ''
    },

    getValuesConcatenatedWithCommas(form_data, attributes_array) {
        let attributeValues = []
        attributes_array.forEach( (attribute) => {
            if (attribute in form_data.data) {
                attributeValues.push(form_data.data[attribute])
            }
        })
        return attributeValues.join(", ")
    },

    getPhoneAreaCodeValue(form_data, attribute) {
        if (attribute in form_data.data) {
            return form_data.data[attribute].substr(0, 3)
        }
        return ''
    },

    getPhoneValue(form_data, attribute) {
        if (attribute in form_data.data) {
            return form_data.data[attribute].substr(3,3) + "-" + form_data.data[attribute].substr(6,9)
        }
        return ''
    },

    getSubStringValue(form_data, [attribute, start, end]) {
        if (attribute in form_data.data) {
            return form_data.data[attribute].substr(start,end)
        }
        return ''
    },

    getIsChecked(form_data, [attribute, expectedValue]) {
        if (attribute in form_data.data) {
            return form_data.data[attribute].includes(expectedValue)
        }
        return false
    },

    getRadioValue(form_data, [attribute, expectedValue]) {
        if (attribute in form_data.data) {
            return (form_data.data[attribute] === expectedValue);
        }
        return false;
    },

    getImpoundLotOperator(form_data, key) {
        if ("impound_lot_operator" in form_data.data) {
            const ilo = form_data.data.impound_lot_operator
            if (key in ilo) {
                return ilo[key].toUpperCase();
            }
        }
        return '';
    },

    getIsFieldPopulated(form_data, attribute) {
        if (attribute in form_data.data) {
            return (form_data.data[attribute].length > 0)
        }
        return false
    },

    // print static text to the printout
    label(form_data, label_text) {
        return label_text
    },

    // --- methods below are being used as a temporary workaround until refactoring --- //

    isJurisdictionBC(form_data) {
        const attribute = "drivers_licence_jurisdiction"
        if (attribute in form_data.data) {
            if ('objectCd' in form_data.data[attribute]) {
                return (form_data.data[attribute].objectCd === "BC");
            }
        }
        return false;
    },

    isUnlicensed(form_data) {
        const attribute = "reason_unlicensed"
        if (attribute in form_data.data) {
            return (form_data.data[attribute] === true);
        }
        return false;
    },

    getJurisdictionIfUnlicensedAndOutOfProvince(form_data, attribute) {
        if(this.isUnlicensedAndOutOfProvince(form_data)) {
            if(attribute in form_data.data) {
                if ("objectCd" in form_data.data[attribute]) {
                    return form_data.data[attribute].objectCd
                }
                return ''
            }
        }
        return ''
    },

    getStringIfUnlicensedAndOutOfProvince(form_data, attribute) {
        if(this.isUnlicensedAndOutOfProvince(form_data)) {
            if(attribute in form_data.data) {
                return form_data.data[attribute]
            }
        }
        return ''
    },

    isUnlicensedAndOutOfProvince(form_data) {
        return ! this.isJurisdictionBC(form_data) && this.isUnlicensed(form_data)
    },

    getOwnerName(form_data) {
        if (this.getIsChecked(form_data, ["corporate_owner", "Owned by corporate entity"])) {
            return this.getStringValue(form_data, "owners_corporation")
        } else {
            return this.getValuesConcatenatedWithCommas(form_data, ["owners_last_name", "owners_first_name"])
        }
    }

}