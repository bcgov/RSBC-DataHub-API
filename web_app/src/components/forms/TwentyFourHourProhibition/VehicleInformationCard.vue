<template>
<form-card title="Vehicle information">
  <form-row>
    <jurisdiction-field id="plate_province" fg_class="col-sm-3">Jurisdiction</jurisdiction-field>
    <plate-number id="plate_number" fg_class="col-sm-6">Plate Number</plate-number>
  </form-row>
  <form-row>
    <text-field id="plate_year" rules="plate_year" fg_class="col-sm-4">Plate Year</text-field>
    <text-field id="plate_val_tag" input_type="number" fg_class="col-sm-4">Plate Val Tag</text-field>
    <text-field id="registration_number" fg_class="col-sm-4">Registration Number</text-field>
  </form-row>
  <form-row>
    <text-field id="vehicle_year" rules="vehicleYear" fg_class="col-sm-2">Vehicle Year</text-field>
    <type-ahead-field :suggestions="getArrayOfVehicleMakes" id="vehicle_make" input_type="number" fg_class="col-sm-3">Vehicle Make</type-ahead-field>
    <type-ahead-field :suggestions="getArrayOfVehicleModels" id="vehicle_model" fg_class="col-sm-3">Vehicle Model</type-ahead-field>
    <type-ahead-field :suggestions="getArrayOfVehicleStyles" id="vehicle_type" fg_class="col-sm-2">Vehicle Type</type-ahead-field>
    <type-ahead-field :suggestions="getArrayOfCommonCarColors" id="vehicle_color" fg_class="col-sm-2">Vehicle Colour</type-ahead-field>
  </form-row>
  <form-row>
    <text-field id="vin_number" fg_class="col-sm-5">VIN Number</text-field>
    <province-field id="puj_code" fg_class="col-sm-2">PUJ Code</province-field>
    <text-field id="nsc_number" fg_class="col-sm-5">NSC Number</text-field>
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
    ...mapGetters(["getArrayOfCommonCarColors", "getArrayOfVehicleYears", "getArrayOfVehicleStyles",
      "getArrayOfVehicleMakes", "getArrayOfVehicleModels"])
  }
}
</script>

<style scoped>

</style>