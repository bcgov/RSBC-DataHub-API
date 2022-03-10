<template>
  <form-card title="Vehicle Disposition">
    <div>
      <form-row>
        <radio-field id="vehicle_impounded" fg_class="col-sm-6" rules="required" :options='["Yes", "No"]'>Vehicle Towed?</radio-field>
      </form-row>
      <form-row>
        <radio-field id="reason_for_not_impounding" fg_class="col-sm-6"
                     :options='["Released to other driver", "Left at roadside"]'
                     :visible="showVehicleNotImpounded">Reason for not towing?</radio-field>
      </form-row>
      <form-row v-if="isReleasedToOtherDriver">
        <text-field id="vehicle_released_to" :visible="showVehicleNotImpounded" fg_class="col-sm-6" >
          Vehicle Released To</text-field>
        <date-field id="released_date" fg_class="col-sm-3" :visible="showVehicleNotImpounded"
                  rules="required|validDt|notFutureDt|notGtYearAgo">Date Released</date-field>
        <time-field id="released_time" fg_class="col-sm-3" :visible="showVehicleNotImpounded"
                    rules="required|validTime|notFutureDateTime:@released_date">Time</time-field>
      </form-row>
      <form-row>
        <radio-field id="location_of_keys" :visible="showVehicleImpounded" fg_class="col-sm-6" rules="required"
                     :options='["With vehicle", "With driver"]'>Location of Keys?</radio-field>
      </form-row>
      <form-row>
        <type-ahead-field id="impound_lot_operator" fg_class="col-sm-12" :visible="showVehicleImpounded" rules="required"
                     :suggestions="getArrayOfImpoundLotOperators">Tow Operator (name, lot address, city & phone)</type-ahead-field>
      </form-row>
    </div>
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