<template>
  <form-card title="Linkage">
    <p>The officer determined the following (relationship between driver, owner and the vehicle)</p>
    <form-row>
      <in-line-check-box id="linkage_keys" :path=path :option="true">{{ keyText }}</in-line-check-box>
    </form-row>
    <form-row v-if="doesAttributeExist(path, 'linkage_keys_true')">
      <text-field id="note" :path="path + '/linkage_keys_true'" fg_class="col-sm-12">Where were the keys located?</text-field>
    </form-row>
    <form-row>
      <in-line-check-box id="linkage_principal_operator" :path=path :option="true">The driver is a principal operator</in-line-check-box>
    </form-row>
    <form-row>
      <in-line-check-box id="linkage_owner_within" :path=path :option="true">The owner was in the vehicle</in-line-check-box>
    </form-row>
    <form-row>
      <in-line-check-box id="linkage_owner_aware" :path=path :option="true">The owner was aware
        the driver was in possession of the vehicle (explain in the incident details)</in-line-check-box>
    </form-row>
    <form-row>
      <in-line-check-box id="linkage_transfer" :path=path :option="true">Vehicle subject to a
          transfer notice (explain in the incident details)</in-line-check-box>
    </form-row>
    <form-row>
      <in-line-check-box id="linkage_other" :path=path :option="true">Other (explain in the incident details)</in-line-check-box>
    </form-row>
  </form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";

export default {
  name: "LinkageCard",
  mixins: [CardsCommon],
  computed: {
    keyText() {
      return "Location of vehicle key(s) (explain below or in the incident details)"
    }
  }
}
</script>
