<template>
  <form-card title="Vehicle Information">
    <form-row>
      <jurisdiction-field id="plate_province" fg_class="col-sm-3" :path=path>Jurisdiction</jurisdiction-field>
      <plate-number id="plate_number" fe_class="uppercase" fg_class="col-sm-6" :path=path>Plate Number</plate-number>
    </form-row>
    <form-row>
      <vehicle-year fg_class="col-sm-2" input_type="number" :path=path rules="max:4"></vehicle-year>
      <vehicle-make-model fg_class="col-sm-5" :path=path></vehicle-make-model>
      <vehicle-colour fg_class="col-sm-3" :path=path></vehicle-colour>
    </form-row>
    <form-row>
      <text-field id="registration_number" :path=path fg_class="col-sm-4">Registration Number</text-field>
      <check-field id="is_nsc" :path=path fg_class="col-sm-2" :options='[["nsc", "NSC number on vehicle?"]]'></check-field>
      <text-field id="vin_number" :path=path fg_class="col-sm-6">Vehicle Identification Number (VIN)</text-field>
    </form-row>
  </form-card>
</template>
<script>
  import CardsCommon from "@/components/forms/CardsCommon";
  export default {
    name: "VehicleInformationCard",
    mixins: [ CardsCommon ]
  }
</script>