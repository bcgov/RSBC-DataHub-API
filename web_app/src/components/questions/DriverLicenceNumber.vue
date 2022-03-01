<template>
  <div v-if="visible" class="form-group">
    <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
      <label v-if="show_label" :for="id"><slot></slot>
        <span v-if="required" class="text-danger"> *</span>
      </label>
      <div class="input-group mb-3">
        <input :disabled="disabled || hasFormBeenPrinted" type=text
             class="form-control"
                :class="errors.length > 0 ? 'border-danger bg-warning' : ''"
             :id="id"
             placeholder="Driver's Licence Number"
             v-model="attribute">
        <div class="input-group-append">
          <button id="btn-bcdl-prefill" type="button" :disabled="hasFormBeenPrinted || ! isDisplayIcbcLicenceLookup" @click="triggerDriversLookup"
                  class="btn-sm btn-secondary text-white font-weight-bold">ICBC Prefill
            <b-spinner v-if="display_spinner" small label="Loading..."></b-spinner>
          </button>
          <button id="btn-dl-scan" type="button" :disabled="hasFormBeenPrinted || ! isLicenceJurisdictionBC"
                  @click="launchDlScanner" class="btn-sm btn-secondary text-white ml-2 font-weight-bold">Scan DL</button>
        </div>
      </div>
      <div class="small text-danger">{{ errors[0] }}
        <fade-text v-if="fetch_error" show-seconds=3000>{{ fetch_error }}</fade-text>
      </div>
      <b-modal id="dl-scanner" hide-footer>
        <template #modal-title>
          Driver's Licence Scanner
        </template>
        <div class="d-block text-center">
            <div v-if="scanner_opened">
              <div>Please scan the BC Driver's licence</div>
              <br />
              <b-spinner></b-spinner>

            </div>
            <div class="alert-warning pt-2 pb-2" v-if=" ! scanner_opened">
              <div>Requesting access to the scanner</div>
              <div class="small">
                {{ scanner_message }}
              </div>
            </div>
          <b-button class="mt-3 btn btn-primary" @click="$bvModal.hide('dl-scanner')">Cancel</b-button>
        </div>
      </b-modal>
    </validation-provider>
  </div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters, mapMutations, mapActions} from 'vuex';
import FadeText from "@/components/FadeText";
import dlScanner from "@/helpers/dlScanner";

export default {
  name: "DriversLicenceNumber",
  components: {FadeText},
  mixins: [FieldCommon],
  data() {
    return {
      display_spinner: false,
      fetch_error: '',
      scanner_opened: false,
      scanner_message: ''
    }
  },
  computed: {
    icbcPayload() {
      return {
        "dlNumber": this.getAttributeValue(this.id),
        "form_object": this.getCurrentlyEditedFormObject
      }
    },
    ...mapGetters([
        'getCurrentlyEditedFormObject',
      "getAttributeValue",
      "isDisplayIcbcLicenceLookup",
      "hasFormBeenPrinted",
      "isLicenceJurisdictionBC"]),
  },
  methods: {
    ...mapMutations(['updateFormField', "populateDriverFromBarCode"]),
    ...mapActions(['lookupDriverFromICBC']),
    triggerDriversLookup() {
      console.log("inside triggerDriversLookup()")
      this.fetch_error = ''
      this.display_spinner = true;
      this.lookupDriverFromICBC(this.icbcPayload)
        .then(() => {
          this.display_spinner = false;
        })
        .catch( error => {
          console.log("error", error)
          this.display_spinner = false;
          this.fetch_error = error.description;
        })
    },

    handledScannedBarCode(event) {
      const { data, device, reportId } = event;
      dlScanner.readFromScanner(device, reportId, data)
      .then( dl_data => {
        this.populateDriverFromBarCode(dl_data)
        this.$bvModal.hide('dl-scanner')
      })
    },


    async launchDlScanner() {
      console.log('inside launchDlScanner')
      this.$bvModal.show('dl-scanner')

      let scanner = await dlScanner.openScanner();

      scanner.addEventListener("inputreport", this.handledScannedBarCode);

      this.scanner_opened = !!scanner.opened;

    },

  }
}
</script>