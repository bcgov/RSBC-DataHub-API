<template>
    <div class="card-header bg-secondary text-left small pt-1 pb-1">
      <div class="d-flex justify-content-between align-items-center">
        <div><span class="font-weight-bold">Not logged in</span>.
          Driver's licence and vehicle licence plate lookups are not available.
        </div>
        <div>
          <router-link to="/login" class="text-white font-weight-bold">
            <div class="btn btn-primary btn-sm m-0">Login</div>
          </router-link>
        </div>
      </div>

    </div>
</template>

<script>


import {mapGetters} from "vuex";

export default {
  name: "offline-banner",
  computed: {
    ...mapGetters(['isUserAuthenticated'])
  }
}
</script>