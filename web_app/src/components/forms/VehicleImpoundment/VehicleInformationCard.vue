<template>
<form-card title="Vehicle information">
  <form-row>
    <jurisdiction-field id="plate_province" :path=path fg_class="col-sm-3">Jurisdiction</jurisdiction-field>
    <plate-number id="plate_number" :path=path fg_class="col-sm-6">Plate Number</plate-number>
  </form-row>
  <form-row>
    <text-field id="vehicle_year" :path=path input_type="number" fg_class="col-sm-2" rules="max:4">Vehicle Year</text-field>
    <text-field id="vehicle_make" :path=path fg_class="col-sm-4" rules="max:7">Vehicle Make</text-field>
    <text-field id="vehicle_model" :path=path fg_class="col-sm-4" rules="max:6">Vehicle Model</text-field>
    <text-field id="vehicle_color" :path=path fg_class="col-sm-2" rules="max:4">Vehicle Colour</text-field>
  </form-row>
  <form-row>
    <text-field id="registration_number" :path=path fg_class="col-sm-4">Registration Number</text-field>
    <check-field id="is_nsc" :path=path fg_class="col-sm-2" :options='[["nsc", "NSC?"]]'></check-field>
    <text-field id="vin_number" :path=path fg_class="col-sm-6">Vehicle Identification Number (VIN)</text-field>
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