<template>
  <div>
    <form-row>
      <radio-description id="location_of_keys" :path="path" fg_class="col-sm-6" rules="required"
                   :options='[["WITH VEHICLE", "With vehicle"], ["WITH DRIVER", "With driver"]]'>Location of Keys?</radio-description>
    </form-row>
    <impound-lot-operator :path="path">
      Impound Lot Operator (name, lot address, city & phone)</impound-lot-operator>
  </div>
</template>

<script>

import CardsCommon from "@/components/forms/CardsCommon";

export default {
name: "VehicleImpounded",
mixins: [CardsCommon],
}
</script>