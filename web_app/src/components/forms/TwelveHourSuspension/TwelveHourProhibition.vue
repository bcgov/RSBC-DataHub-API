<template>
  <form-container title="Notice of 12 Hour Licence Suspension" :form_object="formObject" v-if="isMounted">
    <validation-observer v-slot="{handleSubmit, validate}">
      <form @submit.prevent="handleSubmit(onSubmit(validate))">
        <drivers-information-card :path="getPath"></drivers-information-card>
        <vehicle-information-card :path="getPath"></vehicle-information-card>
<!--        <return-of-licence-card :path="getPath"></return-of-licence-card>-->
        <vehicle-impoundment-card :path="getPath"></vehicle-impoundment-card>
        <prohibition-information-card :path="getPath"></prohibition-information-card>
        <officer-details-card :path="getPath"></officer-details-card>
        <form-card title="Generate PDF for Printing">
          <div class="d-flex justify-content-between">
            <print-documents
              v-for="(document, index) in getDocumentsToPrint(name)" v-bind:key="index"
              :form_object="getCurrentlyEditedForm"
              :validate="validate"
              :variants="document.variants">
              {{ document.name }}
            </print-documents>
          </div>
        </form-card>
      </form>
    </validation-observer>
  </form-container>
</template>

<script>

import FormsCommon from "@/components/forms/FormsCommon";
import DriversInformationCard from "@/components/forms/TwelveHourSuspension/DriversInformationCard";
import OfficerDetailsCard from "@/components/forms/OfficerDetailsCard";
import VehicleInformationCard from "@/components/forms/TwelveHourSuspension/VehicleInformationCard";
import PrintDocuments from "../PrintDocuments";
import ProhibitionInformationCard from "@/components/forms/TwelveHourSuspension/ProhibitionInformationCard";
import VehicleImpoundmentCard from "@/components/forms/TwelveHourSuspension/VehicleImpoundmentCard";
import {mapGetters} from "vuex";

export default {
  name: "TwelveTwentyFour",
  mixins: [FormsCommon],
  components: {
    PrintDocuments,
    ProhibitionInformationCard,
    DriversInformationCard,
    OfficerDetailsCard,
    VehicleInformationCard,
    VehicleImpoundmentCard,
  },
  props: {
    name: {
      type: String,
      default: '12Hour'
    }
  },

  mounted() {
    let payload = {form_type: this.name, form_id: this.id}
    this.editExistingForm(payload)
    this.setNewFormDefaults(payload)
    this.data = this.getCurrentlyEditedFormData
    this.isMounted = true
  },
  computed: {
    ...mapGetters([
      "getCurrentlyEditedFormObject",
      "getDocumentsToPrint",
      "getPdfFileNameString",
      "getCurrentlyEditedForm"]),
  },
}
</script>

<style scoped>
  .lightgray {
    background-color: lightgray;
  }
  .prohibition_number {
    color: red;
  }
</style>