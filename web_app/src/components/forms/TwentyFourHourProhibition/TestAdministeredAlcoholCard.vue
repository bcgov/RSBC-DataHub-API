<template>
<form-card title="Test Administered - Alcohol 215(2)">
    <shadow-box>
      <form-row>
        <check-field :show_label="false"  id="test_administered_asd" fg_class="col-sm-6"
                     :options='["Alco-Sensor FST (ASD)"]'>Test Administered</check-field>
        <date-field v-if="isTestAdministeredASD" id="asd_expiry_date" fg_class="col-sm-6" rules="required|validDt|notExpiredDt">ASD expiry date</date-field>
      </form-row>
      <form-row>
        <radio-field v-if="isTestAdministeredASD" id="result_alcohol" fg_class="col-sm-6"
                     :options='["51-99 mg%", "Over 99 mg%"]'>Result</radio-field>
        <date-field id="test_date" fg_class="col-sm-3" :visible="isTestAdministeredASD"
                  rules="required|validDt|notFutureDt|notGtYearAgo">Date of test</date-field>
        <time-field id="test_time" fg_class="col-sm-3" :visible="isTestAdministeredASD"
                    rules="required|validTime|notFutureDateTime:@test_date|notBeforeCareDateTime:@prohibition_start_date,@prohibition_start_time,@test_date">Time</time-field>
      </form-row>
    </shadow-box>
    <shadow-box>
      <form-row>
        <check-field :show_label="false"  id="test_administered_instrument" fg_class="col-sm-6"
                     :options='["Approved Instrument"]'></check-field>
      </form-row>
      <form-row>
        <text-field rules="required|bac_result"
                    v-if="isTestAdministeredApprovedInstrument"
                    id="test_result_bac"
                    fg_class="col-sm-2">BAC Result (mg%)
        </text-field>
        <date-field id="test_date" fg_class="col-sm-3" :visible="isTestAdministeredApprovedInstrument"
                  rules="required|validDt|notFutureDt|notGtYearAgo">Date of test</date-field>
        <time-field id="test_time" fg_class="col-sm-3" :visible="isTestAdministeredApprovedInstrument"
                    rules="required|validTime|notFutureDateTime:@test_date|notBeforeCareDateTime:@prohibition_start_date,@prohibition_start_time,@test_date">Time</time-field>
      </form-row>
    </shadow-box>
    <shadow-box>
      <form-row>
        <check-field :show_label="false" id="test_administered_sfst" fg_class="col-sm-6"
                     :options='["Prescribed Physical Coordination Test (SFST)"]'>&nbsp;
        </check-field>
        <date-field id="test_date" fg_class="col-sm-3" :visible="isTestAdministeredSFST"
                  rules="required|validDt|notFutureDt|notGtYearAgo">Date of test</date-field>
        <time-field id="test_time" fg_class="col-sm-3" :visible="isTestAdministeredSFST"
                    rules="required|validTime|notFutureDateTime:@test_date|notBeforeCareDateTime:@prohibition_start_date,@prohibition_start_time,@test_date">Time</time-field>
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