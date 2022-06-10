<template>
  <form-card title="Vehicle Disposition">
    <div>
      <form-row>
        <radio-field id="vehicle_impounded" :path="path"
                     fg_class="col-sm-6"
                     rules="required"
                     :options='[["yes", "Yes"], ["no", "No"]]'>Vehicle Towed?</radio-field>
      </form-row>
      <vehicle-towed-card :path="path + '/vehicle_impounded_yes'" v-if="doesAttributeExist(this.path, 'vehicle_impounded_yes')">

      </vehicle-towed-card>
      <vehicle-not-towed-card :path="path + '/vehicle_impounded_no'" v-if="doesAttributeExist(this.path, 'vehicle_impounded_no')">

      </vehicle-not-towed-card>
    </div>
  </form-card>
</template>

<script>

import CardsCommon from "@/components/forms/CardsCommon";
import VehicleTowedCard from "@/components/forms/TwelveHourSuspension/VehicleTowedCard";
import VehicleNotTowedCard from "@/components/forms/TwelveHourSuspension/VehicleNotTowedCard";
import { mapGetters } from 'vuex';


export default {
name: "VehicleImpoundmentCard",
mixins: [CardsCommon],
  computed: {
    ...mapGetters(["getAttributeValue"]),
  },
  components: {
    VehicleNotTowedCard,
    VehicleTowedCard
  }
}
</script>

<style scoped>

</style>