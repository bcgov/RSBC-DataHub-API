<template>
  <form-card title="Time & Place">
    <div>
      <shadow-box>
        <form-row>
          <text-field id="offence_address" fe_class="uppercase" fg_class="col-sm-8" :path=path rules="required|max:22">Intersection or Address of Offence</text-field>
          <offence-city fg_class="col-sm-4" :path=path>City</offence-city>
        </form-row>
        <form-row>
          <!-- <text-field id="file_number" fg_class="col-sm-3" input_mask="##-#####" :path=path rules="required">Agency File #</text-field> -->
          <text-field id="file_number" fg_class="col-sm-3" :path=path rules="required">Agency File #</text-field>
          <date-field id="prohibition_start_date" fg_class="col-sm-5" :path=path rules="required|validDt|notFutureDt|notGtYearAgo">Date</date-field>
          <time-field id="prohibition_start_time" fg_class="col-sm-4" :path=path rules="required|validTime|notFutureDateTime:@prohibition_start_date">Time</time-field>
        </form-row>
      </shadow-box>
    </div>
  </form-card>
</template>
<script>
  import CardsCommon from "@/components/forms/CardsCommon";
  export default {
    name: "TimeAndPlaceCard",
    mixins: [ CardsCommon ],
  }
</script>