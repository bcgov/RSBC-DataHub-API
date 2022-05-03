<template>
<form-card title="Vehicle information">
  <form-row>
    <jurisdiction-field id="plate_province" fg_class="col-sm-3">Jurisdiction</jurisdiction-field>
    <plate-number id="plate_number" fg_class="col-sm-6">Plate Number</plate-number>
  </form-row>
  <form-row>
    <type-ahead-field :suggestions="getArrayOfVehicleYears" id="vehicle_year" fg_class="col-sm-2">Vehicle Year</type-ahead-field>
    <type-ahead-field :suggestions="getArrayOfVehicleMakes" id="vehicle_make" input_type="number" fg_class="col-sm-4">Vehicle Make</type-ahead-field>
    <type-ahead-field :suggestions="getArrayOfVehicleModels" id="vehicle_model" fg_class="col-sm-4">Vehicle Model</type-ahead-field>
    <type-ahead-field :suggestions="getArrayOfCommonCarColors" id="vehicle_color" fg_class="col-sm-2">Vehicle Colour</type-ahead-field>
  </form-row>
  <form-row>
    <text-field id="registration_number" fg_class="col-sm-4">Registration Number</text-field>
    <check-field id="is_nsc" fg_class="col-sm-2" :options='["NSC?"]'></check-field>
    <text-field id="vin_number" fg_class="col-sm-6">Vehicle Identification Number (VIN)</text-field>
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