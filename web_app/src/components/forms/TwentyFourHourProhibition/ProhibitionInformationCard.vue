<template>
<form-card title="Prohibition">
    <form-row>
      <radio-field id="prohibition_type" :path="path" fg_class="col-sm-6" rules="required"
                   :options='[["alcohol", "Alcohol 215(2)"], ["drugs", "Drugs 215(3)"]]'>Type of Prohibition (select one)</radio-field>
    </form-row>
    <form-row>
      <text-field id="offence_address" :path="path" fg_class="col-sm-8" rules="required">Intersection or Address of Offence</text-field>
      <offence-city :path="path" fg_class="col-sm-4">City</offence-city>
    </form-row>
    <form-row>
      <text-field id="file_number" :path="path" fg_class="col-sm-2" rules="required">Agency File #</text-field>
      <date-field id="prohibition_start_date" :path="path" fg_class="col-sm-5"
                  rules="required|validDt|notFutureDt|notGtYearAgo">
        Date of Driving - care or control
      </date-field>
      <time-field id="prohibition_start_time" :path="path" fg_class="col-sm-5"
                  rules="required|validTime|notFutureDateTime:@prohibition_start_date">
        Time of Driving - care or control
      </time-field>
    </form-row>
</form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";

export default {
  name: "ProhibitionInformationCard",
  mixins: [CardsCommon],
}
</script>

<style scoped>

</style>