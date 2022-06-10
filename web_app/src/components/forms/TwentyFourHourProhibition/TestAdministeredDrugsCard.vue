<template>
<form-card title="Test Administered - Drugs 215(3)">
    <shadow-box>
      <form-row>
        <in-line-check-box id="test_administered_adse" :path="path" fg_class="col-sm-6"
                     :option='true'>Approved Drug Screening Equipment
        </in-line-check-box>
      </form-row>
      <form-row v-if="doesAttributeExist(path, 'test_administered_adse_true')">
        <check-field  id="positive_adse" :path="path + '/test_administered_adse_true'" fg_class="col-sm-6"
                     :options='[["thc", "THC"], ["cocaine", "Cocaine"]]'>Test result</check-field>
        <date-field id="test_date" :path="path" fg_class="col-sm-3"
                  rules="required|validDt|notFutureDt|notGtYearAgo">Date of test</date-field>
        <time-field id="test_time" :path="path" fg_class="col-sm-3"
                    rules="required|validTime|notFutureDateTime:@test_date|notBeforeCareDateTime:@prohibition_start_date,@prohibition_start_time,@test_date">Time</time-field>
      </form-row>
    </shadow-box>
    <shadow-box>
      <form-row>
        <in-line-check-box :path="path" id="test_administered_sfst" fg_class="col-sm-6"
                           :option="true">Prescribed Physical Coordination Test (SFST)
        </in-line-check-box>
        <date-field id="test_date" :path="path" fg_class="col-sm-3"
                    v-if="doesAttributeExist(path, 'test_administered_sfst_true')"
                  rules="required|validDt|notFutureDt|notGtYearAgo">Date of test</date-field>
        <time-field id="test_time" :path="path" fg_class="col-sm-3"
                    v-if="doesAttributeExist(path, 'test_administered_sfst_true')"
                    rules="required|validTime|notFutureDateTime:@test_date|notBeforeCareDateTime:@prohibition_start_date,@prohibition_start_time,@test_date">Time</time-field>
      </form-row>
    </shadow-box>
    <shadow-box>
      <form-row>
        <in-line-check-box :path="path" id="test_administered_dre" fg_class="col-sm-6"
                     :option="true">Prescribed Physical Coordination Test (DRE)
        </in-line-check-box>
        <date-field id="test_date" :path="path" fg_class="col-sm-3"
                    v-if="doesAttributeExist(path, 'test_administered_dre_true')"
                  rules="required|validDt|notFutureDt|notGtYearAgo">Date of test</date-field>
        <time-field id="test_time" :path="path" fg_class="col-sm-3"
                    v-if="doesAttributeExist(path, 'test_administered_dre_true')"
                    rules="required|validTime|notFutureDateTime:@test_date|notBeforeCareDateTime:@prohibition_start_date,@prohibition_start_time,@test_date">Time</time-field>
      </form-row>
    </shadow-box>
</form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";

export default {

  name: "TestAdministeredDrugsCard",
  mixins: [CardsCommon],
  computed: {
    drugConclusion() {
      return "Ability to drive affected by a drug";
    },
  }
}
</script>