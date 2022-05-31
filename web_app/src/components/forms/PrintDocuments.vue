<template>
  <div>
    <div @click="onSubmit(validate, variants, form_object)" class="btn btn-primary mr-3" id="btn_print_forms">
      <slot></slot>
      <b-spinner v-if="display_spinner" small label="Loading..."></b-spinner>
    </div>
    <div class="small text-danger pt-2">
      <fade-text v-if="isNotValid" :key="rerender" show-seconds=3000>Errors in form - check for validation errors above</fade-text>
    </div>
  </div>
</template>

<script>
import moment from "moment-timezone";
import fadeText from "../FadeText";
import {mapActions, mapGetters, mapMutations} from "vuex";
import constants from "@/config/constants";

export default {
  name: "PrintDocuments",
  props: {
    form_object: {
      type: Object
    },
    validate: {},
    variants: {
      type: Array
    }
  },
  data() {
    return {
      display_spinner: false,
      isNotValid: false,
      rerender: 1
    }
  },
  computed: {
    ...mapGetters([
        "getAttributeValue",
        "getCurrentlyEditedForm",
        "getCurrentlyEditedFormData",
        "getCurrentlyEditedFormObject",
    ]),
  },
  methods: {
    ...mapActions(["tellApiFormIsPrinted", "saveCurrentFormToDB"]),
    ...mapMutations(["setFormAsPrinted"]),
    async onSubmit (validate, variantList, form_object) {
      this.display_spinner = true;
      const is_validated = await validate()
      console.log('inside onSubmit()', is_validated, variantList);
      if(is_validated) {
        const current_timestamp = moment().tz(constants.TIMEZONE).format()
        let payload = {}
        payload['form_object'] = form_object
        payload['variants'] = variantList;
        payload['form_data'] = form_object.data;
        payload['timestamp'] = current_timestamp
        this.setFormAsPrinted(payload)
        this.saveCurrentFormToDB(form_object)
        this.tellApiFormIsPrinted(form_object)
          .then( (response) => {
              console.log("response from tellApiFormIsPrinted()", response)
          })
          .catch( (error) => {
              console.log("no response from tellApiFormIsPrinted()", error)
          })
        this.display_spinner = false;
        this.$router.replace({
          name: "print", params: {
            "form_type": form_object.form_type,
            "id": form_object.form_id
          }
        })
      } else {
        this.rerender++;
        this.isNotValid = true;
      }
      this.display_spinner = false;
    }
  },
  components: {
    fadeText
  }
}
</script>