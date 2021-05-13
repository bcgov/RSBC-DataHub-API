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
  validate: value => moment(value, "YYYY-MM-DD", true).isValid(),
  message: "That's not a valid date"
});

extend('validDtTime', {
  validate: value => moment(value, "YYYY-MM-DD HH:mm", true).isValid(),
  message: "That's not a valid date time"
});

extend('notExpired', {
  validate: value => moment().diff(moment(value, 'YYYY-MM-DD', true), 'days') < 0,
  message: "Expired"
});

extend('dob', {
  validate(value) {
    return {
      required: true,
      valid: moment().diff(moment(value), 'years') > 5,
    };
  },
  message: "That's not a valid date-of-birth",
  computesRequired: true
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
  message: "That's not a valid phone number"
});



