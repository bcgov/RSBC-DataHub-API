<template>
<form-card title="Reasonable Grounds">
    <div v-if="doesAttributeExist(this.path, 'prohibition_type_drugs') || doesAttributeExist(this.path, 'prohibition_type_alcohol')" >
      <form-row>
        <check-field id="operating_grounds" :path="path" fg_class="col-sm-12" rules="required"
                     :options='[
                         ["officer", "Witnessed by officer"],
                         ["admission", "Admission by driver"],
                         ["witness", "Independent witness"],
                         ["video", "Video surveillance"],
                         ["other", "Other"]]'>
          The driver was operating a motor vehicle or had care and
          control of a motor vehicle for the purposes of MVA section 215(1) based on (select at least one):
        </check-field>
      </form-row>
      <form-row v-if="doesAttributeExist(path, 'operating_grounds_other')">
        <text-field id="operating_ground_other" :path="path + '/operating_grounds_other'" fg_class="col-sm-12">Other</text-field>
      </form-row>
      <form-row>
        <radio-field id="prescribed_device" :path="path" fg_class="col-sm-12"
                     :options='[["yes", "Yes"], ["no", "No"]]'>Was a prescribed test used to form reasonable grounds?
        </radio-field>
      </form-row>
      <form-row>
        <radio-description v-if="doesAttributeExist(this.path, 'prescribed_device_no')"
                     id="reason_prescribed_test_not_used"
                     :path="path  + '/prescribed_device_no'" fg_class="col-sm-12"
                     :options='[
                       ["refused", "Refused by driver"],
                       ["opinion", "Opinion formed the driver was affected by alcohol and/or drugs"]
                     ]'>
          Why was a prescribed test not used?
        </radio-description>
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
  }
}
</script>

<style scoped>

</style>