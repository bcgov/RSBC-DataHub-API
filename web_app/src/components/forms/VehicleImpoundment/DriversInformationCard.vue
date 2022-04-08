<template>
<form-card title="Driver's Information">
    <form-row>
      <driver-licence-number id="drivers_number">Driver's Licence Number</driver-licence-number>
      <jurisdiction-field id="drivers_licence_jurisdiction" fg_class="col-sm-3">Prov / State / International</jurisdiction-field>
    </form-row>
    <form-row>
      <text-field id="last_name" fg_class="col-sm-4" rules="required|lt25">Surname</text-field>
      <text-field id="first_name" fg_class="col-sm-4" rules="lt25">Given Names</text-field>
      <dob-field id="dob" fg_class="col-sm-4" rules="dob8|dob">Date of Birth</dob-field>
    </form-row>
    <form-row>
      <gender-field id="driver_gender" fg_class="col-sm-4">Gender</gender-field>
      <text-field id="expiry_year" fg_class="col-sm-4" placeholder="YYYY" rules="bcdlExpiryYear">License Expiry Year</text-field>
      <text-field v-if="isLicenceJurisdictionBC" id="dl_class" fg_class="col-sm-4" rules="lt3">BCDL Class</text-field>
    </form-row>
</form-card>
</template>

<script>
import {mapGetters} from "vuex";
import CardsCommon from "@/components/forms/CardsCommon";

export default {
  name: "DriversInformationCard",
  mixins: [CardsCommon],
  computed: {
    ...mapGetters(["isLicenceJurisdictionBC"])
  }
}
</script>