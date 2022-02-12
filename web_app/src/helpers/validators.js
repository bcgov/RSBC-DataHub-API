import moment from 'moment';
import {extend} from "vee-validate";

extend('secret', {
  validate: value => value === 'example',
  message: 'This is not the magic word'
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
  validate: value => moment(value, "YYYYMMDD", true).isValid(),
  message: "That's not a valid date"
});

// extend('validDtTime', {
//   validate(value) {
//     console.log("validDtTime " + value)
//     return {
//       required: true,
//       valid: moment(value, "YYYYMMDD HHmm", true).isValid()
//     };
//   },
//   message: "That's not a valid date time"
// });

extend('notExpired', {
  validate: value => moment().diff(moment(value, 'YYYYMMDD', true), 'days') < 0,
  message: "Expired"
});

extend('notFutureDt', {
  validate(value) {
    return {
      required: true,
      valid: moment().diff(moment(value, 'YYYYMMDD HHmm', true), 'minutes') > 0,
    };
  },
  message: "Cannot be future dated",
  computesRequired: true
});

extend('dob', {
  validate(value) {
    const dob_dt = moment(value, "YYYYMMDD", true)
    const dob_years = moment().diff(dob_dt, 'years')
    return {
      required: true,
      valid: dob_years > 16 && dob_years < 120,
    };
  },
  message: "Driver must be between 16 and 120 years old",
  computesRequired: true
});


extend('bac_result', {
  validate(value) {
    return {
      required: true,
      valid: value >= 1 && value < 999,
    };
  },
  message: "BAC results must be between 1 and 999",
  computesRequired: true
});



extend('plate_year', {
  validate(value) {
    return {
      required: true,
      valid: value >= 2000 && value < parseInt(moment().format("YYYY")) + 1,
    };
  },
  message: "Plate year must be between 2000 and the current year",
  computesRequired: true
});


extend('phone', {
  validate(value) {
    let result = false;
    const regexMatch = value.match("^[0-9]{10}$")
    if (Array.isArray(regexMatch)) {
       result = regexMatch[0] === value;
    }
    return {
      valid: result
    };
  },
  message: "Phone number format ##########"
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
      valid: value.length < 5,
    };
  },
  message: "Value must be than 5 chars",
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


