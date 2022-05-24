<template>
  <form-card title="Vehicle Impoundment or Disposition">
      <form-row>
        <radio-field id="vehicle_impounded" :path="path"
                     fg_class="col-sm-6" :options='[["yes", "Yes"], ["no", "No"]]'
                     rules="required">Vehicle Impounded?
        </radio-field>
      </form-row>
      <vehicle-not-impounded
          v-if="doesAttributeExist(this.path, 'vehicle_impounded_no')"
          :path="this.path + '/vehicle_impounded_no'">
      </vehicle-not-impounded>
      <vehicle-impounded
          v-if="doesAttributeExist(this.path, 'vehicle_impounded_yes')"
          :path="this.path + '/vehicle_impounded_yes'">
      </vehicle-impounded>
  </form-card>
</template>

<script>

import CardsCommon from "@/components/forms/CardsCommon";
import VehicleNotImpounded from "@/components/forms/TwentyFourHourProhibition/VehicleNotImpounded";
import VehicleImpounded from "@/components/forms/TwentyFourHourProhibition/VehicleImpounded";

export default {
name: "VehicleImpoundmentCard",
mixins: [CardsCommon],
  components: {
    VehicleImpounded,
    VehicleNotImpounded
  }
}
</script>

<style scoped>

</style>