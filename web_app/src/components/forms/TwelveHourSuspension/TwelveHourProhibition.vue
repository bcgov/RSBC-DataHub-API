<template>
  <form-container title="Notice of 12 Hour Licence Suspension" v-if="isMounted">
    <validation-observer v-slot="{handleSubmit, invalid}">
      <form @submit.prevent="handleSubmit(onSubmit(invalid))">
        <drivers-information-card></drivers-information-card>
        <vehicle-information-card></vehicle-information-card>
        <return-of-licence-card></return-of-licence-card>
        <vehicle-impoundment-card></vehicle-impoundment-card>
        <prohibition-information-card></prohibition-information-card>
        <officer-details-card></officer-details-card>
        <form-card title="Generate PDF for Printing">
          <div class="d-flex justify-content-between">
            <button type="submit" class="btn btn-primary" :disabled="invalid" id="btn_print_forms">Print Forms
              <b-spinner v-if="display_spinner" small label="Loading..."></b-spinner>
            </button>
          </div>
          <div class="small text-danger pt-2">
            <fade-text v-if="isNotValid" :key="rerender" show-seconds=3000>Errors in form - check above</fade-text>
          </div>
        </form-card>
      </form>
    </validation-observer>
  </form-container>
</template>

<script>

import FormsCommon from "@/components/forms/FormsCommon";
import DriversInformationCard from "@/components/forms/TwelveHourSuspension/DriversInformationCard";
import ReturnOfLicenceCard from "@/components/forms/ReturnOfLicenceCard";
import OfficerDetailsCard from "@/components/forms/OfficerDetailsCard";
import VehicleInformationCard from "@/components/forms/TwelveHourSuspension/VehicleInformationCard";
import ProhibitionInformationCard from "@/components/forms/TwelveHourSuspension/ProhibitionInformationCard";
import VehicleImpoundmentCard from "@/components/forms/TwelveHourSuspension/VehicleImpoundmentCard";
import {mapActions, mapGetters, mapMutations} from "vuex";
import FadeText from "@/components/FadeText";

export default {
  name: "TwelveTwentyFour",
  mixins: [FormsCommon],
  components: {
    FadeText,
    ProhibitionInformationCard,
    DriversInformationCard,
    OfficerDetailsCard,
    ReturnOfLicenceCard,
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
    ...mapGetters(["getCurrentlyEditedFormObject", "getPdfFileNameString"]),
  },
  methods: {
    ...mapMutations(["setFormAsPrinted"]),
    ...mapActions(["saveFormAndGeneratePDF"]),
    async onSubmit (invalid) {
      console.log('inside onSubmit()', invalid);
      if(! invalid) {
        this.display_spinner = true;
        await this.saveFormAndGeneratePDF(this.getFormObject)
            .then(() => {
              this.display_spinner = false;
            })
            .catch(() => {
              this.display_spinner = false;
              this.rerender++;
              this.isNotValid = true;
            })
      }
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