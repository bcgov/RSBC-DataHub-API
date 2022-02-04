<template>
<form-card title="Driver's Information">
    <form-row>
      <jurisdiction-field id="drivers_licence_jurisdiction" fg_class="col-sm-3">Prov / State / International</jurisdiction-field>
      <driver-licence-number id="drivers_number">Driver's Licence Number</driver-licence-number>
    </form-row>
    <form-row>
      <text-field id="last_name" fg_class="col-sm-4" placeholder="Last Name" rules="required|lt25">Last Name</text-field>
      <text-field id="first_name" fg_class="col-sm-4" placeholder="First Name" rules="lt25">First Name</text-field>
      <dob-field id="dob" fg_class="col-sm-4" rules="dob8|dob">Date of Birth</dob-field>
    </form-row>
    <form-row>
      <text-field id="expiry_year" fg_class="col-sm-4" rules="lt5">Expiry Year</text-field>
      <text-field id="driver_gender" fg_class="col-sm-4" rules="lt3">Gender</text-field>
      <text-field id="dl_class" fg_class="col-sm-4" rules="lt3">DL Class</text-field>
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
