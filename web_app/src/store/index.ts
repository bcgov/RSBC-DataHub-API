import Common from '@/store/modules/common';
import MV2906 from '@/store/modules/forms/mv2906';
import MV2634 from '@/store/modules/forms/mv2634';
import VI from './modules/forms/vi';
import IRP from './modules/forms/irp';
import {plugins} from "@/store/plugins";


import {getters} from "@/store/getters";
import {mutations} from "@/store/mutations";
// import {version} from "../../package.json";


import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex)

const rsiStore = new Vuex.Store({
	modules: {
		Common,
		MV2906,
		MV2634,
		VI,
		IRP
	},

	state: {
		admin_users: {},
		// agencies: [],
		// db_ready: false,
		// cities: [],
		// countries: [],
		// configuration: {
		//   environment: 'prod'
		// },
		// currently_editing_form_object: {
		//   "form_type": null,
		//   "form_id": null
		// },
		forms: {
		"IRP": {},
		"24Hour": {},
		"12Hour": {},
		"VI": {}
		},
		form_schemas: {
		forms: {
			"12Hour": {
			"component": "TwelveHourProhibition",
			"form_type": "12Hour",
			"label": "12-Hour",
			"description": "12-Hour Driving Suspension",
			"full_name": "MV2906",
			"documents": {
				"all": {
				"name": "Print All Copies",
				"reprint": true,
				"variants": ['icbc', 'driver', 'police']
				}
			},
			"disabled": false,
			"check_digit": false
			},
			"24Hour": {
			"component": "TwentyFourHourProhibition",
			"form_type": "24Hour",
			"label": "24-Hour",
			"description": "24-Hour Prohibition",
			"full_name": "MV2634",
			"documents": {
				"all": {
				"name": "Print All Copies",
				"reprint": true,
				"variants": ['icbc', 'driver', 'ilo', 'police']
				}
			},
			"disabled": false,
			"check_digit": false
			},
			"VI": {
			"component": "VehicleImpoundment",
			"form_type": "VI",
			"label": "VI",
			"description": "Vehicle Impoundment",
			"full_name": "MV2721 & MV2722",
			"documents": {
				"all": {
				"name": "Print All Copies",
				"reprint": true,
				"variants": ['driver', 'police', 'ilo', 'report']
				}
			},
			"disabled": true,
			"check_digit": true
			},
			"IRP": {
			"component": "ImmediateRoadsideProhibition",
			"form_type": "IRP",
			"label": "IRP",
			"description": "Immediate Roadside Prohibition",
			"full_name": "MV2723",
			"documents": {},
			"disabled": true,
			"check_digit": true
			}
		}
		},
		// icbc_vehicle_lookup: [],
		// impound_lot_operators: [],
		isUserAuthorized: null,
		// isOnline: true,
		// jurisdictions: [],
		keycloak: {},
		// loaded: {
		//   "agencies": false,
		//   "impound_lot_operators": false,
		//   "countries": false,
		//   "jurisdictions": false,
		//   "provinces": false,
		//   "cities": false,
		//   "vehicles": false,
		//   "vehicle_styles": false,
		//   "configuration": false,
		// },
		// pickup_locations: [],
		// provinces: [],
		user_roles: {},
		users: {
		agency: '',
		badge_number: '',
		first_name: '',
		last_name: '',
		user_guid: '',
		username: ''
		},
		// vehicles: [],
		// vehicle_styles: [],
		// version: version,
	},

	getters: getters,
	mutations: mutations,
	plugins: plugins
})

export default rsiStore