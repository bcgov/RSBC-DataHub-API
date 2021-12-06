<template>
  <form-card title="Vehicle Impoundment or Disposition">
      <form-row>
        <radio-field id="vehicle_impounded" fg_class="col-sm-6" :options='["Yes", "No"]'>Vehicle Impounded?</radio-field>
      </form-row>
      <form-row>
        <radio-field id="reason_for_not_impounding" fg_class="col-sm-6"
                     :options='["Released to other driver", "Left at roadside", "Private tow", "Seized for investigation"]'
                     :visible="showVehicleNotImpounded">Reason for not impounding?</radio-field>
      </form-row>
      <form-row v-if="isReleasedToOtherDriver">
        <text-field id="vehicle_released_to" :visible="showVehicleNotImpounded" fg_class="col-sm-6" >
          Vehicle Released To</text-field>
        <date-time id="datetime_released" :visible="showVehicleNotImpounded" fg_class="col-sm-6" >
          Date and Time Released</date-time>
      </form-row>
      <form-row>
        <radio-field id="location_of_keys" :visible="showVehicleImpounded" fg_class="col-sm-6"
                     :options='["With vehicle", "With driver"]'>Location of Keys?</radio-field>
      </form-row>
      <form-row>
        <type-ahead-field id="impound_lot_operator" fg_class="col-sm-12" :visible="showVehicleImpounded"
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
    ...mapGetters(["getAttributeValue", "getArrayOfImpoundLotOperators"]),
    showVehicleImpounded() {
      return this.getAttributeValue('vehicle_impounded') === "Yes";
    },
    showVehicleNotImpounded() {
      return this.getAttributeValue('vehicle_impounded') === "No";
    },
    isReleasedToOtherDriver() {
      return this.getAttributeValue('reason_for_not_impounding') === "Released to other driver";
    },
  }
}
</script>

<style scoped>

</style>