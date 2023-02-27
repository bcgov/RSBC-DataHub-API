<template>
  <form-card title="Linkage Factors">
    <p>The officer determined the following: (relationship between driver, owner and the vehicle)</p>
    <form-row>
      <in-line-check-box id="linkage_keys" :option="true" :path=path>Location of vehicle key(s) (explain below or in incident details)</in-line-check-box>
    </form-row>
    <form-row v-if="doesAttributeExist(path, 'linkage_keys_true')">
      <text-field id="note" fe_class="uppercase" fg_class="col-sm-12" :path="path + '/linkage_keys_true'">Where are the keys located?</text-field>
    </form-row>
    <form-row>
      <in-line-check-box id="linkage_principal_operator" :option="true" :path=path>The driver is a principal operator</in-line-check-box>
    </form-row>
    <form-row>
      <in-line-check-box id="linkage_owner_within" :option="true" :path=path>The owner was in the vehicle</in-line-check-box>
    </form-row>
    <form-row>
      <in-line-check-box id="linkage_owner_aware" :option="true" :path=path>The owner was aware the driver was in possession of the vehicle (explain in incident details)</in-line-check-box>
    </form-row>
    <form-row>
      <in-line-check-box id="linkage_transfer" :option="true" :path=path>Vehicle subject to a transfer notice (explain in incident details)</in-line-check-box>
    </form-row>
    <form-row>
      <in-line-check-box id="linkage_other" :option="true" :path=path>Other (explain in incident details)</in-line-check-box>
    </form-row>
  </form-card>
</template>
<script>
  import CardsCommon from "@/components/forms/CardsCommon";
  export default {
    name: "LinkageCard",
    mixins: [CardsCommon],
  }
</script>