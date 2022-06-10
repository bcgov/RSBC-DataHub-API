<template>
  <form-card title="Excessive Speed">
    <form-row >
      <text-field id="speed_limit" :path="path" input_type="number" rules="required" fg_class="col-sm-3">Speed Limit (km/h)</text-field>
    </form-row>
    <form-row>
      <text-field id="vehicle_speed" :path="path" input_type="number" rules="required" fg_class="col-sm-3">Vehicle Speed (km/h)</text-field>
    </form-row>
    <form-row>
      <radio-field id="speed_estimated" :path="path" fg_class="col-sm-12" :options='[["visual", "Visual"], ["pacing", "Pacing"]]'>
          Vehicle speed estimated by:
      </radio-field>

      <radio-field id="speed_confirmed" :path="path" fg_class="col-sm-12"
                   :options='[["laser", "Laser"], ["radar", "Radar"], ["other", "Other (explain in incident details)"]]'>
          Vehicle speed confirmed by:
      </radio-field>
    </form-row>
  </form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";

export default {
  name: "ExcessiveSpeedCard",
  mixins: [CardsCommon]
}
</script>
