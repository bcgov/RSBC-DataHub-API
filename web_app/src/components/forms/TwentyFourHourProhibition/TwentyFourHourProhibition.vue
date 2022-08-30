<template>
  <form-container title="Notice of 24 Hour Licence Prohibition" :form_object="formObject" v-if="isMounted">
    <validation-observer v-slot="{handleSubmit, validate}">
      <form @submit.prevent="handleSubmit(onSubmit(validate))">
        <drivers-information-card :path="getPath"></drivers-information-card>
        <vehicle-information-card :path="getPath"></vehicle-information-card>
        <vehicle-owner-card :path="getPath"></vehicle-owner-card>
        <vehicle-impoundment-card :path="getPath"></vehicle-impoundment-card>
        <return-of-licence-card :path="getPath"></return-of-licence-card>
        <prohibition-information-card :path="getPath"></prohibition-information-card>
        <reasonable-grounds-card :path="getPath"></reasonable-grounds-card>
        <test-administered-alcohol-card :path="getPath + '/prohibition_type_alcohol'"
                                        v-if="doesAttributeExist(getPath, 'prohibition_type_alcohol')
                                        && doesAttributeExist(getPath, 'prescribed_device_yes')">

        </test-administered-alcohol-card>
        <test-administered-drugs-card :path="getPath + '/prohibition_type_drugs'"
                                      v-if="doesAttributeExist(getPath, 'prohibition_type_drugs')
                                        && doesAttributeExist(getPath, 'prescribed_device_yes')">
        </test-administered-drugs-card>
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
import DriversInformationCard from "@/components/forms/TwentyFourHourProhibition/DriversInformationCard";
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
    OfficerDetailsCard,
    PrintDocuments,
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
        "getDocumentsToPrint",
        "getAttributeValue",
        "getCurrentlyEditedFormData",
        "getCurrentlyEditedFormObject",
        "getCurrentlyEditedForm",
        "doesAttributeExist"]),

    isPrescribedTestUsed() {
      return this.getAttributeValue(this.getPath, 'prescribed_device') === "Yes";
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