<template>
  <form-container title="Immediate Roadside Prohibition">
    <form-card title="Vehicle Licence Plate">
      <form-row>
        <province-field id="plate_province" fg_class="col-sm-2">Jurisdiction</province-field>
        <plate-number id="plate_number" fg_class="col-sm-6">Plate Number</plate-number>
      </form-row>
    </form-card>
    <form-card title="Registered Owner">
      <form-row>
        <radio-field id="driver_is_owner" fg_class="col-sm-6" :options='["Yes", "No"]'>Driver is registered owner?</radio-field>
        <text-field v-if="isJurisdictionBC" id="owners_drivers_number">Owner's Licence Number (BC only)</text-field>
      </form-row>
      <form-row>
        <text-field id="owners_last_name" fg_class="col-sm-6">Owner's Last Name</text-field>
        <text-field id="owners_first_name" fg_class="col-sm-6">Owner's First Name</text-field>
      </form-row>
      <form-row>
        <text-field id="owners_address1" fg_class="col-sm-12" placeholder="Address" rules="required">Address Line 1</text-field>
      </form-row>
      <form-row>
        <text-field id="owners_address2" fg_class="col-sm-12" placeholder="Address">Address Line 2</text-field>
      </form-row>
      <form-row>
        <text-field id="owners_city" fg_class="col-sm-4" rules="required">City</text-field>
        <province-field id="owners_province" fg_class="col-sm-2">Province</province-field>
        <text-field id="owners_postal" fg_class="col-sm-2">Postal / Zip</text-field>
        <phone-field id="owners_phone" fg_class="col-sm-4" rules="phone">Phone</phone-field>
      </form-row>
    </form-card>
    <form-card title="Vehicle information">
      <form-row>
        <text-field id="plate_year" fg_class="col-sm-4">Plate Year</text-field>
        <text-field id="plate_val_tag" input_type="number" fg_class="col-sm-4">Plate Val Tag</text-field>
        <text-field id="registration_number" fg_class="col-sm-4">Registration Number</text-field>
      </form-row>
      <form-row>
        <text-field id="vehicle_year" fg_class="col-sm-3">Vehicle Year</text-field>
        <text-field id="vehicle_make" input_type="number" fg_class="col-sm-3">Vehicle Make</text-field>
        <text-field id="vehicle_model" fg_class="col-sm-3">Vehicle Model</text-field>
        <text-field id="vehicle_color" fg_class="col-sm-3">Vehicle Colour</text-field>
      </form-row>
      <form-row>
        <text-field id="puj_code" fg_class="col-sm-5">PUJ Code</text-field>
        <text-field id="nsc_number" fg_class="col-sm-7">NSC Number</text-field>
      </form-row>

    </form-card>

    <form-card title="Driver's Information" v-if="driverIsNotRegisteredOwner">
      <form-row>
        <province-field id="drivers_licence_jurisdiction" fg_class="col-sm-2">Jurisdiction</province-field>
        <driver-licence-number id="drivers_number">Driver's Licence Number</driver-licence-number>
      </form-row>
      <form-row>
        <text-field id="last_name" fg_class="col-sm-4" placeholder="Last Name" rules="required">Last Name</text-field>
        <text-field id="first_name" fg_class="col-sm-4" placeholder="First Name" rules="required">First Name</text-field>
        <dob-field id="dob" fg_class="col-sm-4" rules="dob">Date of Birth</dob-field>
      </form-row>
      <form-row>
        <text-field id="address1" fg_class="col-sm-12" placeholder="Address" rules="required">Address Line 1</text-field>
      </form-row>
      <form-row>
        <text-field id="address2" fg_class="col-sm-12" placeholder="Address">Address Line 2</text-field>
      </form-row>
      <form-row>
        <text-field id="city" fg_class="col-sm-6" rules="required">City</text-field>
        <province-field id="province" fg_class="col-sm-4">Province</province-field>
        <text-field id="postal" fg_class="col-sm-2">Postal / Zip</text-field>
      </form-row>
    </form-card>
    <form-card title="Details">
      <form-row>
        <text-field id="agency" fg_class="col-sm-2">Agency</text-field>
        <text-field id="file_number" fg_class="col-sm-3">File Number</text-field>
        <date-time id="prohibition_start_time" fg_class="col-sm-7">
          Time of driving, care or control
        </date-time>
      </form-row>
    </form-card>
    <form-submission-buttons></form-submission-buttons>
    <print-confirmation-modal id="printConfirmationModal" title="printConfirmation"></print-confirmation-modal>
  </form-container>
</template>

<script>
import FormsCommon from "@/components/forms/FormsCommon";

export default {
  name: "ImmediateRoadsideProhibition",
  mixins: [FormsCommon]
}
</script>