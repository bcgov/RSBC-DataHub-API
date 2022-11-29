import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import { BootstrapVue, BootstrapVueIcons, ModalPlugin } from 'bootstrap-vue'
import { ValidationProvider } from 'vee-validate';
import VueKeyCloak from '@dsb-norge/vue-keycloak-js'
import router from '@/router'
import VueMask from 'v-mask'
import "./filters";
import "@/styles/index.scss";

import "@/config/custom_stylesheet.scss";
import rsiStore from "@/store"

import './registerServiceWorker'
import constants from "@/config/constants";

import {downloadLookupTables, fetchStaticLookupTables} from "@/utils/calls"
import {getMoreFormsFromApiIfNecessary, getAllFormsFromDB, saveCurrentFormToDB} from "@/utils/forms"
import {updateUserIsAuthenticated} from "@/utils/userAuth"

Vue.use(Vuex)

// Make BootstrapVue components throughout your project
Vue.use(BootstrapVue)
Vue.use(ModalPlugin)
Vue.use(BootstrapVueIcons)
Vue.use(VueMask);


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

    await getAllFormsFromDB();

    // download lookup tables while offline
    // await rsiStore.dispatch("downloadLookupTables")
    downloadLookupTables()

  },
  render: h => h(App),
}).$mount('#app')


rsiStore.subscribe((mutation) => {
      if (mutation.type === 'setKeycloak') {
        getMoreFormsFromApiIfNecessary()
        // TODO - store.dispatch("renewFormLeasesFromApiIfNecessary")
        fetchStaticLookupTables({"resource": "user_roles", "admin": false, "static": false})
          .then(data => {
              updateUserIsAuthenticated(data)
          })

        fetchStaticLookupTables({"resource": "users", "admin": false, "static": false})
      }
      if (mutation.type === 'updateFormField' ||
          mutation.type === 'updateFormAttribute' ||
          mutation.type === 'updateCheckBox' ||
          mutation.type === 'populateDriverFromICBC' ||
          mutation.type === 'populateVehicleFromICBC' ||
          mutation.type === 'typeAheadUpdate' ||
          mutation.type === 'updateFormInRoot' ||
          mutation.type === 'setFormAsPrinted' ||
          mutation.type === 'addHtmlToForm'
      ) {
        saveCurrentFormToDB(rsiStore.state.Common.currently_editing_form_object)
      }
    });




