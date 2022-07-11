import moment from "moment";
export default {

    API_ROOT_URL: process.env.VUE_APP_API_ROOT_URL,

    // Number of days before this app will refresh unique prohibition ids.  The unique
    // id expiry date is set by the prohibition web service (currently set to 30 days),
    // but this app determines when to refresh the list.  If the app waited until the
    // unique ids had expired the officer could be find themselves offline with no
    // unique ids.
    UNIQUE_ID_REFRESH_DAYS: 15,

    // The minimum number of unique ids per type to have in storage before requesting more.
    MINIMUM_NUMBER_OF_UNIQUE_IDS_PER_TYPE: 10,

    // The maximum number of times app will attempt to retrieve unique IDs
    MAX_NUMBER_UNIQUE_ID_FETCH_ATTEMPTS: 2,

    MIN_VEHICLE_YEAR: 1900,
    MAX_VEHICLE_YEAR: moment().add(1, "years").format("YYYY"),

    TIMEZONE: "America/Vancouver",

    ROAD_SAFETY_CONTACT: 'RSIOpsSupport',

}