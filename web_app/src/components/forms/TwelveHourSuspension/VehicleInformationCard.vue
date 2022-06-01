<template>
<form-card title="Vehicle information">
  <form-row>
      <jurisdiction-field id="plate_province" :path="path"  fg_class="col-sm-3">Jurisdiction</jurisdiction-field>
      <plate-number id="plate_number" :path="path"  fg_class="col-sm-6">Plate Number</plate-number>
    </form-row>
  <form-row>
    <text-field id="vehicle_year" :path="path"  rules="vehicleYear" fg_class="col-sm-2">Vehicle Year</text-field>
    <text-field id="vehicle_make" :path="path" fg_class="col-sm-2" rules="max:7">Vehicle Make</text-field>
    <text-field id="vehicle_model" :path="path"  fg_class="col-sm-3" rules="max:6">Vehicle Model</text-field>
    <text-field id="vehicle_color" :path="path"  fg_class="col-sm-2" rules="max:4">Vehicle Colour</text-field>
  </form-row>
  <form-row>
    <province-field id="puj_code" :path="path"  fg_class="col-sm-2" :default-to-bc=false>PUJ Code</province-field>
    <text-field id="nsc_number" :path="path"  fg_class="col-sm-7" rules="max:14">NSC Number</text-field>
  </form-row>
</form-card>
</template>

<script>

import CardsCommon from "@/components/forms/CardsCommon";
import {mapGetters} from "vuex";

export default {
  name: "VehicleInformationCard",
  mixins: [CardsCommon],
  computed: {
        ...mapGetters(["getArrayOfCommonCarColors", "getArrayOfVehicleYears",
      "getArrayOfVehicleMakes", "getArrayOfVehicleModels", "getArrayOfVehicleStyles"])
  }
}
</script>

<style scoped>

</style>