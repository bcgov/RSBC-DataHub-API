<template>
<form-card title="Reasonable Grounds">
    <div v-if="isProhibitionTypeSelected">
      <form-row>
        <check-field id="operating_grounds" fg_class="col-sm-12" rules="required"
                     :options='[
                         "Witnessed by officer",
                         "Admission by driver",
                         "Independent witness",
                         "Other"]'>
          The driver was operating a motor vehicle or had care and
          control of a motor vehicle for the purposes of MVA section 215(1) based on (select at least one):
        </check-field>
      </form-row>
      <form-row v-if="isOperatingGroundsOther">
        <text-field id="operating_ground_other" fg_class="col-sm-12">Other</text-field>
      </form-row>
      <form-row>
        <radio-field id="prescribed_device" fg_class="col-sm-12"
                     :options='["Yes", "No"]'>Was a prescribed test used to form reasonable grounds?
        </radio-field>
        <!-- "No, opinion formed the driver was affected by alcohol and/or drugs",
                     "No, refused by driver" -->
      </form-row>
    </div>
</form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";
import {mapGetters} from "vuex";

export default {
  name: "ReasonableGroundsCard",
  mixins: [CardsCommon],
  computed: {
    ...mapGetters(["checkBoxStatus"]),
    isProhibitionTypeSelected() {
      return this.getAttributeValue('prohibition_type').length > 0;
    },
    isOperatingGroundsOther() {
      return this.checkBoxStatus('operating_grounds', "Other");
    },
  }
}
</script>

<style scoped>

</style>