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
          <div class="form-inline">
            <div class="form-group">
              <label v-if="false" for="keycloak_username">Username</label>
              <input type="text"
                   class="form-group"
                   id="keycloak_username"
                   :value=getKeycloakUsername
                   :disabled=true>
              <button @click="dispatchUnlock" class="btn btn-secondary btn-sm">
                Apply
                <b-spinner v-if="showSpinner" small></b-spinner>
              </button>
            </div>
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
      showApplication: false,
      showSpinner: false
    }
  },
  methods: {
    ...mapActions(['applyToUnlockApplication']),
    dispatchUnlock() {
      this.showSpinner = true
      this.applyToUnlockApplication()
        .then(() => {
          this.showSpinner = false
        })
        .catch(() => {
          this.showSpinner = false
        })
    }
  },
  computed: {
    ...mapGetters(['getKeycloakUsername', 'hasUserApplied']),
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