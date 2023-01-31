import moment from 'moment-timezone';
import { extend } from "vee-validate";
import { max } from 'vee-validate/dist/rules';
import constants from "@/config/constants";

extend('max', {
  ...max,
  message: 'Too many characters'
});

extend('bcdlNumberRule', {
  validate(value) {
    const regX = new RegExp(/^(\d{7})$/);
    return {
      valid: regX.test(value)
    };
  },
  message: 'BCDL numbers must have 7 digits'
});

extend('bcdlExpiryYear', {
  validate(value) {
    return {
      required: true,
      valid: moment(value, "YYYY", true).isValid()
    };
  },
  message: "That's not a valid year"
});

extend('required', {
  validate(value) {
    return {
      required: true,
      valid: ['', null, undefined].indexOf(value) === -1
    };
  },
  message: "This field is required",
  computesRequired: true
});

extend('validDt', {
  validate(value) {
    return {
      required: true,
      valid: moment(value, "YYYYMMDD", true).isValid()
    }
  },
  message: "That's not a valid date"
});

extend('validTime', {
  validate(value) {
    const not24 = parseInt(value.slice(0,2)) < 24
    return {
      required: true,
      valid: moment(value, "HHmm", true).isValid() && not24
    }
  },
  message: "That's not a valid time"
});

extend('notFutureDateTime', {
  params: ['relatedDate'],
  validate(value, {relatedDate}) {
    const date_time = moment.tz(relatedDate + " " + value, 'YYYYMMDD HHmm', true, constants.TIMEZONE)
    return {
      valid: moment().diff(date_time, 'minutes') >= 0
    }
  },
  hasTarget: true,
  message: "Date and time cannot be in the future"
});

extend('notExpiredDt', {
  validate(value) {
    return {
      required: true,
      valid: moment().diff(moment(value, 'YYYYMMDD', true), 'days') <= 0
    }
  },
  message: "Expired"
});

extend('notFutureDt', {
  validate(value) {
    const date_time = moment.tz(value + " 0000", 'YYYYMMDD HHmm', true, constants.TIMEZONE)
    return {
      required: true,
      valid: moment().diff(date_time, 'minutes') > 0,
    };
  },
  message: "Cannot be future dated",
});

extend('notGtYearAgo', {
  validate(value) {
    return {
      required: true,
      valid: moment().diff(moment(value, 'YYYYMMDD', true), 'days') < 364,
    };
  },
  message: "That's over a year ago",
});

extend('dob', {
  validate(value) {
    const dob_dt = moment(value, "YYYYMMDD", true)
    const dob_years = moment().diff(dob_dt, 'years')
    return {
      required: true,
      valid: dob_years >= 10 && dob_years <= 120,
    };
  },
  message: "Driver must be between 10 and 120 years old",
});

extend('notBeforeCareDateTime', {
  params: ['careDate', 'careTime', 'relatedDate'],
  validate(value, {careDate, careTime, relatedDate}) {
    const careDateTime = moment.tz(careDate + " " + careTime, 'YYYYMMDD HHmm', true, constants.TIMEZONE)
    const relatedDateTime = moment.tz(relatedDate + " " + value, 'YYYYMMDD HHmm', true, constants.TIMEZONE)
    return {
      valid: careDateTime.diff(relatedDateTime, 'minutes') <= 0
    }
  },
  hasTarget: true,
  message: "Cannot be before date/time of care or control"
});

extend('bac_result', {
  validate(value) {
    return {
      required: true,
      valid: value >= 1 && value < 999,
    };
  },
  message: "BAC results must be between 1 and 999",
});

extend('plate_year', {
  validate(value) {
    return {
      required: true,
      valid: value = 2000 && value <= parseInt(moment().format("YYYY")) + 1,
    };
  },
  message: "Plate year must be between 2000 and the current year",
});

extend('phone', {
  validate(value) {
    let result = false;
    const regexMatch = value.match("^[0-9]{3}-[0-9]{3}-[0-9]{4}$")
    if (Array.isArray(regexMatch)) {
       result = regexMatch[0] === value;
    }
    return {
      valid: result
    };
  },
  message: "Phone number format ###-###-####"
});

extend('email', {
  validate(value) {
    let result = false;
    const re = "^(([^<>()[\\]\\\\.,;:\\s@\"]+(\\.[^<>()[\\]\\\\.,;:\\s@\"]+)*)|(\".+\"))@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\])|(([a-zA-Z\\-0-9]+\\.)+[a-zA-Z]{2,}))$"
    const regexMatch = value.match(re)
    if (Array.isArray(regexMatch)) {
       result = regexMatch[0] === value;
    }
    return {
      valid: result
    };
  },
  message: "Email address format user@domain.com"
});

extend('lt25', {
  validate(value) {
    return {
      valid: value.length <= 25,
    };
  },
  message: "too long; must be less 25 chars",
});

extend('lt5', {
  validate(value) {
    return {
      valid: value.length <= 5,
    };
  },
  message: "Value must be less than 5 chars",
});

extend('lt3', {
  validate(value) {
    return {
      valid: value.length < 3,
    };
  },
  message: "Value must be less than 3 chars",
});

extend('lt4', {
  validate(value) {
    return {
      valid: value.length < 4,
    };
  },
  message: "Value must be than 4 chars",
});

extend('vehicleYear', {
  validate(value) {
    return {
      required: true,
      valid: moment(value, "YYYY", true).isValid()
    };
  },
  message: "That's not a valid year"
});

extend('vehicleYear', {
  validate(value) {
    const yearsOld = moment().diff(moment(value, 'YYYY', true), 'years')
    return {
      required: true,
      valid: yearsOld > -2 && value > 1900,
    };
  },
  message: "That's not a valid year"
});

extend('excessiveSpeed', {
  params: ['speedLimit'],
  validate(vehicleSpeed, {speedLimit}) {
    return {
      valid: vehicleSpeed - speedLimit >= 41
    }
  },
  hasTarget: true,
  message: "Must be at least 41 km/h over speed limit"
});

extend("offenceCityRules", {
  params: ['arrayOfCityObjects'],
  validate(value, {arrayOfCityObjects}) {
    const arrayOfCityCodes = arrayOfCityObjects.map( o => o.objectCd)
    return {
      required: true,
      valid: arrayOfCityCodes.includes(value.objectCd)
    }
  },
  message: 'Not a city in the list'
});

extend('primeLogin', {
  validate(value) {
    const regX = new RegExp(/^([A-Z0-9]{2}\d{4})$/);
    return {
      required: true,
      valid: regX.test(value)
    };
  },
  message: 'PRIME ID must exactly 2 letters + 4 digits OR 6 digits (HRMIS)'
});