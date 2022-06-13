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
    <vehicle-year :path=path rules="vehicleYear" fg_class="col-sm-2">Vehicle Year</vehicle-year>
    <vehicle-make-model :path="path" fg_class="col-sm-3"></vehicle-make-model>
    <vehicle-style :path=path fg_class="col-sm-4"></vehicle-style>
    <vehicle-colour :path=path fg_class="col-sm-3"></vehicle-colour>
  </form-row>
  <form-row>
    <text-field id="vin_number" :path=path fg_class="col-sm-5" rules="max:20">VIN Number</text-field>
    <province-field id="puj_code" :path=path fg_class="col-sm-3" :default-to-bc=false>NSC Prov / State</province-field>
    <text-field id="nsc_number" :path=path fg_class="col-sm-4" rules="max:14">NSC Number</text-field>
  </form-row>
</form-card>
</template>

<script>

import CardsCommon from "@/components/forms/CardsCommon";

export default {
  name: "VehicleInformationCard",
  mixins: [CardsCommon],
}
</script>

<style scoped>

</style>