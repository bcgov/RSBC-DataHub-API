<template>
<form-card title="Driver's Information">
    <form-row>
      <driver-licence-number id="drivers_number" :path=path fg_class="col-sm-6">Driver's Licence Number</driver-licence-number>
      <jurisdiction-field id="drivers_licence_jurisdiction" fg_class="col-sm-3">Prov / State / International</jurisdiction-field>
    </form-row>
    <form-row>
      <text-field id="last_name" :path="path" fg_class="col-sm-4" rules="required|lt25">Surname</text-field>
      <text-field id="first_name" fg_class="col-sm-5" rules="lt25">Given Names</text-field>
      <dob-field id="dob" fg_class="col-sm-3" rules="dob8|dob">Date of Birth</dob-field>
    </form-row>
    <form-row>
      <gender-field id="driver_gender" fg_class="col-sm-4">Gender</gender-field>
      <text-field id="expiry_year" fg_class="col-sm-4" placeholder="YYYY" rules="bcdlExpiryYear">License Expiry Year</text-field>
      <driver-licence-class v-if="isLicenceJurisdictionBC" id="dl_class" fg_class="col-sm-2">BCDL Class</driver-licence-class>
    </form-row>
</form-card>
</template>

<script>
import {mapGetters} from "vuex";
import CardsCommon from "@/components/forms/CardsCommon";
import DriverLicenceClass from "@/components/questions/DriverLicenceClass";

export default {
  name: "DriversInformationCard",
  components: {DriverLicenceClass},
  mixins: [CardsCommon],
  computed: {
    ...mapGetters(["isLicenceJurisdictionBC"])
  }
}
</script>