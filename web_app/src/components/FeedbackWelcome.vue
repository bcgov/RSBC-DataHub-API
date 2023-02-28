<template>
  <div class="card mt-3 bg-light border-light pt-1 pb-1">
    <div class="card-body">
      <p class="card-text text-dark">We welcome your suggestions for how to improve this application.</p>
      <p class="card-text"><small class="text-muted">Contact us at: {{ getRoadSafetyEmailAddress }}</small></p>
    </div>
  </div>
</template>
<script>
  import constants from "@/config/constants";
  export default {
    name: "FeedbackWelcome",
    computed: {
      getRoadSafetyEmailAddress() {
        return constants.ROAD_SAFETY_CONTACT + '@gov.bc.ca'
      }
    }
  }
</script>