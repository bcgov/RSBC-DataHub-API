<template>
  <div v-if="visible" class="form-group" :class="fg_class">
    <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
      <label v-if="show_label" :for="id"><slot></slot>
        <span v-if="required" class="text-danger"> *</span>
      </label>
      <div class="input-group mb-3">
        <input type=text
             class="form-control"
             :id="id"
             placeholder="Plate"
             :value="getAttributeValue(id)"
             @input="updateFormField">
        <div class="input-group-append">
          <button type="button" @click="triggerPlateLookup" class="btn-sm btn-secondary font-weight-bold" id="icbc-prefill"
                  :disabled="! isDisplayIcbcPlateLookup">
            ICBC Prefill
            <b-spinner v-if="display_spinner" small label="Loading..."></b-spinner>
          </button>
        </div>
      </div>
      <div class="small text-danger">
        {{ errors[0] }}
        <fade-text v-if="fetch_error" :show-seconds=3000>{{ fetch_error }}</fade-text>
      </div>
    </validation-provider>
  </div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters, mapMutations, mapActions} from "vuex";
import FadeText from "@/components/FadeText";

export default {
  name: "PlateNumber",
  mixins: [FieldCommon],
  data() {
    return {
      display_spinner: false,
      fetch_error: ''
    }
  },
  computed: {
    ...mapGetters(["getAttributeValue", "isDisplayIcbcPlateLookup", "getCurrentlyEditedFormId"]),
    icbcPayload() {
      return {
        "plateNumber": this.getAttributeValue(this.id)
      }
    },
  },
  methods: {
    ...mapMutations(["updateFormField"]),
    ...mapActions(["lookupPlateFromICBC"]),
    triggerPlateLookup() {
      console.log("inside triggerPlateLookup()")
      this.fetch_error = ''
      this.display_spinner = true;
      this.lookupPlateFromICBC(this.icbcPayload)
          .then( () => {
            this.display_spinner = false
          })
          .catch( error => {
            console.log("error", error)
            this.display_spinner = false
            this.fetch_error = error.description;
          })
    }
  },
  components: {
    FadeText
  }
}
</script>

<style scoped>

</style>