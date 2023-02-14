<template>
  <form-container title="Vehicle Impoundment" :form_object="formObject" v-if="isMounted">
    <validation-observer v-slot="{handleSubmit, validate}">
      <form @submit.prevent="handleSubmit(onSubmit(validate))">
        <drivers-information-card :path="getPath"></drivers-information-card>
        <vehicle-information-card :path="getPath"></vehicle-information-card>
        <vehicle-owner-card :path="getPath"></vehicle-owner-card>
        <time-and-place-card :path="getPath"></time-and-place-card>
        <impoundment-lot-card :path="getPath"></impoundment-lot-card>
        <immediate-roadside-prohibition :path="getPath"></immediate-roadside-prohibition>
        <seven-day-impound-card :path="getPath"></seven-day-impound-card>
        <excessive-speed-card
            :path="getPath + '/reason_excessive_speed_true'"
            v-if="getAttributeValue(getPath, 'reason_excessive_speed_true')">
        </excessive-speed-card>
        <linkage-card :path="getPath"></linkage-card>
        <incident-details-card :path="getPath"></incident-details-card>
        <officer-details-card :path="getPath"></officer-details-card>
        <form-card title="Generate PDF for Printing">
          <div class="d-flex">
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
  import {mapGetters} from 'vuex';
  import PrintDocuments from "../PrintDocuments";
  import DriversInformationCard from "@/components/forms/VehicleImpoundment/DriversInformationCard";
  import OfficerDetailsCard from "@/components/forms/OfficerDetailsCard";
  import VehicleInformationCard from "@/components/forms/VehicleImpoundment/VehicleInformationCard";
  import VehicleOwnerCard from "@/components/forms/VehicleImpoundment/VehicleOwnerCard";
  import TimeAndPlaceCard from "@/components/forms/VehicleImpoundment/TimeAndPlaceCard";
  import ImpoundmentLotCard from "@/components/forms/VehicleImpoundment/ImpoundmentLotCard";
  import SevenDayImpoundCard from "@/components/forms/VehicleImpoundment/SevenDayImpoundCard";
  import ExcessiveSpeedCard from "@/components/forms/VehicleImpoundment/ExcessiveSpeedCard";
  import LinkageCard from "@/components/forms/VehicleImpoundment/LinkageCard";
  import IncidentDetailsCard from "@/components/forms/VehicleImpoundment/IncidentDetailsCard";
  import ImmediateRoadsideProhibition from "@/components/forms/VehicleImpoundment/ImmediateRoadsideProhibition";
  export default {
    name: "VehicleImpoundment",
    components: {
      ImmediateRoadsideProhibition,
      IncidentDetailsCard,
      LinkageCard,
      ExcessiveSpeedCard,
      ImpoundmentLotCard,
      TimeAndPlaceCard,
      SevenDayImpoundCard,
      DriversInformationCard,
      OfficerDetailsCard,
      VehicleInformationCard,
      VehicleOwnerCard,
      PrintDocuments
    },
    mixins: [FormsCommon],
    props: {
      name: {
        type: String,
        default: 'VI'
      }
    },
    data() {
      return {
        isNotValid: false,
        rerender: 1
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
          "getDocumentsToPrint",
          "getAttributeValue",
          "getCurrentlyEditedForm",
          "getCurrentlyEditedFormData",
          "getCurrentlyEditedFormObject",
          "getPdfFileNameString",
      ]),
    }
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