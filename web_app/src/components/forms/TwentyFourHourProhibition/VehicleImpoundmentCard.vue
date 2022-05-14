<template>
  <form-card title="Vehicle Impoundment or Disposition">
      <form-row>
        <radio-field id="vehicle_impounded"
                     fg_class="col-sm-6" :options='["Yes", "No"]'
                     rules="required">Vehicle Impounded?
        </radio-field>
      </form-row>
      <form-row>
        <radio-field id="reason_for_not_impounding" fg_class="col-sm-6"
                     :options='["Released to other driver", "Left at roadside", "Private tow", "Seized for investigation"]'
                     :visible="showVehicleNotImpounded">Reason for not impounding?</radio-field>
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
      <impound-lot-operator v-if="showVehicleImpounded" fg_class="col-sm-12" rules="required">
        Impound Lot Operator (name, lot address, city & phone)</impound-lot-operator>
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