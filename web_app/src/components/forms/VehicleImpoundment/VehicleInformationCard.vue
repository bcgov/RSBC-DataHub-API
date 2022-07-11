<template>
<form-card title="Vehicle information">
  <form-row>
    <jurisdiction-field id="plate_province" :path=path fg_class="col-sm-3">Jurisdiction</jurisdiction-field>
    <plate-number id="plate_number" :path=path fg_class="col-sm-6">Plate Number</plate-number>
  </form-row>
  <form-row>
    <vehicle-year :path=path input_type="number" fg_class="col-sm-2" rules="max:4">Vehicle Year</vehicle-year>
    <vehicle-make-model :path=path fg_class="col-sm-5">Vehicle Make</vehicle-make-model>
    <vehicle-colour :path=path fg_class="col-sm-3"></vehicle-colour>
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

export default {
  name: "VehicleInformationCard",
  mixins: [CardsCommon],
}
</script>

<style scoped>

</style>