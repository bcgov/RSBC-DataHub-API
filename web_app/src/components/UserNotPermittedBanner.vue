<template>
  <div class="card bg-light border-secondary mb-3">
    <div class="card-body text-dark">
      <div v-if="!showApplicationReceived">
        <p>
          <span class="font-weight-bold" style="font-size:x-large">Welcome to the Digital Forms system</span>
        </p>
        <p>
          <em>WARNING: This system is for use by authorized law enforcement officers only.</em>
        </p>
        <p>
          You currently do not have access to the Digital Forms system.
        </p>
        <p>
          Please apply for access after completing the training course and with the approval of your unit commander.
        </p>
      </div>
      <div v-if="!showApplicationReceived && !showApplication" class="btn btn-primary" @click="showApplication = true">
        Apply for Access
      </div>
      <div v-if="showApplication && !showApplicationReceived">
        <div class="d-flex justify-content-center mt-2">
          <div class="form-row pl-2">
            <application-field id="last_name" :errors="errors" fe_class="uppercase" fg_class="col-sm-3" @modified="modified_event">SURNAME</application-field>
            <application-field id="first_name" :errors="errors" fe_class="capitalize" fg_class="col-sm-3" @modified="modified_event">Given</application-field>
            <application-field-agency id="agency" :errors="errors" fg_class="col-sm-4" @modified="modified_event">Agency or RCMP Detachment</application-field-agency>
            <application-field id="badge_number" :errors="errors" fe_class="uppercase" fe_mask="NN####" fg_class="col-sm-2" @modified="modified_event">PRIME ID</application-field>
          </div>
        </div>
        <div class="container">
          <div class="row">
            <div class="col" />
            <div class="col-9 text-left">
              <p>
                <b-icon-exclamation-triangle-fill class="text-info" /> <span class="font-weight-bold">PRIME ID</span> is the username you use to log into the MDT (CAD) and the MRE.<br />
              </p>
              <ul>
                  <li>For independents, this is your agency's two-letter abbreviation followed by 2 to 4 numbers.</li><br />
                  <li>For RCMP members, this will be your 6 digit HRMIS.</li>
              </ul>
            </div>
            <div class="col" />
          </div>
        </div>     
        <div>
          <button class="btn btn-secondary" @click="dispatchUnlock">
            Apply for Access
            <b-spinner v-if="showSpinner" small></b-spinner>
          </button>
        </div>
      </div>
      <div v-if="showApplicationReceived">
        <p>
          <span class="font-weight-bold">Application received.</span> Thank-you!
        </p>
        <p>
          Your application will be reviewed and approved within 24 business hours.
        </p>
      </div>
    </div>
  </div>
</template>
<script>
  import ApplicationField from "@/components/ApplicationField";
  import ApplicationFieldAgency from "@/components/ApplicationFieldAgency";
  import Vue from 'vue';
  import { mapActions, mapGetters } from "vuex";
  export default {
    name: "UserNotPermittedBanner",
    components: {
      ApplicationField,
      ApplicationFieldAgency
    },
    computed: {
      ...mapGetters([
        'getArrayOfAgencies',
        'getKeycloakUsername',
        'hasUserApplied'
      ])
    },
    data() {
      return {
        application: {
          agency: '',
          badge_number: '',
          first_name: '',
          last_name: ''
        },
        errors: {
          agency: [],
          badge_number: [],
          first_name: [],
          last_name: []
        },
        showApplication: false,
        showApplicationReceived: false,
        showSpinner: false
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
              console.log("applyToUnlockApplication() failed", data.errors)
              Vue.set(this, "errors", data.errors)
            })
            this.showApplication = true
            this.showSpinner = false
          })
      },
      modified_event(payload) {
        Vue.set(this.application, payload['id'], payload['value'])
      }
    },
    watch: {
      'application.badge_number'() {
        this.application.badge_number = this.application.badge_number.toUpperCase();
      },
      'application.first_name'() {
        this.application.first_name = toMixedCase(this.application.first_name);
      },
      'application.last_name'() {
        this.application.last_name = this.application.last_name.toUpperCase();
      }
    }
  };
  function toMixedCase(data) {
    if (data.length !== undefined) {
      return (data.charAt(0).toUpperCase() + data.slice(1));
    } else {
      return (data);
    }
  }
</script>
<style>
  #apply-button button {
    border: red 2px solid;
    vertical-align: bottom;
  }
</style>