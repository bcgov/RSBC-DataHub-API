<template>
  <div class="card mb-3">
    <div class="card-body">
        <div class="row small alert text-dark py-0 my-0">
        <div class="col-1 my-0">
          <b-spinner v-if="!allResourcesLoaded" small></b-spinner>
        </div>
        <div class="col-11 text-left">Loading resources ...</div>
      </div>
    </div>
  </div>
</template>
<script>
  import { mapGetters } from "vuex";
  export default {
    name: "LoadingResources",
    computed: {
      ...mapGetters([
        "allResourcesLoaded"
      ])
    }
  }
</script>