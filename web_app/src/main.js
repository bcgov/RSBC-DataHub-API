import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import { BootstrapVue, BootstrapVueIcons, ModalPlugin } from 'bootstrap-vue'
import { ValidationProvider } from 'vee-validate';
import VueKeyCloak from '@dsb-norge/vue-keycloak-js'


import "@/config/custom_stylesheet.scss";
import {store} from "@/store/store.js"

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


Vue.use(VueKeyCloak, {
  onLoad: 'login-required',
  config: {
    realm: '',
    url: '',
    clientId: ''
  },
  onReady: kc => {
    console.log(`I wonder what Keycloak returns: ${kc}`)
    new Vue({
      store: store,
      async created() {
        await store.dispatch("getAllFormsFromDB");

        await store.dispatch("getMoreFormsFromApiIfNecessary")

        await store.dispatch("fetchStaticLookupTables", "impound_lot_operators")
        await store.dispatch("fetchStaticLookupTables", "countries")
        await store.dispatch("fetchStaticLookupTables", "jurisdictions")
        await store.dispatch("fetchStaticLookupTables", "provinces")
        await store.dispatch("fetchStaticLookupTables", "cities")
        await store.dispatch("fetchStaticLookupTables", "colors")
        await store.dispatch("fetchStaticLookupTables", "vehicles")

        // await store.dispatch("renewFormLeasesFromApiIfNecessary")

      },
      render: h => h(App),
    }).$mount('#app')

  }
})

