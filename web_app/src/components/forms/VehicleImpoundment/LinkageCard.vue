<template>
  <form-card title="Linkage">
    <form-row>
      <check-field id="linkage" fg_class="col-sm-12" :options='[
          keyText,
          "The driver is a principal operator",
          "The owner was in the vehicle",
          "The owner was aware the driver was in possession of the vehicle (explain in the incident details)",
          "Vehicle subject to a transfer notice (explain in the incident details)",
          "Other (explain in the incident details)"]'>
          The officer determined the following (relationship between driver, owner and the vehicle)
      </check-field>
    </form-row>
    <form-row>
      <text-field v-if="isVehicleKeySelected" id="vehicle_key_linkage" fg_class="col-sm-12">Where were the keys located?</text-field>
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
    },
    isVehicleKeySelected() {
      return this.getAttributeValue('linkage').includes(this.keyText);
    },
  }
}
</script>
