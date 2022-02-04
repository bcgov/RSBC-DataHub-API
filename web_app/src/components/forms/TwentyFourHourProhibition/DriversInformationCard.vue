<template>
<form-card title="Driver's Information">
    <form-row>
      <driver-licence-number id="drivers_number">Driver's Licence Number</driver-licence-number>
      <jurisdiction-field id="drivers_licence_jurisdiction" fg_class="col-sm-3">Prov / State / International</jurisdiction-field>
    </form-row>
    <form-row>
      <text-field id="last_name" fg_class="col-sm-4" placeholder="Last Name" rules="required|lt25">Last Name</text-field>
      <text-field id="first_name" fg_class="col-sm-4" placeholder="First Name" rules="lt25">First Name</text-field>
      <dob-field id="dob" fg_class="col-sm-4" rules="dob8|dob">Date of Birth</dob-field>
    </form-row>
    <form-row>
      <text-field id="address1" fg_class="col-sm-12" placeholder="Address" rules="required">Address Line 1</text-field>
    </form-row>
    <form-row>
      <type-ahead-field id="city" fg_class="col-sm-6" :suggestions="getArrayOfBCCityNames" rules="required">City</type-ahead-field>
      <province-field id="province" fg_class="col-sm-2" rules="required">Province</province-field>
      <text-field id="postal" fg_class="col-sm-4">Postal / Zip</text-field>
    </form-row>
</form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";
export default {
  name: "DriversInformationCard",
  mixins: [CardsCommon],
}
</script>
