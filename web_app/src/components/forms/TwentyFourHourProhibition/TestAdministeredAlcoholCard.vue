<template>
<form-card title="Test Administered - Alcohol 215(2)">
    <radio-field id="test_administered" :path="path" fg_class="col-sm-6"
                     :options='[
                         ["asd", "Alco-Sensor FST (ASD)"],
                         ["instrument", "Approved Instrument"],
                         ["sfst", "Prescribed Physical Coordination Test (SFST)"]]'>Which test was used?</radio-field>
      <form-row>
        <date-field v-if="doesAttributeExist(path, 'test_administered_asd')"
                    id="asd_expiry_date"
                    :path="path + '/test_administered_asd'"
                    fg_class="col-sm-6"
                    rules="required|validDt|notExpiredDt">ASD expiry date</date-field>
      </form-row>
      <form-row v-if="doesAttributeExist(path, 'test_administered_asd')">
        <radio-field id="result_alcohol"
                     :path="path + '/test_administered_asd'" fg_class="col-sm-6"
                     :options='[["51-59", "51-59 mg%"], ["warn", "Warn"], ["fail", "Fail"]]'>Result</radio-field>

      </form-row>
      <form-row v-if="doesAttributeExist(path, 'test_administered_instrument')">
        <text-field rules="required|bac_result"
                    id="test_result_bac" :path="path + '/test_administered_instrument'"
                    fg_class="col-sm-2">BAC Result (mg%)
        </text-field>
      </form-row>

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