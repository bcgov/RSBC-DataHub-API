<template>
  <form-card title="Impound Lot">
      <form-row>
        <date-field id="impounded_dt" fg_class="col-sm-12">The motor vehicle was impounded on</date-field>
      </form-row>
      <form-row>
        <type-ahead-field id="impound_lot_operator" fg_class="col-sm-12"
            :suggestions="getArrayOfImpoundLotOperators">Impound Lot Operator (name, lot address, city & phone)</type-ahead-field>
      </form-row>
  </form-card>
</template>

<script>

import CardsCommon from "@/components/forms/CardsCommon";
import { mapGetters } from 'vuex';


export default {
name: "VehicleImpoundmentCard",
mixins: [CardsCommon],
  computed: {
    ...mapGetters(["getAttributeValue", "getArrayOfImpoundLotOperators"])
  }
}
</script>

<style scoped>

</style>