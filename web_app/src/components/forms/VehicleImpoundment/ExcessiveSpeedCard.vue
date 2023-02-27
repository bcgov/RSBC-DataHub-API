<template>
  <form-card title="Excessive Speed">
    <form-row>
      <text-field id="speed_limit" fg_class="col-sm-2" input_type="number" :path="path" rules="required" v-mask="'###'">Speed Limit (km/h)</text-field>
    </form-row>
    <form-row>
      <text-field id="vehicle_speed" fg_class="col-sm-2" input_type="number" :path="path" rules="required|excessiveSpeed:@speed_limit" v-mask="'###'">Vehicle Speed (km/h)</text-field>
    </form-row>
    <form-row>
      <radio-field id="speed_estimated" fg_class="col-sm-12" :options='[["visual", "Visual"], ["pacing", "Pacing"]]' :path="path">Vehicle speed estimated by:</radio-field>
      <radio-field id="speed_confirmed" fg_class="col-sm-12" :options='[["laser", "Laser"], ["radar", "Radar"], ["other", "Other (explain in incident details)"]]' :path="path">Vehicle speed confirmed by:</radio-field>
    </form-row>
  </form-card>
</template>
<script>
  import CardsCommon from "@/components/forms/CardsCommon";
  export default {
    name: "ExcessiveSpeedCard",
    mixins: [ CardsCommon ]
  }
</script>