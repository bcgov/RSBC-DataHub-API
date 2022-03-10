<template>
  <!-- DISABLED WHILE WE WAIT FOR FORM TO BE ADJUSTED TO INCLUDE PLACE TO PRINT THESE FIELDS -->
  <div v-if="false">
    <form-card title="Driver's Licence Disposition">
      <form-row>
        <radio-field id="licence_surrendered" fg_class="col-sm-12" :options='["Yes", "No"]'>Licence surrendered at roadside?</radio-field>
      </form-row>
      <form-row v-if="isLicenceSurrendered">
        <radio-field id="return_of_licence" fg_class="col-sm-12" :options='["By mail", "Pickup in person"]'>How will licence be returned?</radio-field>
      </form-row>
      <form-row v-if="licencePickupInPerson && isLicenceSurrendered">
        <type-ahead-field id="pickup_address" :suggestions="getArrayOfPickupLocations" fg_class="col-sm-6">
          Pickup address and city
        </type-ahead-field>
      </form-row>
    </form-card>
  </div>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";
import {mapGetters} from "vuex";

export default {
  name: "ReturnOfLicenceCard",
  mixins: [CardsCommon],
  computed: {
    ...mapGetters(["getArrayOfPickupLocations"]),
    licencePickupInPerson() {
      return this.getAttributeValue('return_of_licence') === "Pickup in person";
    },
    isLicenceSurrendered() {
      return this.getAttributeValue('licence_surrendered') === "Yes";
    }
  }
}
</script>

<style scoped>

</style>