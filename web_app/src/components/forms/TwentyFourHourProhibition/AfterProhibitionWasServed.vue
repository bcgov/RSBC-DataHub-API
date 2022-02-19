<template>
  <div>
    <form-card>
    <radio-field id="test_requested_after" fg_class="col-sm-12"
                         :options='["Yes",
                         "No",
                         "Not applicable, refused by driver"]'>
      After the prohibition was served, did the driver request a breath test or prescribed physical coordination test?
    </radio-field>
  </form-card>
<form-card v-if="isPrescribedTestUsed" :title="testAdministeredTitle">
  <shadow-box v-if="isProhibitionTypeAlcohol">
    <form-row>
      <check-field :show_label="false"  id="after_test_administered" fg_class="col-sm-6"
                   :options='["Alco-Sensor FST (ASD)"]'>Test Administered</check-field>
      <date-field v-if="isProhibitionTypeAlcohol && isTestAdministeredASD" id="after_asd_expiry_date" fg_class="col-sm-6" rules="notExpiredDt">ASD expiry date</date-field>
      <radio-field v-if="isProhibitionTypeAlcohol && isTestAdministeredASD" id="after_result_alcohol" fg_class="col-sm-12"
                   :options='["51-99 mg%", "Over 99 mg%"]'>Result</radio-field>
    </form-row>
  </shadow-box>
  <shadow-box v-if="isProhibitionTypeAlcohol && isPrescribedTestUsed">
    <form-row>
      <check-field :show_label="false"  id="after_test_administered" fg_class="col-sm-6"
                   :options='["Approved Instrument"]'></check-field>
    </form-row>
    <form-row>
      <check-field v-if="isTestAdministeredApprovedInstrument" id="after_result_alcohol_approved_instrument" fg_class="col-sm-2"
                   :options='["BAC"]'>Result</check-field>
      <text-field v-if="isTestAdministeredApprovedInstrument" id="after_test_result_bac" fg_class="col-sm-10"></text-field>
    </form-row>
  </shadow-box>
  <shadow-box v-if="isProhibitionTypeDrugs">
    <form-row>
      <check-field :show_label="false" id="after_test_administered" fg_class="col-sm-12"
                   :options='["Approved Drug Screening Equipment"]'>Test Administered
      </check-field>
    </form-row>
    <form-row>
      <check-field v-if="isTestAdministeredADSE" id="after_positive_adse" fg_class="col-sm-12"
                   :options='["THC", "Cocaine"]'>Test result</check-field>
    </form-row>
    <form-row>
      <date-time v-if="isTestAdministeredADSE" id="after_time_of_physical_test_adse" fg_class="col-sm-12">Time of test</date-time>
    </form-row>
  </shadow-box>
  <shadow-box v-if="isProhibitionTypeDrugs && isPrescribedTestUsed">
    <form-row>
      <check-field :show_label="false" id="after_test_administered" fg_class="col-sm-12"
                   :options='["Prescribed Physical Coordination Test (SFST)"]'>&nbsp;
      </check-field>
    </form-row>
    <form-row>
      <date-time v-if="isTestAdministeredSFST" id="after_time_of_physical_test_sfst" fg_class="col-sm-12">Time of test</date-time>
    </form-row>
  </shadow-box>
  <shadow-box v-if="isProhibitionTypeDrugs && isPrescribedTestUsed">
    <form-row>
      <check-field :show_label="false" id="after_test_administered" fg_class="col-sm-12"
                   :options='["Prescribed Physical Coordination Test (DRE)"]'>&nbsp;
      </check-field>
    </form-row>
    <form-row v-if="isTestAdministeredDRE">
      <date-time id="after_start_time_of_physical_test_dre" fg_class="col-sm-12">Time of opinion</date-time>
    </form-row>
    <form-row>
      <text-field id="after_positive_dre" fg_class="col-sm-12">Notes (expand to 3 lines)</text-field>
    </form-row>
  </shadow-box>
  <form-row v-if="isPrescribedTestUsed && isProhibitionTypeDrugs">
      <check-field id="after_result_drug_sfst" fg_class="col-sm-12"
                   :options='["Ability to drive affected by a drug"]'><strong>Result</strong></check-field>
    </form-row>
</form-card>
  </div>

</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";

export default {
  name: "OfficersReport",
  mixins: [CardsCommon],
  computed: {
    isProhibitionTypeSelected() {
      return this.getAttributeValue('prohibition_type').length > 0;
    },
    isProhibitionTypeDrugs() {
      return this.getAttributeValue('prohibition_type') === "Drugs 215(3)";
    },
    isProhibitionTypeAlcohol() {
      return this.getAttributeValue('prohibition_type') === "Alcohol 215(2)";
    },
    isOperatingGroundsOther() {
      return this.getAttributeValue('after_operating_grounds') === "Other";
    },
    isPrescribedTestUsed() {
      return this.getAttributeValue('test_requested_after').substr(0,3) === "Yes";
    },
    isTestAdministeredASD() {
      const root = this.getAttributeValue('after_test_administered')
      console.log('after_test_administered', root)
      if (Array.isArray(root)) {
        return root.includes("Alco-Sensor FST (ASD)")
      }
      return false;
    },
    isTestAdministeredApprovedInstrument() {
      const root = this.getAttributeValue('after_test_administered')
      if (Array.isArray(root)) {
        return root.includes("Approved Instrument")
      }
      return false;
    },
    isTestAdministeredADSE() {
      const root = this.getAttributeValue('after_test_administered')
      console.log('after_test_administered', root)
      if (Array.isArray(root)) {
        return root.includes("Approved Drug Screening Equipment")
      }
      return false;
    },
    isTestAdministeredSFST() {
      const root = this.getAttributeValue('after_test_administered')
      console.log('after_test_administered', root)
      if (Array.isArray(root)) {
        return root.includes("Prescribed Physical Coordination Test (SFST)")
      }
      return false;
    },
    isTestAdministeredDRE() {
      const root = this.getAttributeValue('after_test_administered')
      console.log('after_test_administered', root)
      if (Array.isArray(root)) {
        return root.includes("Prescribed Physical Coordination Test (DRE)")
      }
      return false;
    },
    testAdministeredTitle() {
      return "Test Administered - " + this.getAttributeValue('prohibition_type')
    }
  }
}
</script>

<style scoped>

</style>