<template>
  <div id="end-of-life-banner">
    <div class="card bg-light mb-2 ml-5 mr-5 mt-4 pb-2 pt-4" style="border: 4px solid #003366 !important;">
      <span class="font-weight-bold h1 pb-2 pt-2 text-dark">
        Welcome to Digital Forms
      </span>
    </div>      
    <div class="card-body mr-5 ml-5">
      <p class="card-text mr-4 ml-4 text-dark text-left">
        In the near future, Digital Forms will be upgraded to support end-to-end <span class="font-weight-bold">data
        submission</span>. This enhancement will eliminate the need to manually send copies of the 12-hour, 24-hour
        or Vehicle Impound documents to ICBC or RoadSafetyBC/Superintendent of Motor Vehicles.
      </p>
    </div>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  name: "EndOfLifeBanner",
  computed: {
    ...mapGetters(["daysBeforeRetirement", "retirementAchievementUnlocked"]),
  }
};
</script>