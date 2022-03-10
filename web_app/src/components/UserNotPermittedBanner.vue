<template>
  <div class="card bg-light border-secondary mb-3">
      <div class="card-body text-dark">
        <span class="font-weight-bold">Welcome!</span>
        It looks like you haven't used this app before.<br />
        <span class="small">Until you're authorized, this app is disabled.
          <span v-if="! hasUserApplied" @click="showApplication = ! showApplication" class="text-secondary">
            {{ this.showApplicationLabel }}
          </span>
        </span>
        <div v-if="showApplication && ! hasUserApplied" class="d-flex justify-content-center mt-2">
          <div class="form-row pl-2">
            <application-field id="first_name" @modified="modified_event" :errors="errors">First Name</application-field>
          </div>
          <div class="form-row pl-2">
            <application-field id="last_name" @modified="modified_event" :errors="errors">Last Name</application-field>
          </div>
          <div class="form-row pl-2">
            <application-field id="badge_number" @modified="modified_event" :errors="errors">Badge Number</application-field>
          </div>
          <div class="form-row pl-2">
            <application-field id="agency" @modified="modified_event" :errors="errors">Agency</application-field>
            <button @click="dispatchUnlock" class="btn btn-secondary">
              Apply
              <b-spinner v-if="showSpinner" small></b-spinner>
            </button>
          </div>
        </div>
        <div v-if="hasUserApplied" class="text-muted small">
          Waiting for the administrator to unlock
        </div>
    </div>
  </div>
</template>

<script>

import {mapGetters, mapActions} from "vuex";
import ApplicationField from "@/components/ApplicationField";
import Vue from 'vue'


export default {
  name: "UserNotPermittedBanner",
  data() {
    return {
      errors: {
        first_name: [],
        last_name: [],
        badge_number: [],
        agency: []
      },
      application: {
        first_name: '',
        last_name: '',
        badge_number: '',
        agency: this.$store.getters.getAgencyName
      },
      showApplication: false,
      showSpinner: false,
    }
  },
  methods: {
    ...mapActions(['applyToUnlockApplication']),
    async dispatchUnlock() {
      this.showSpinner = true
      await this.applyToUnlockApplication(this.application)
        .then(() => {
          this.showSpinner = false
          this.showApplication = false
        })
        .catch((errors) => {
          errors.then( (data) => {
            console.log("applyToUnlockApplication failed", data.errors)
            Vue.set(this, "errors", data.errors)
          })
          this.showApplication = true
          this.showSpinner = false
        })
    },
    modified_event(payload) {
      console.log(payload)
      Vue.set(this.application, payload['id'], payload['value'])
    }
  },
  computed: {
    ...mapGetters(['getKeycloakUsername', 'hasUserApplied', 'getAgencyName']),
    showApplicationLabel() {
      if (this.showApplication) {
        return 'Hide'
      } else {
        return 'Unlock'
      }
    }
  },
  components: {
    ApplicationField
  }
}
</script>

<style>
#apply-button button {
  border: red 2px solid;
  vertical-align: bottom;
}

</style>