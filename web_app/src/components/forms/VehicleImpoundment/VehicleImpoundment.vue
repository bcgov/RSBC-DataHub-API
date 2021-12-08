<template>
  <form-container title="Vehicle Impoundment" v-if="isMounted">
    <validation-observer v-slot="{handleSubmit, invalid}">
      <form @submit.prevent="handleSubmit(onSubmit(invalid))">
        <drivers-information-card></drivers-information-card>
        <vehicle-information-card></vehicle-information-card>
        <vehicle-owner-card></vehicle-owner-card>
        <vehicle-impoundment-card></vehicle-impoundment-card>
        <reasonable-grounds-card></reasonable-grounds-card>
        <officer-details-card></officer-details-card>
        <form-card title="Generate PDF for Printing">
          <div class="d-flex justify-content-between">
            <button type="submit" class="btn btn-primary" :disabled="invalid">PDF
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
import {mapActions, mapGetters, mapMutations} from 'vuex';

import DriversInformationCard from "@/components/forms/VehicleImpoundment/DriversInformationCard";
import FadeText from "@/components/FadeText";
import OfficerDetailsCard from "@/components/forms/VehicleImpoundment/OfficerDetailsCard";
import VehicleInformationCard from "@/components/forms/VehicleImpoundment/VehicleInformationCard";
import VehicleOwnerCard from "@/components/forms/VehicleImpoundment/VehicleOwnerCard";
import VehicleImpoundmentCard from "@/components/forms/VehicleImpoundment/VehicleImpoundmentCard";
import ReasonableGroundsCard from "@/components/forms/VehicleImpoundment/ReasonableGroundsCard";


export default {
  name: "VehicleImpoundment",
  components: {
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
        "corporateOwner"
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