<template>
<form-card title="Vehicle information">
  <form-row>
    <jurisdiction-field id="plate_province" :path=path fg_class="col-sm-3">Jurisdiction</jurisdiction-field>
    <plate-number id="plate_number" :path=path fg_class="col-sm-6">Plate Number</plate-number>
  </form-row>
  <form-row>
    <text-field id="plate_year" :path=path rules="plate_year" fg_class="col-sm-4">Plate Year</text-field>
    <text-field id="plate_val_tag" :path=path input_type="number" fg_class="col-sm-4">Plate Val Tag</text-field>
    <text-field id="registration_number" :path=path fg_class="col-sm-4">Registration Number</text-field>
  </form-row>
  <form-row>
    <text-field id="vehicle_year" :path=path rules="vehicleYear" fg_class="col-sm-2">Vehicle Year</text-field>
    <type-ahead-field :suggestions="getArrayOfVehicleMakes" :path=path id="vehicle_make" input_type="number" fg_class="col-sm-3">Vehicle Make</type-ahead-field>
    <type-ahead-field :suggestions="getArrayOfVehicleModels" :path=path id="vehicle_model" fg_class="col-sm-3">Vehicle Model</type-ahead-field>
    <type-ahead-field :suggestions="getArrayOfVehicleStyles" :path=path id="vehicle_type" fg_class="col-sm-2" rules="max:6">Vehicle Type</type-ahead-field>
    <type-ahead-field :suggestions="getArrayOfCommonCarColors" :path=path id="vehicle_color" fg_class="col-sm-2" rules="max:4">Vehicle Colour</type-ahead-field>
  </form-row>
  <form-row>
    <text-field id="vin_number" :path=path fg_class="col-sm-5" rules="max:20">VIN Number</text-field>
    <province-field id="puj_code" :path=path fg_class="col-sm-2" :default-to-bc=false>PUJ Code</province-field>
    <text-field id="nsc_number" :path=path fg_class="col-sm-5" rules="max:14">NSC Number</text-field>
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