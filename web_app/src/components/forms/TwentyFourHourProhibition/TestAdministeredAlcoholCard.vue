<template>
<form-card title="Test Administered - Alcohol 215(2)">
    <shadow-box>
      <form-row>
        <in-line-check-box id="test_administered_asd" :path="path" fg_class="col-sm-6"
                     :option='true'>Alco-Sensor FST (ASD)</in-line-check-box>
        <date-field v-if="doesAttributeExist(path, 'test_administered_asd_true')"
                    id="asd_expiry_date"
                    :path="path + '/test_administered_asd_true'"
                    fg_class="col-sm-6"
                    rules="required|validDt|notExpiredDt">ASD expiry date</date-field>
      </form-row>
      <form-row v-if="doesAttributeExist(path, 'test_administered_asd_true')">
        <radio-field id="result_alcohol"
                     :path="path + '/test_administered_asd_true'" fg_class="col-sm-6"
                     :options='[["under","51-99 mg%"], ["over","Over 99 mg%"]]'>Result</radio-field>

        <date-field id="test_date"
                    :path="path" fg_class="col-sm-3"
                  rules="required|validDt|notFutureDt|notGtYearAgo">Date of test</date-field>
        <time-field id="test_time"
                    :path="path" fg_class="col-sm-3"
                    rules="required|validTime|notFutureDateTime:@test_date|notBeforeCareDateTime:@prohibition_start_date,@prohibition_start_time,@test_date">Time</time-field>
      </form-row>
    </shadow-box>
    <shadow-box>
      <form-row>
        <in-line-check-box id="test_administered_instrument" :path="path" fg_class="col-sm-6"
                     :option='true'>Approved Instrument</in-line-check-box>
      </form-row>
      <form-row v-if="doesAttributeExist(path, 'test_administered_instrument_true')">
        <text-field rules="required|bac_result"
                    id="test_result_bac" :path="path + '/test_administered_instrument_true'"
                    fg_class="col-sm-2">BAC Result (mg%)
        </text-field>
        <date-field id="test_date" :path="path" fg_class="col-sm-3"
                  rules="required|validDt|notFutureDt|notGtYearAgo">Date of test</date-field>
        <time-field id="test_time" :path="path" fg_class="col-sm-3"
                    rules="required|validTime|notFutureDateTime:@test_date|notBeforeCareDateTime:@prohibition_start_date,@prohibition_start_time,@test_date">Time</time-field>
      </form-row>
    </shadow-box>
    <shadow-box>
      <form-row>
        <in-line-check-box id="test_administered_sfst"
                     :path="path" fg_class="col-sm-6"
                     :option="true">Prescribed Physical Coordination Test (SFST)
        </in-line-check-box>
        <date-field id="test_date" :path="path" fg_class="col-sm-3" v-if="doesAttributeExist(path, 'test_administered_sfst_true')"
                  rules="required|validDt|notFutureDt|notGtYearAgo">Date of test</date-field>
        <time-field id="test_time" :path="path" fg_class="col-sm-3" v-if="doesAttributeExist(path, 'test_administered_sfst_true')"
                    rules="required|validTime|notFutureDateTime:@test_date|notBeforeCareDateTime:@prohibition_start_date,@prohibition_start_time,@test_date">Time</time-field>
      </form-row>
    </shadow-box>
</form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";

export default {
  name: "OfficersReport",
  mixins: [CardsCommon]
}
</script>

<style scoped>

</style>