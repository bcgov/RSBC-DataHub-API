<template>
  <div class="card bg-light border-secondary mb-3">
    <div class="card-body text-dark">
      <div v-if="! showApplicationReceived">
        <p>
          <span class="font-weight-bold" style="font-size:x-large">Welcome to the Digital Forms system</span>
        </p>
        <p>
          <em>Warning: This system is available to authorized law enforcement officers only.</em>
        </p>
        <p>
          You currently do not have access to the Digital Forms system.
        </p>
        <p>
          Please apply for access after completing the training course and with the approval of your unit commander.
        </p>
      </div>
      <div class="btn btn-primary" v-if="! showApplicationReceived && ! showApplication" @click="showApplication = true">
        Apply for Access
      </div>
      <div v-if="showApplication && ! showApplicationReceived">
        <p>
          <b>Example</b>
        </p>
        <p>
          <table class="small" cols="3" width="50%" style="margin-left:auto;margin-right:auto;">
            <tr>
              <td>SURNAME</td>
              <td><span class="font-weight-bold">SHERWOOD</span></td>
              <td>ALL CAPITALIZED</td>
            </tr>
            <tr>
              <td>Given</td>
              <td><span class="font-weight-bold">Percy</span></td>
              <td>Normal Case</td>
            </tr>
            <tr>
              <td>Agency</td>
              <td><span class="font-weight-bold">Dominion Police</span></td>
              <td>Use "Dept." instead of "Department"</td>
            </tr>
            <tr>
              <td>PRIME ID</td>
              <td><span class="font-weight-bold">DO1854</span></td>
              <td>The ID you use to login to the MDT</td>
            </tr>
          </table>
        </p>
        <div class="d-flex justify-content-center mt-2">
          <div class="form-row pl-2">
            <application-field fg_class="col-sm-3" id="last_name" @modified="modified_event" :errors="errors">SURNAME</application-field>
            <application-field fg_class="col-sm-3" id="first_name" @modified="modified_event" :errors="errors">Given</application-field>
            <application-field fg_class="col-sm-3" id="agency" @modified="modified_event" :errors="errors">Agency</application-field>
            <application-field fg_class="col-sm-2" id="badge_number" @modified="modified_event" :errors="errors">PRIME ID</application-field>
          </div>
        </div>
        <div>
          <button @click="dispatchUnlock" class="btn btn-secondary">
            Apply
          <b-spinner v-if="showSpinner" small></b-spinner>
          </button>
        </div>
      </div>
      <div v-if="showApplicationReceived">
      <p>
      <span class="font-weight-bold">Application received.</span> Thank you!
      </p>
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
        showApplicationReceived: false
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
            this.showApplicationReceived = true
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
      ...mapGetters(['getKeycloakUsername', 'hasUserApplied', 'getAgencyName'])
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