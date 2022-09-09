<template>
  <div id="print-row" class="row">
    <div @click="onSubmit(validate, variants, form_object)" class="btn btn-primary mr-3" id="btn_print_forms">
      <slot></slot>
      <b-spinner v-if="display_spinner" small label="Loading..."></b-spinner>
    </div>
    <div class="small text-danger pt-2">
      <fade-text v-if="isNotValid" :key="rerender" show-seconds=3000>Errors in form - check for validation errors above</fade-text>
    </div>
    <router-link v-if="isDocumentServed(path) && show_certificate" :to="{ name: 'cos', params: { id: form_object.form_id, form_type: form_object.form_type}}" target="_blank">
      <div class="btn btn-primary">Print Certificate of Service</div>
    </router-link>
  </div>
</template>

<script>
import fadeText from "../FadeText";
import {mapGetters} from "vuex";

export default {
  name: "PrintDocuments",
  props: {
    show_certificate: {
      type: Boolean,
      default: false
    },
    path: {
      type: String,
      default: ''
    },
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
        "getOfficialFormName",
        "formattedNoticeNumber",
        "concatenateDriverName",
        "isDocumentServed",
        "getAttributeValue",
        "getCurrentlyEditedForm",
        "getCurrentlyEditedFormData",
        "getCurrentlyEditedFormObject",
    ]),
  },
  methods: {
    async onSubmit (validate) {
      this.display_spinner = true;
      const is_validated = await validate()
      console.log('inside onSubmit()', is_validated);
      if(is_validated) {
        this.display_spinner = false;
        this.$router.replace({
          name: "print", params: {
            "form_type": this.form_object.form_type,
            "id": this.form_object.form_id
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
    fadeText,
  }
}
</script>

<style scoped>

  #print-row {

    margin: 0 0 0 0;
    padding: 0 0 0 0;
  }

</style>
