<template>
  <div id="is-served" class="card text-dark mb-2">

    <div class="card-header text-left">
      <div class="font-weight-bold">Print this page</div>
      <div class="small text-muted">Once the documents have been printed and delivered to the driver,
      mark the documents as {{ servedWording.toLowerCase() }} below.</div>

      <div class="small card mt-2" v-if="show_certificate">
          <div class="card-body">
            <service-certificate-wording
              :served_date="getServedDateString"
              :form_full_name="getOfficialFormName(getPath)"
              :certified_date="getCertifiedDateString"
              :form_id="formattedNoticeNumber(getPath)"
              :driver_name="concatenateDriverName(getPath)"
              :officer_name="getAttributeValue(getPath, 'officer_name')"
              :badge_number="getAttributeValue(getPath, 'badge_number')"
              :agency="getAttributeValue(getPath, 'agency')">
            </service-certificate-wording>
          </div>
      </div>

      <div class="text-right mt-3">
          <b-button variant="success" @click="onSuccessfulServe">{{ servedWording }}</b-button>
          <b-button class="ml-3 mr-3" variant="danger" @click="onUnsuccessfulServe">Not {{ servedWording }}</b-button>
      </div>

    </div>


  </div>
</template>

<script>

import moment from "moment-timezone";
import constants from "@/config/constants";
import ServiceCertificateWording from "@/components/print/ServiceCertificateWording";
import {mapGetters, mapActions, mapMutations} from "vuex";

export default {
  name: "PrintConfirmation",
  props: {
    form_type: {
      type: String
    },
    id: {
      type: String,
    },
    show_certificate: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      form_object: {
        "form_id": this.id,
        "form_type": this.form_type
      }
    }
  },
  computed: {
    ...mapGetters([
      'getFormData',
      "isVehicleImpounded",
      "getOfficialFormName",
      "formattedNoticeNumber",
      "concatenateDriverName",
      "isDocumentServed",
      "getAttributeValue",
      "getCurrentlyEditedForm",
      "getCurrentlyEditedFormData",
      "getCurrentlyEditedFormObject"
    ]),
    getPath() {
      return `forms/${this.form_type}/${this.id}/data`
    },
    getCertifiedDateString() {
      return moment().tz(constants.TIMEZONE).format("YYYY-MM-DD")
    },

    getServedDateString() {
      return moment().tz(constants.TIMEZONE).format("Do MMMM, YYYY")
    },
    servedWording() {
      if (this.show_certificate) {
        return "Served"
      } else {
        return "Printed"
      }
    }
  },
  components: {
    ServiceCertificateWording
  },
  methods: {
    ...mapActions(["tellApiFormIsPrinted", "saveCurrentFormToDB"]),
    ...mapMutations(["setFormAsPrinted"]),
    onSuccessfulServe() {
      const current_timestamp = moment().tz(constants.TIMEZONE).format()
      let payload = {}
      payload['form_object'] = this.form_object
      payload['variants'] = this.variants;
      payload['form_data'] = this.form_object.data;
      payload['timestamp'] = current_timestamp
      console.log("onSuccessfulServe()", payload)
      this.setFormAsPrinted(payload)
      this.saveCurrentFormToDB(this.form_object)
      this.tellApiFormIsPrinted(this.form_object)
        .then( (response) => {
            console.log("response from tellApiFormIsPrinted()", response)
        })
        .catch( (error) => {
            console.log("no response from tellApiFormIsPrinted()", error)
        })
      if(this.show_certificate) {
        this.$router.replace({
          name: 'cos', params: {"form_type": this.form_type, "id": this.id}
        })
      } else {
        this.$router.replace({name: 'Home'})
      }
    },

    onUnsuccessfulServe() {
      this.$router.replace({
          name: this.form_type, params: {
            "form_type": this.form_type,
            "id": this.id
          }
        })
    }

  }

}
</script>

<style scoped>

</style>