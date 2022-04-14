<template>
  <form-card title="Excessive Speed">
    <form-row >
      <text-field id="speed_limit" rules="required" fg_class="col-sm-3">Speed Limit</text-field>
      <text-field id="vehicle_speed" rules="required" fg_class="col-sm-9">Vehicle Speed</text-field>
    </form-row>
    <form-row>
      <radio-field id="speed_estimated" fg_class="col-sm-12" :options='["Visual", "Pacing"]'>
          Vehicle speed estimated by:
      </radio-field>

      <radio-field id="speed_confirmed" fg_class="col-sm-12"
                   :options='["Laser", "Radar", "Other (explain in incident details)"]'>
          Vehicle speed estimated by:
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
