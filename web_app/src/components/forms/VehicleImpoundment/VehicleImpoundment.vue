<template>
  <form-container title="Vehicle Impoundment" v-if="isMounted">
    <validation-observer v-slot="{handleSubmit, validate}">
      <form @submit.prevent="handleSubmit(onSubmit(validate))">
        <drivers-information-card></drivers-information-card>
        <vehicle-information-card></vehicle-information-card>
        <vehicle-owner-card></vehicle-owner-card>
        <vehicle-impoundment-card></vehicle-impoundment-card>
        <reasonable-grounds-card></reasonable-grounds-card>
        <excessive-speed-card v-if="getAttributeValue('reason_excessive_speed')"></excessive-speed-card>

        <linkage-card></linkage-card>
        <incident-details-card></incident-details-card>
        <officer-details-card></officer-details-card>
        <form-card title="Generate PDF for Printing">
          <div class="d-flex">
            <print-documents
              v-for="(document, index) in getDocumentsToPrint(name)" v-bind:key="index"
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
import OfficerDetailsCard from "@/components/forms/VehicleImpoundment/OfficerDetailsCard";
import VehicleInformationCard from "@/components/forms/VehicleImpoundment/VehicleInformationCard";
import VehicleOwnerCard from "@/components/forms/VehicleImpoundment/VehicleOwnerCard";
import VehicleImpoundmentCard from "@/components/forms/VehicleImpoundment/VehicleImpoundmentCard";
import ReasonableGroundsCard from "@/components/forms/VehicleImpoundment/ReasonableGroundsCard";
import ExcessiveSpeedCard from "@/components/forms/VehicleImpoundment/ExcessiveSpeedCard";
import LinkageCard from "@/components/forms/VehicleImpoundment/LinkageCard";
import IncidentDetailsCard from "@/components/forms/VehicleImpoundment/IncidentDetailsCard";

export default {
  name: "VehicleImpoundment",
  components: {
    IncidentDetailsCard,
    LinkageCard,
    ExcessiveSpeedCard,
    ReasonableGroundsCard,
    VehicleImpoundmentCard,
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
        "getCurrentlyEditedFormData",
        "getCurrentlyEditedFormObject",
        "corporateOwner",
        "getPdfFileNameString",
        "getPagesToPrint"
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