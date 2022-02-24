<template>
<form-card title="Driver's Information">
  <div>
    <form-row>
      <driver-licence-number id="drivers_number" :rules="bcdlNumberRules">Driver's Licence Number</driver-licence-number>
      <jurisdiction-field :disabled=true id="drivers_licence_jurisdiction" fg_class="col-sm-3">Prov / State / International</jurisdiction-field>
    </form-row>
    <form-row>
      <text-field id="last_name" fg_class="col-sm-4" placeholder="Last Name" rules="required|max:20">Last Name</text-field>
      <text-field id="first_name" fg_class="col-sm-4" placeholder="Given Names" rules="required|max:20">Given Names</text-field>
      <dob-field id="dob" fg_class="col-sm-4">Date of Birth</dob-field>
    </form-row>
    <form-row>
      <text-field id="address1" fg_class="col-sm-8" placeholder="Address" rules="required|max:25">Address</text-field>
      <phone-field id="driver_phone" fg_class="col-sm-4" rules="phone">Phone</phone-field>
    </form-row>
    <form-row>
      <type-ahead-field id="city" fg_class="col-sm-6" :suggestions="getArrayOfBCCityNames" rules="required|max:15">City</type-ahead-field>
      <province-field id="province" fg_class="col-sm-2">Prov / State</province-field>
      <text-field id="postal" fg_class="col-sm-4">Postal / Zip</text-field>
    </form-row>
  </div>
</form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";
export default {
  name: "DriversInformationCard",
  mixins: [CardsCommon],
}
</script>

<style scoped>

</style>