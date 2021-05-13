<template>
  <form-container title="Notice of 24 Hour Licence Suspension">
    <form-card title="Vehicle Licence Plate">
      <form-row>
        <province-field id="plate_province" fg_class="col-sm-2">Jurisdiction</province-field>
        <plate-number id="plate_number" fg_class="col-sm-6">Plate Number</plate-number>
      </form-row>
    </form-card>
    <form-card title="Registered Owner">
      <form-row>
        <radio-field id="driver_is_owner" fg_class="col-sm-6" :options='["Yes", "No"]'>Driver is registered owner?</radio-field>
        <text-field v-if="isPlateJurisdictionBC" id="owners_drivers_number">Owner's Licence Number (BC only)</text-field>
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
      <form-row v-if="isReleasedToOtherDriver">
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
      <form-row>
        <radio-field id="prohibition_type" fg_class="col-sm-6"
                     :options='["Alcohol 215(2)", "Drugs 215(3)"]'>Type of Prohibition</radio-field>
      </form-row>
      <div v-if="isProhibitionTypeSelected">
        <form-row>
          <text-field id="offence_address" fg_class="col-sm-8">Intersection or Address of Offence</text-field>
          <type-ahead-field id="offence_city" fg_class="col-sm-4" :suggestions="getArrayOfBCCityNames" rules="required">City</type-ahead-field>
        </form-row>
        <form-row>
          <radio-field id="operating_grounds" fg_class="col-sm-12"
                       :options='["Witnessed by officer", "Admission by driver", "Independent witness", "Other"]'>
            The driver was operating a motor vehicle or had care and
            control of a motor vehicle for the purposes of MVA section 215(1) based on:
          </radio-field>
        </form-row>
        <form-row v-if="isOperatingGroundsOther">
          <text-field id="operating_ground_other" fg_class="col-sm-12">Other</text-field>
        </form-row>
        <form-row>
          <radio-field id="prescribed_device" fg_class="col-sm-12"
                       :options='["Yes", "Yes, requested by driver",
                       "No, opinion formed the driver was affected by alcohol and/or drugs",
                       "No, refused by driver"]'>Was a prescribed test used to form reasonable grounds?
          </radio-field>
        </form-row>
      </div>
    </form-card>

    <form-card v-if="isPrescribedTestUsed" :title="testAdministeredTitle">
      <shadow-box v-if="isProhibitionTypeAlcohol">
        <form-row>
          <check-field :show_label="false"  id="test_administered" fg_class="col-sm-6"
                       :options='["Alco-Sensor FST (ASD)"]'>Test Administered</check-field>
          <date-field v-if="isProhibitionTypeAlcohol && isTestAdministeredASD" id="asd_expiry_date" fg_class="col-sm-6" rules="notExpired">ASD expiry date</date-field>
          <radio-field v-if="isProhibitionTypeAlcohol && isTestAdministeredASD" id="result_alcohol" fg_class="col-sm-12"
                       :options='["51-99 mg%", "Over 99 mg%"]'>Result</radio-field>
        </form-row>
      </shadow-box>
      <shadow-box v-if="isProhibitionTypeAlcohol && isPrescribedTestUsed">
        <form-row>
          <check-field :show_label="false"  id="test_administered" fg_class="col-sm-6"
                       :options='["Approved Instrument"]'></check-field>
          <check-field v-if="isTestAdministeredApprovedInstrument" id="result_alcohol_approved_instrument" fg_class="col-sm-12"
                       :options='["BAC"]'>Result</check-field>
        </form-row>
      </shadow-box>
      <shadow-box v-if="isProhibitionTypeDrugs">
        <form-row>
          <check-field :show_label="false" id="test_administered" fg_class="col-sm-6"
                       :options='["Approved Drug Screening Equipment"]'>Test Administered
          </check-field>
        </form-row>
        <form-row>
          <check-field v-if="isTestAdministeredADSE" id="positive_adse" fg_class="col-sm-6"
                       :options='["THC", "Cocaine"]'>Result - roadside</check-field>
          <date-time v-if="isTestAdministeredADSE" id="time_of_physical_test_adse" fg_class="col-sm-6">Time of test</date-time>
        </form-row>
      </shadow-box>
      <shadow-box v-if="isProhibitionTypeDrugs && isPrescribedTestUsed">
        <form-row>
          <check-field :show_label="false" id="test_administered" fg_class="col-sm-6"
                       :options='["Prescribed Physical Coordination Test (SFST)"]'>&nbsp;
          </check-field>
          <date-time v-if="isTestAdministeredSFST" id="time_of_physical_test_sfst" fg_class="col-sm-6">Time of test</date-time>
        </form-row>
        <form-row v-if="isTestAdministeredSFST">
          <check-field id="result_drug_sfst" fg_class="col-sm-12"
                       :options='["Ability to drive affected by a drug"]'>Result</check-field>
        </form-row>
      </shadow-box>
      <shadow-box v-if="isProhibitionTypeDrugs && isPrescribedTestUsed">
        <form-row>
          <check-field :show_label="false" id="test_administered" fg_class="col-sm-6"
                       :options='["Prescribed Physical Coordination Test (DRE)"]'>&nbsp;
          </check-field>
        </form-row>
        <form-row v-if="isTestAdministeredDRE">
          <radio-field id="result_dre_affected" fg_class="col-sm-6"
                       :options='["affected", "impaired"]'>Opinion of evaluator</radio-field>
          <date-time id="start_time_of_physical_test_dre" fg_class="col-sm-6">Time of opinion</date-time>
          <text-field id="positive_dre" fg_class="col-sm-12">Notes (expand to 3 lines)</text-field>

        </form-row>
        <form-row v-if="isTestAdministeredDRE">
          <check-field id="result_drug_sfst" fg_class="col-sm-12"
                       :options='["Ability to drive affected by a drug"]'>Result</check-field>
        </form-row>
      </shadow-box>
    </form-card>

    <form-card title="Driver's licence">
      <form-row>
        <radio-field id="licence_surrendered" fg_class="col-sm-12" :options='["Yes", "No"]'>Licence surrendered at roadside?</radio-field>
      </form-row>
      <form-row v-if="isLicenceSurrendered">
        <radio-field id="return_of_licence" fg_class="col-sm-12" :options='["By mail", "Pickup in person"]'>How will licence be returned?</radio-field>
      </form-row>
      <form-row v-if="licencePickupInPerson && isLicenceSurrendered">
        <text-field id="pickup_address" fg_class="col-sm-6">Pickup Address</text-field>
        <type-ahead-field id="pickup_city" fg_class="col-sm-4" :suggestions="getArrayOfBCCityNames" rules="required">Pickup City</type-ahead-field>
      </form-row>
    </form-card>


    <form-card title="Miscellaneous">

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
import CheckField from "@/components/questions/CheckField";

export default {
  name: "TwentyFourHourProhibition",
  components: {CheckField},
  mixins: [FormsCommon],
  computed: {
    ...mapGetters(["getAttributeValue", "isPlateJurisdictionBC", "driverIsNotRegisteredOwner"]),
    showVehicleImpounded() {
      return this.getAttributeValue('vehicle_impounded') === "Yes";
    },
    showVehicleNotImpounded() {
      return this.getAttributeValue('vehicle_impounded') === "No";
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
      return this.getAttributeValue('prescribed_device').substr(0,3) === "Yes";
    },
    isTestAdministeredASD() {
      const root = this.getAttributeValue('test_administered')
      console.log('test_administered', root)
      if (Array.isArray(root)) {
        return root.includes("Alco-Sensor FST (ASD)")
      }
      return false;
    },
    isTestAdministeredApprovedInstrument() {
      const root = this.getAttributeValue('test_administered')
      console.log('test_administered', root)
      if (Array.isArray(root)) {
        return root.includes("Approved Instrument")
      }
      return false;
    },
    isTestAdministeredADSE() {
      const root = this.getAttributeValue('test_administered')
      console.log('test_administered', root)
      if (Array.isArray(root)) {
        return root.includes("Approved Drug Screening Equipment")
      }
      return false;
    },
    isTestAdministeredSFST() {
      const root = this.getAttributeValue('test_administered')
      console.log('test_administered', root)
      if (Array.isArray(root)) {
        return root.includes("Prescribed Physical Coordination Test (SFST)")
      }
      return false;
    },
    isTestAdministeredDRE() {
      const root = this.getAttributeValue('test_administered')
      console.log('test_administered', root)
      if (Array.isArray(root)) {
        return root.includes("Prescribed Physical Coordination Test (DRE)")
      }
      return false;
    },
    isReleasedToOtherDriver() {
      return this.getAttributeValue('reason_for_not_impounding') === "Released to other driver";
    },
    testAdministeredTitle() {
      return "Test Administered - " + this.getAttributeValue('prohibition_type')
    }
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