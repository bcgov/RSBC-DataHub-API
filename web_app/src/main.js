import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import { BootstrapVue, BootstrapVueIcons, ModalPlugin } from 'bootstrap-vue'
import { ValidationProvider } from 'vee-validate';

import "@/config/custom_stylesheet.scss";
import getters from "@/store/getters.js"
import mutations from "@/store/mutations";
import actions from "@/store/actions";
import form_schemas from "@/config/form_schemas.json";
import bc_city_names from "@/config/cities.json";
import car_colors from "@/config/car_colors.json"
import './registerServiceWorker'

Vue.use(Vuex)

// Make BootstrapVue components throughout your project
Vue.use(BootstrapVue)
Vue.use(ModalPlugin)
Vue.use(BootstrapVueIcons)

// import custom validation rules
require("@/helpers/validators");
Vue.component('ValidationProvider', ValidationProvider);

Vue.config.productionTip = false

const store = new Vuex.Store({
  state: {
    provinces: ["BC", "AB"],
    isOnline: null,
    bc_city_names: bc_city_names,
    car_colors: car_colors,
    edited_forms: Array(),
    currently_editing_prohibition_index: null,
    form_schemas: form_schemas
  },
  mutations: mutations,
  getters: getters,
  actions: actions
})

new Vue({
  store: store,
  beforeCreate() { this.$store.commit("retrieveFormsFromLocalStorage")},
  render: h => h(App),
}).$mount('#app')
