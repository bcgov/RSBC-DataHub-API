<template>
  <form-card title="Time & Place">
    <div>
      <shadow-box>
        <form-row>
          <text-field id="offence_address" :path=path fg_class="col-sm-8" rules="required|max:22">Intersection or Address of Offence</text-field>
          <offence-city :path=path fg_class="col-sm-4">City</offence-city>
        </form-row>
        <form-row>
          <text-field id="file_number" :path=path fg_class="col-sm-3" rules="required">Agency File #</text-field>
          <date-field id="prohibition_start_date" :path=path fg_class="col-sm-5" rules="required|validDt|notFutureDt|notGtYearAgo">Date of Driving, care or control</date-field>
          <time-field id="prohibition_start_time" :path=path fg_class="col-sm-4" rules="required|validTime|notFutureDateTime:@prohibition_start_date">Time</time-field>
        </form-row>
      </shadow-box>
    </div>
  </form-card>
</template>
<script>
  import CardsCommon from "@/components/forms/CardsCommon";
  export default {
    name: "TimeAndPlaceCard",
    mixins: [CardsCommon],
  }
</script>