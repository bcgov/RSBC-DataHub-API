<template>
  <form-card title="Vehicle Impounded Details">
      <form-row>
        <text-field id="offence_address" fg_class="col-sm-8" rules="required">Intersection or Address of Offence</text-field>
        <type-ahead-field id="offence_city" fg_class="col-sm-4" :suggestions="getArrayOfBCCityNames" rules="required">City</type-ahead-field>
      </form-row>
      <form-row>
        <date-time id="prohibition_start_time" fg_class="col-sm-4" rules="required|notFutureDt">
          Time of driving, care or control
        </date-time>
      </form-row>
      <form-row>
        <date-field id="impounded_dt" fg_class="col-sm-4">The motor vehicle was impounded on</date-field>
        <type-ahead-field id="impound_lot_operator" fg_class="col-sm-8"
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