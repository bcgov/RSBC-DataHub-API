<template>
  <form-container title="Immediate Roadside Prohibition">
    <form-card title="Driver's Information">
      <form-row>
        <driver-licence-number id="drivers_number">Driver's Licence Number</driver-licence-number>
      </form-row>
      <form-row>
        <text-field id="last_name" fg_class="col-sm-4" placeholder="Last Name" rules="required">Surname</text-field>
        <text-field id="first_name" fg_class="col-sm-4" placeholder="First Name" rules="required">Given Name</text-field>
        <dob-field id="dob" fg_class="col-sm-4" rules="dob">Date of Birth</dob-field>
      </form-row>
      <form-row>
        <text-field id="address1" fg_class="col-sm-12" placeholder="Address" rules="required">Address Line 1</text-field>
      </form-row>
      <form-row>
        <text-field id="address2" fg_class="col-sm-12" placeholder="Address">Address Line 1</text-field>
      </form-row>
      <form-row>
        <type-ahead-field id="city" fg_class="col-sm-6" :suggestions="getArrayOfBCCityNames" rules="required">
          City
        </type-ahead-field>
        <province-field id="province" fg_class="col-sm-4">Province</province-field>
        <text-field id="postal" fg_class="col-sm-2">Postal</text-field>
      </form-row>
      <form-row>
        <phone-field id="phone" fg_class="col-sm-6" rules="phone">Phone</phone-field>
      </form-row>
      <form-submission-buttons></form-submission-buttons>
    </form-card>
  </form-container>
</template>

<script>
import FormsCommon from "@/components/forms/FormsCommon";

export default {
  name: "ImmediateRoadsideProhibition",
  mixins: [FormsCommon]
}
</script>