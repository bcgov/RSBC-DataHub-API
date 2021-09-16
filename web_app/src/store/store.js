import Vue from 'vue'
import Vuex from 'vuex'
import {getters} from "@/store/getters";
import {actions} from "@/store/actions"
import {mutations} from "@/store/mutations";
import {version} from "../../package.json";

Vue.use(Vuex)


export const store = new Vuex.Store ({
  state: {
    version: version,
    isOnline: null,
    forms: {
      "IRP": {},
      "24Hour": {},
      "12Hour": {}
    },
    currently_editing_form_object: {
      "form_type": null,
      "form_id": null
    },
    form_schemas: {
      forms: {
        "12Hour": {
          "component": "TwelveHourProhibition",
          "form_type": "12Hour",
          "steps": ["Prohibition" ,"Validate & Serve"],
          "description": "12 Hour Driving Suspension",
          "full_name": "MV2906",
          "pdf_template": "MV2906_12h_Suspension_2021-04-27.pdf"
        },
        "24Hour": {
          "component": "TwentyFourHourProhibition",
          "steps": ["Prohibition" ,"Validate & Serve"],
          "form_type": "24Hour",
          "description": "24-Hour Prohibition",
          "full_name": "MV2634",
          "pdf_template": "MV2634_24h_Prohibition_2021-04-27.pdf"
        },
        "IRP": {
          "component": "ImmediateRoadsideProhibition",
          "form_type": "IRP",
          "description": "Immediate Roadside Prohibition",
          "full_name": "MV2723",
          "pdf_template": "MV2906_12h_Suspension_2021-04-27.pdf"
        }
      }
    },
    impound_lot_operators: [],
    provinces: [],
    jurisdictions: [],
    countries: [],
    cities: [],
    colors: [],
    vehicles: [],
    pickup_locations: [],
    ROADSAFETY_EMAIL: '[to_be_determined@gov.bc.ca]',
    icbc_vehicle_lookup: []
  },

  getters: getters,
  mutations: mutations,
  actions: actions
})

