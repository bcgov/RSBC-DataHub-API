<template>
  <form-card title="Driver's Information">
    <form-row>
      <driver-licence-number id="drivers_number" :path=path fg_class="col-sm-6">Driver's Licence Number</driver-licence-number>
      <jurisdiction-field id="drivers_licence_jurisdiction" :path=path fg_class="col-sm-3">Prov / State / International</jurisdiction-field>
    </form-row>
    <form-row>
      <text-field id="last_name" fe_class="uppercase" fg_class="col-sm-4" :path=path rules="required|lt25">Surname</text-field>
      <text-field id="first_name" fe_class="capitalize" fg_class="col-sm-5" :path=path rules="lt25">Given Names</text-field>
      <dob-field id="dob" fg_class="col-sm-3" :path=path rules="dob8|dob">Date of Birth</dob-field>
    </form-row>
    <form-row>
      <gender-field id="driver_gender" fg_class="col-sm-4" :path=path>Gender</gender-field>
      <text-field id="expiry_year" fg_class="col-sm-4" :path=path placeholder="" rules="bcdlExpiryYear" v-mask="'####'">License Expiry Year</text-field>
      <driver-licence-class v-if="isLicenceJurisdictionBC" id="dl_class" fg_class="col-sm-2" :path=path>BCDL Class</driver-licence-class>
    </form-row>
  </form-card>
</template>
<script>
  import CardsCommon from "@/components/forms/CardsCommon";
  import DriverLicenceClass from "@/components/questions/DriverLicenceClass";
  import { mapGetters } from "vuex";
  export default {
    name: "DriversInformationCard",
    components: { DriverLicenceClass },
    computed: {
      ...mapGetters([
        "isLicenceJurisdictionBC"
      ])
    },
    mixins: [ CardsCommon ]
  }
</script>