<template>
  <div class="card bg-light border-secondary mb-3">
      <div class="card-body text-dark">
        <span class="font-weight-bold">Welcome!</span>
        it looks like you haven't used this app before.<br />
        <span class="small">Until you're authorized, this app is disabled.
          <span v-if="! hasUserApplied" @click="showApplication = ! showApplication" class="text-secondary">
            {{ this.showApplicationLabel }}
          </span>
        </span>
        <div v-if="showApplication && ! hasUserApplied" class="d-flex justify-content-center mt-2">
          <div class="form-row pl-2">
            <div class="form-group">
              <label for="first_name">First Name</label>
              <input type="text"
                   class="form-control"
                   id="first_name"
                   v-model="application.first_name">
            </div>
          </div>
          <div class="form-row pl-2">
            <div class="form-group">
              <label for="last_name">Last Name</label>
              <input type="text"
                   class="form-control"
                   id="last_name"
                   v-model="application.last_name">
            </div>
          </div>
          <div class="form-row pl-2">
            <div class="form-group">
              <label for="badge_number">Badge Number</label>
              <input type="text"
                   class="form-control"
                   id="badge_number"
                   v-model="application.badge_number">
            </div>
          </div>
          <div class="form-row pl-2">
            <div class="form-group">
              <label for="agency">Agency</label>
              <input type="text"
                   class="form-control"
                   id="agency"
                   v-model="application.agency">
            </div>
          </div>
          <div class="form-row pl-2">
            <div class="form-group">
              <label for="keycloak_username">Username</label>
              <div class="form-inline">
                <input type="text"
                     class="form-control"
                     id="keycloak_username"
                     :value=getKeycloakUsername
                     :disabled=true>
                <button @click="dispatchUnlock" class="btn btn-secondary">
                  Apply
                  <b-spinner v-if="showSpinner" small></b-spinner>
                </button>
              </div>
            </div>
          </div>

          <div class="row">


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


export default {
  name: "UserNotPermittedBanner",
  data() {
    return {
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
    dispatchUnlock() {
      this.showSpinner = true
      this.applyToUnlockApplication(this.application)
        .then(() => {
          this.showSpinner = false
          this.showApplication = false
        })
        .catch(() => {
          this.showSpinner = false
        })
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
  }
}
</script>

<style>
#apply-button button {
  border: red 2px solid;
  vertical-align: bottom;
}

</style>