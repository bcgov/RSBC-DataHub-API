<template>
  <form-container title="Notice of 12 Hour Licence Suspension">
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
        <type-ahead-field id="owners_city" fg_class="col-sm-4" :suggestions="getArrayOfBCCityNames" rules="required">City</type-ahead-field>
        <province-field id="owners_province" fg_class="col-sm-2">Province</province-field>
        <text-field id="owners_postal" fg_class="col-sm-2">Postal</text-field>
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
        <type-ahead-field id="city" fg_class="col-sm-6" :suggestions="getArrayOfBCCityNames" rules="required">City</type-ahead-field>
        <province-field id="province" fg_class="col-sm-4">Province</province-field>
        <text-field id="postal" fg_class="col-sm-2">Postal</text-field>
      </form-row>
    </form-card>
    <form-card title="Vehicle Impoundment or Disposition">
      <form-row>
        <radio-field id="vehicle_impounded" fg_class="col-sm-6" :options='["Yes", "No"]'>Vehicle Impounded?</radio-field>
      </form-row>
      <form-row>
        <radio-field id="reason_for_not_impounding" fg_class="col-sm-6"
                     :options='["Released to other driver", "Left at roadside", "Private tow", "Seized for investigation"]'
                     :visible="showVehicleNotImpounded">Reason for not impounding?</radio-field>
      </form-row>
      <form-row>
        <text-field id="vehicle_released_to" :visible="showVehicleNotImpounded" fg_class="col-sm-6" >
          Vehicle Released To</text-field>
        <date-time id="datetime_released" :visible="showVehicleNotImpounded" fg_class="col-sm-6" >
          Date and Time Released</date-time>
      </form-row>
      <form-row>
        <radio-field id="location_of_keys" :visible="showVehicleImpounded" fg_class="col-sm-6"
                     :options='["With vehicle", "With driver"]'>Location of Keys?</radio-field>
      </form-row>
      <form-row>
        <type-ahead-field id="impound_lot_operator" fg_class="col-sm-12" :visible="showVehicleImpounded"
                          :suggestions="['Busters Towing', 'Roadway Towing - Delta']">Impound Lot Operator</type-ahead-field>
      </form-row>
      <form-row>
        <text-field id="ilo_address" :visible="showVehicleImpounded" fg_class="col-sm-4">Address</text-field>
        <text-field id="ilo_city" :visible="showVehicleImpounded" fg_class="col-sm-4">City</text-field>
        <text-field id="ilo_phone" :visible="showVehicleImpounded" fg_class="col-sm-4">Phone</text-field>
      </form-row>
    </form-card>
    <form-card title="Prohibition">

      <div><!-- TODO / INCOMPLETE --></div>

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
import {mapGetters} from "vuex";

export default {
  name: "TwelveTwentyFour",
  mixins: [FormsCommon],
  computed: {
    ...mapGetters(["getAttributeValue"]),
    showVehicleImpounded() {
      return this.getAttributeValue('vehicle_impounded') === "Yes";
    },
    showVehicleNotImpounded() {
      return this.getAttributeValue('vehicle_impounded') === "No";
    },
    driverIsNotRegisteredOwner() {
      return this.getAttributeValue('driver_is_owner') === "No";
    },
    licencePickupInPerson() {
      return this.getAttributeValue('return_of_licence') === "Pickup in person";
    },
    isLicenceSurrendered() {
      return this.getAttributeValue('licence_surrendered') === "Yes";
    },
    isProhibitionTypeSelected() {
      return this.getAttributeValue('prohibition_type').length > 0;
    },
    isProhibitionTypeDrugs() {
      return this.getAttributeValue('prohibition_type') === "Drugs 215(3)";
    },
    isProhibitionTypeAlcohol() {
      return this.getAttributeValue('prohibition_type') === "Alcohol 215(2)";
    },
    isOperatingGroundsOther() {
      return this.getAttributeValue('operating_grounds') === "Other";
    },
    isPrescribedTestUsed() {
      return this.getAttributeValue('prescribed_device').substr(0, 3) === "Yes";
    },
    isJurisdictionBC() {
      return this.getAttributeValue('plate_province') === 'BC'
    },
  }
}
</script>

<style scoped>
  .lightgray {
    background-color: lightgray;
  }
  .prohibition_number {
    color: red;
  }
</style>