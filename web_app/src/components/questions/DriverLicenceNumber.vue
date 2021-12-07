<template>
  <div v-if="visible" class="form-group">
    <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
      <label v-if="show_label" :for="id"><slot></slot>
        <span v-if="required" class="text-danger"> *</span>
      </label>
      <div class="input-group mb-3">
        <input :disabled="disabled" type=text
             class="form-control"
             :id="id"
             placeholder="Driver's Licence Number"
             v-model="attribute">
        <div class="input-group-append">
          <button type="button" :disabled="! isDisplayIcbcLicenceLookup" @click="triggerDriversLookup"
                  class="btn-sm btn-secondary text-white font-weight-bold">Driver's Lookup
            <b-spinner v-if="display_spinner" small label="Loading..."></b-spinner>
          </button>
          <button type="button" :disabled=true class="btn-sm btn-secondary text-white ml-2 font-weight-bold">Scan DL</button>
        </div>
      </div>
      <div class="small text-danger">{{ errors[0] }}
        <fade-text v-if="fetch_error" show-seconds=3000>{{ fetch_error }}</fade-text>
      </div>
    </validation-provider>
  </div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters, mapMutations, mapActions} from 'vuex';
import FadeText from "@/components/FadeText";

export default {
  name: "DriversLicenceNumber",
  components: {FadeText},
  mixins: [FieldCommon],
  data() {
    return {
      display_spinner: false,
      fetch_error: ''
    }
  },
  computed: {
    icbcPayload() {
      return {
        "dlNumber": this.getAttributeValue(this.id),
        "form_object": this.getCurrentlyEditedFormObject
      }
    },
    ...mapGetters(['getCurrentlyEditedFormObject', "getAttributeValue", "isDisplayIcbcLicenceLookup"]),
  },
  methods: {
    ...mapMutations(['updateFormField']),
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
    }
  }
}
</script>