<template>
<form-card title="Test Administered - Drugs 215(3)">
  <radio-field id="test_administered" :path="path" fg_class="col-sm-6"
               :options='[
                   ["adse", "Approved Drug Screening Equipment"],
                   ["sfst", "Prescribed Physical Coordination Test (SFST)"],
                   ["dre", "Prescribed Physical Coordination Test (DRE)"]]'>Which test was used?</radio-field>

  <form-row>
      <check-field v-if="doesAttributeExist(path, 'test_administered_adse')"
                   id="positive_adse" :path="path + '/test_administered_adse'" fg_class="col-sm-6"
                   :options='[["thc", "THC"], ["cocaine", "Cocaine"]]'>Test result</check-field>
  </form-row>
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