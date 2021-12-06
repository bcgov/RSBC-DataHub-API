<template>
  <div class="card mt-3 bg-light border-light pt-1 pb-1">
      <div class="card-body">
        <p class="card-text text-dark">We'd welcome your suggestions for how to improve this app.</p>
        <p class="card-text"><small class="text-muted">Contact us at: {{ getRoadSafetyEmailAddress }}</small></p>
      </div>
  </div>
</template>

<script>

import {mapGetters} from "vuex";

export default {
  name: "FeedbackWelcome",
  computed: {
    ...mapGetters(["getRoadSafetyEmailAddress"])
  }
}
</script>