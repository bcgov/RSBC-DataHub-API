<template>
  <div class="alert alert-secondary mt-3 small" v-if="updateExists">
    Good news, a new version of the roadside-forms web app is available.
    <div class="btn btn-secondary btn-sm" @click="refreshApp">Update</div>
  </div>
</template>

<script>
import update from "@/helpers/update";
export default {
  mixins: [update],
  name: "UpdateAvailableBanner"
}
</script>