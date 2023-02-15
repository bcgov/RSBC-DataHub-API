<template>
  <form-container v-if="isMounted" title="Vehicle Impoundment" :form_object="formObject">
    <validation-observer v-slot="{ handleSubmit, validate }">
      <form @submit.prevent="handleSubmit(onSubmit(validate))">
        <drivers-information-card :path="getPath"></drivers-information-card>
        <vehicle-information-card :path="getPath"></vehicle-information-card>
        <vehicle-owner-card :path="getPath"></vehicle-owner-card>
        <time-and-place-card :path="getPath"></time-and-place-card>
        <impoundment-lot-card :path="getPath"></impoundment-lot-card>
        <immediate-roadside-prohibition :path="getPath"></immediate-roadside-prohibition>
        <seven-day-impound-card :path="getPath"></seven-day-impound-card>
        <excessive-speed-card v-if="getAttributeValue(getPath, 'reason_excessive_speed_true')" :path="getPath + '/reason_excessive_speed_true'"></excessive-speed-card>
        <unlicensed-driver-card v-if="getAttributeValue(getPath, 'reason_unlicensed_true')" :path="getPath + '/reason_unlicensed_true'"></unlicensed-driver-card>
        <linkage-card :path="getPath"></linkage-card>
        <incident-details-card :path="getPath"></incident-details-card>
        <officer-details-card :path="getPath"></officer-details-card>
        <form-card title="Generate Document for Printing">
          <div class="d-flex">
            <print-documents v-for="(document, index) in getDocumentsToPrint(name)" v-bind:key="index" :form_object="getCurrentlyEditedForm" :validate="validate" :variants="document.variants">
              {{ document.name }}
            </print-documents>
          </div>
        </form-card>
      </form>
    </validation-observer>
  </form-container>
</template>
<script>
  import DriversInformationCard from "@/components/forms/VehicleImpoundment/DriversInformationCard";
  import ExcessiveSpeedCard from "@/components/forms/VehicleImpoundment/ExcessiveSpeedCard";
  import FormsCommon from "@/components/forms/FormsCommon";
  import ImmediateRoadsideProhibition from "@/components/forms/VehicleImpoundment/ImmediateRoadsideProhibition";
  import ImpoundmentLotCard from "@/components/forms/VehicleImpoundment/ImpoundmentLotCard";
  import IncidentDetailsCard from "@/components/forms/VehicleImpoundment/IncidentDetailsCard";
  import LinkageCard from "@/components/forms/VehicleImpoundment/LinkageCard";
  import OfficerDetailsCard from "@/components/forms/OfficerDetailsCard";
  import PrintDocuments from "../PrintDocuments";
  import SevenDayImpoundCard from "@/components/forms/VehicleImpoundment/SevenDayImpoundCard";
  import TimeAndPlaceCard from "@/components/forms/VehicleImpoundment/TimeAndPlaceCard";
  import UnlicensedDriverCard from "@/components/forms/VehicleImpoundment/UnlicensedDriverCard";
  import VehicleInformationCard from "@/components/forms/VehicleImpoundment/VehicleInformationCard";
  import VehicleOwnerCard from "@/components/forms/VehicleImpoundment/VehicleOwnerCard";
  import { mapGetters } from 'vuex';
  export default {
    name: "VehicleImpoundment",
    components: {
      DriversInformationCard,
      ExcessiveSpeedCard,
      ImmediateRoadsideProhibition,
      ImpoundmentLotCard,
      IncidentDetailsCard,
      LinkageCard,
      OfficerDetailsCard,
      PrintDocuments,
      SevenDayImpoundCard,
      TimeAndPlaceCard,
      UnlicensedDriverCard,
      VehicleInformationCard,
      VehicleOwnerCard
    },
    computed: {
      ...mapGetters([
        "getAttributeValue",
        "getCurrentlyEditedForm",
        "getCurrentlyEditedFormData",
        "getCurrentlyEditedFormObject",
        "getDocumentsToPrint",
        "getPdfFileNameString"
      ])
    },
    data() {
      return {
        isNotValid: false,
        rerender: 1
      }
    },
    mixins: [ FormsCommon ],
    mounted() {
      let payload = {
          form_type: this.name,
          form_id: this.id
      };
      this.editExistingForm(payload);
      this.setNewFormDefaults(payload);
      this.data = this.getCurrentlyEditedFormData;
      this.isMounted = true;
    },
    props: {
      name: {
        type: String,
        default: 'VI'
      }
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