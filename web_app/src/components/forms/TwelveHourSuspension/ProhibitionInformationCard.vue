<template>
<form-card title="Prohibition">
  <div>
    <form-row>
      <radio-field id="prohibition_type_12hr" fg_class="col-sm-6" rules="required"
                   :options='["Alcohol 90.3(2)", "Drugs 90.3(2.1)"]'>Type of Prohibition (select one)</radio-field>
    </form-row>
    <form-row>
      <text-field id="offence_address" fg_class="col-sm-8">Intersection or Address of Offence</text-field>
      <type-ahead-field id="offence_city" fg_class="col-sm-4" :suggestions="getArrayOfBCCityNames" :rules="offenceCityRules">City</type-ahead-field>
    </form-row>
    <form-row>
      <text-field id="file_number" fg_class="col-sm-3" rules="required">Agency File Number</text-field>
      <date-time id="prohibition_start_time" fg_class="col-sm-9" rules="required">
        Date/Time of Driving, care or control
      </date-time>
    </form-row>
  </div>
</form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";

export default {
  name: "ProhibitionInformationCard",
  mixins: [CardsCommon]
}
</script>

<style scoped>

</style>