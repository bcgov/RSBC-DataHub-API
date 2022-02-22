<template>
<form-card title="Test Administered - Drugs 215(3)">
    <shadow-box>
      <form-row>
        <check-field :show_label="false" id="test_administered_adse" fg_class="col-sm-6"
                     :options='["Approved Drug Screening Equipment"]'>Test Administered
        </check-field>
      </form-row>
      <form-row>
        <check-field v-if="isTestAdministeredADSE" id="positive_adse" fg_class="col-sm-6"
                     :options='["THC", "Cocaine"]'>Test result</check-field>
        <date-field id="test_date" fg_class="col-sm-3" :visible="isTestAdministeredADSE"
                  rules="required|validDt|notFutureDt|notGtYearAgo">Date of test</date-field>
        <time-field id="test_time" fg_class="col-sm-3" :visible="isTestAdministeredADSE"
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
    <shadow-box>
      <form-row>
        <check-field :show_label="false" id="test_administered_dre" fg_class="col-sm-6"
                     :options='["Prescribed Physical Coordination Test (DRE)"]'>&nbsp;
        </check-field>
        <date-field id="test_date" fg_class="col-sm-3" :visible="isTestAdministeredDRE"
                  rules="required|validDt|notFutureDt|notGtYearAgo">Date of test</date-field>
        <time-field id="test_time" fg_class="col-sm-3" :visible="isTestAdministeredDRE"
                    rules="required|validTime|notFutureDateTime:@test_date|notBeforeCareDateTime:@prohibition_start_date,@prohibition_start_time,@test_date">Time</time-field>
      </form-row>
    </shadow-box>
    <form-row>
        <check-field id="result_drug" fg_class="col-sm-12"
                     :options='[this.drugConclusion]'><strong>Result</strong></check-field>
    </form-row>
</form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";
import {mapGetters} from "vuex";

export default {

  name: "TestAdministeredDrugsCard",
  mixins: [CardsCommon],
  mounted () {
    // set "Ability to drive affected by a drug" to checked
    this.$store.commit("updateFormField", {
      target: {
        id: "result_drug",
        value: this.drugConclusion}
    })
  },
  computed: {
    drugConclusion() {
      return "Ability to drive affected by a drug";
    },
    isProhibitionTypeSelected() {
      return this.getAttributeValue('prohibition_type').length > 0;
    },
    isProhibitionTypeDrugs() {
      return this.getAttributeValue('prohibition_type') === "Drugs 215(3)";
    },
    isOperatingGroundsOther() {
      return this.getAttributeValue('operating_grounds') === "Other";
    },
    isPrescribedTestUsed() {
      return this.getAttributeValue('prescribed_device').substr(0,3) === "Yes";
    },
    ...mapGetters(['isTestAdministeredDRE', 'isTestAdministeredSFST', 'isTestAdministeredADSE'])
  }
}
</script>