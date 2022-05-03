<template>
  <form-container title="Notice of 24 Hour Licence Prohibition" v-if="isMounted">
    <validation-observer v-slot="{handleSubmit, validate}">
      <form @submit.prevent="handleSubmit(onSubmit(validate))">
        <drivers-information-card></drivers-information-card>
        <vehicle-information-card></vehicle-information-card>
        <vehicle-owner-card></vehicle-owner-card>
        <vehicle-impoundment-card></vehicle-impoundment-card>
        <return-of-licence-card></return-of-licence-card>
        <prohibition-information-card></prohibition-information-card>
        <reasonable-grounds-card></reasonable-grounds-card>
        <test-administered-alcohol-card v-if="isPrescribedTestUsed && isProhibitionTypeAlcohol"></test-administered-alcohol-card>
        <test-administered-drugs-card v-if="isPrescribedTestUsed && isProhibitionTypeDrugs"></test-administered-drugs-card>
        <officer-details-card></officer-details-card>
        <form-card title="Generate PDF for Printing">
          <div class="d-flex justify-content-between">
            <button type="submit" class="btn btn-primary" id="btn_print_forms">Print Forms
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

import DriversInformationCard from "@/components/forms/TwentyFourHourProhibition/DriversInformationCard";
import FadeText from "@/components/FadeText";
import OfficerDetailsCard from "@/components/forms/OfficerDetailsCard";
import ProhibitionInformationCard from "@/components/forms/TwentyFourHourProhibition/ProhibitionInformationCard";
import ReasonableGroundsCard from "@/components/forms/TwentyFourHourProhibition/ReasonableGroundsCard";
import ReturnOfLicenceCard from "@/components/forms/ReturnOfLicenceCard";
import TestAdministeredAlcoholCard from "@/components/forms/TwentyFourHourProhibition/TestAdministeredAlcoholCard";
import TestAdministeredDrugsCard from "@/components/forms/TwentyFourHourProhibition/TestAdministeredDrugsCard";
import VehicleImpoundmentCard from "@/components/forms/TwentyFourHourProhibition/VehicleImpoundmentCard";
import VehicleInformationCard from "@/components/forms/TwentyFourHourProhibition/VehicleInformationCard";
import VehicleOwnerCard from "@/components/forms/TwentyFourHourProhibition/VehicleOwnerCard";


export default {
  name: "TwentyFourHourProhibition",
  components: {
    DriversInformationCard,
    FadeText,
    OfficerDetailsCard,
    ProhibitionInformationCard,
    ReasonableGroundsCard,
    ReturnOfLicenceCard,
    TestAdministeredAlcoholCard,
    TestAdministeredDrugsCard,
    VehicleImpoundmentCard,
    VehicleInformationCard,
    VehicleOwnerCard,
  },
  mixins: [FormsCommon],
  computed: {
    ...mapGetters([
        "getAttributeValue",
        "getCurrentlyEditedFormData",
        "getCurrentlyEditedFormObject",
        "corporateOwner"]),
    isProhibitionTypeDrugs() {
      return this.getAttributeValue('prohibition_type') === "Drugs 215(3)";
    },
    isProhibitionTypeAlcohol() {
      return this.getAttributeValue('prohibition_type') === "Alcohol 215(2)";
    },
    isPrescribedTestUsed() {
      return this.getAttributeValue('prescribed_device').substr(0,3) === "Yes";
    }
  },
  props: {
    name: {
      type: String,
      default: '24Hour'
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