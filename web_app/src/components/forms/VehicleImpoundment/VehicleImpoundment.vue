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
          <div class="d-flex justify-content-between">
            <button type="submit" class="btn btn-primary" id="btn_print_forms">Print Notice and Report
              <b-spinner v-if="display_spinner" small label="Loading..."></b-spinner>
            </button>
          </div>
          <div class="small text-danger pt-2">
            <fade-text v-if="isNotValid" :key="rerender" show-seconds=3000>Errors in form - check for validation errors above</fade-text>
          </div>
        </form-card>
      </form>
    </validation-observer>
  </form-container>
</template>

<script>

import FormsCommon from "@/components/forms/FormsCommon";
import {mapActions, mapGetters, mapMutations} from 'vuex';

import DriversInformationCard from "@/components/forms/VehicleImpoundment/DriversInformationCard";
import FadeText from "@/components/FadeText";
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
    FadeText,
    OfficerDetailsCard,
    VehicleInformationCard,
    VehicleOwnerCard,
  },
  mixins: [FormsCommon],
  computed: {
    ...mapGetters([
        "getAttributeValue",
        "getCurrentlyEditedFormData",
        "getCurrentlyEditedFormObject",
        "corporateOwner",
    ]),
  },
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
  methods: {
    ...mapMutations(["setFormAsPrinted"]),
    ...mapActions(["saveFormAndGeneratePDF"]),
    async onSubmit (validate) {
      this.display_spinner = true;
      const is_validated = await validate()
      console.log('inside onSubmit()', is_validated);
      if(is_validated) {
        await this.saveFormAndGeneratePDF(this.getFormObject)
          .then( (response) => {
              console.log('form generated successfully', response)
              this.display_spinner = false;
            })
          .catch((error) => {
              console.log('form did not generate successfully', error)
              this.display_spinner = false;
            })
      } else {
        this.rerender++;
        this.isNotValid = true;
      }
      this.display_spinner = false;
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