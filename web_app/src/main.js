import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import { BootstrapVue, BootstrapVueIcons, ModalPlugin, BTooltip  } from 'bootstrap-vue'
import { ValidationProvider } from 'vee-validate';
import VueKeyCloak from '@dsb-norge/vue-keycloak-js'
import router from '@/router'
import VueMask from 'v-mask'


import "@/config/custom_stylesheet.scss";
import {rsiStore} from "@/store/store.js"

import './registerServiceWorker'
import constants from "@/config/constants";


Vue.use(Vuex)

// Make BootstrapVue components throughout your project
Vue.use(BootstrapVue)
Vue.use(ModalPlugin)
Vue.use(BootstrapVueIcons)
Vue.use(VueMask);
Vue.component('b-tooltip', BTooltip);


// import custom validation rules
require("@/helpers/validators");
Vue.component('ValidationProvider', ValidationProvider);

Vue.config.productionTip = false


Vue.use(VueKeyCloak, {
  init: {
    onLoad: 'check-sso',
    pkceMethod: "S256",
  },
  config: constants.API_ROOT_URL + '/api/v1/static/keycloak',
  onReady: () => {
    rsiStore.commit("setKeycloak", Vue.prototype.$keycloak)
  }
});


new Vue({
  router,
  store: rsiStore,
  async created() {

    await rsiStore.dispatch("getAllFormsFromDB");

    // download lookup tables while offline
    await rsiStore.dispatch("downloadLookupTables")

  },
  render: h => h(App),
}).$mount('#app')


rsiStore.subscribe((mutation) => {
      if (mutation.type === 'setKeycloak') {
        rsiStore.dispatch("getMoreFormsFromApiIfNecessary")
        // TODO - store.dispatch("renewFormLeasesFromApiIfNecessary")
        rsiStore.dispatch("fetchStaticLookupTables", {"resource": "user_roles", "admin": false, "static": false})
            .then(data => {
                rsiStore.dispatch("updateUserIsAuthenticated", data)
            })
        rsiStore.dispatch("fetchStaticLookupTables", {"resource": "users", "admin": false, "static": false})
      }
      if (mutation.type === 'updateFormField' ||
          mutation.type === 'updateFormAttribute' ||
          mutation.type === 'updateCheckBox' ||
          mutation.type === 'populateDriverFromICBC' ||
          mutation.type === 'populateVehicleFromICBC' ||
          mutation.type === 'typeAheadUpdate'
      ) {
        rsiStore.dispatch("saveCurrentFormToDB", rsiStore.state.currently_editing_form_object)
      }
    });




