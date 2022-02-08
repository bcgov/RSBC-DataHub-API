<template>
<form-card title="Test Administered - Alcohol 215(2)">
    <shadow-box>
      <form-row>
        <check-field :show_label="false"  id="test_administered_asd" fg_class="col-sm-6"
                     :options='["Alco-Sensor FST (ASD)"]'>Test Administered</check-field>
        <date-field v-if="isTestAdministeredASD" id="asd_expiry_date" fg_class="col-sm-6" rules="notExpired">ASD expiry date</date-field>
      </form-row>
      <form-row>
        <radio-field v-if="isTestAdministeredASD" id="result_alcohol" fg_class="col-sm-6"
                     :options='["51-99 mg%", "Over 99 mg%"]'>Result</radio-field>
        <date-time v-if="isTestAdministeredASD" id="time_of_test"
                   rules="required"
                   fg_class="col-sm-6">Time of test</date-time>
      </form-row>
    </shadow-box>
    <shadow-box>
      <form-row>
        <check-field :show_label="false"  id="test_administered_instrument" fg_class="col-sm-6"
                     :options='["Approved Instrument"]'></check-field>
      </form-row>
      <form-row>
        <check-field v-if="isTestAdministeredApprovedInstrument" id="result_alcohol_approved_instrument" fg_class="col-sm-6"
                     :options='["BAC"]'>Result</check-field>
        <date-time v-if="isTestAdministeredApprovedInstrument" id="time_of_test"
                   rules="required"
                   fg_class="col-sm-6">Time of test</date-time>
      </form-row>
      <form-row>
        <text-field v-if="isTestAdministeredApprovedInstrument" id="test_result_bac" fg_class="col-sm-12">Result</text-field>
      </form-row>
    </shadow-box>
    <shadow-box>
      <form-row>
        <check-field :show_label="false" id="test_administered_sfst" fg_class="col-sm-6"
                     :options='["Prescribed Physical Coordination Test (SFST)"]'>&nbsp;
        </check-field>
        <date-time v-if="isTestAdministeredSFST"
                   id="time_of_test"
                   rules="required"
                   fg_class="col-sm-6">Time of test</date-time>
      </form-row>
    </shadow-box>
</form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";
import {mapGetters} from "vuex";

export default {
  name: "OfficersReport",
  mixins: [CardsCommon],
  computed: {
    ...mapGetters(["isTestAdministeredSFST", "isTestAdministeredApprovedInstrument", "isTestAdministeredASD"])
  }
}
</script>

<style scoped>

</style>