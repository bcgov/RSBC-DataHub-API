<template>
  <div id="not-authenticated-banner" class="card-header bg-secondary text-left small pt-1 pb-1">
    <div class="d-flex justify-content-between align-items-center">
      <div>
        <span class="font-weight-bold h4" id="logged-in-status"><b-icon-exclamation-triangle-fill variant="warning"></b-icon-exclamation-triangle-fill>&nbsp; Not signed in!</span>
        &nbsp;
        <span class="h5">Driver's licence and vehicle licence plate lookups are not available.</span>
      </div>
      <div>
        <router-link to="/login">
          <div class="btn btn-warning btn-lg m-1 text-dark font-weight-bold" id="login-button">SIGN IN</div>
        </router-link>
      </div>
    </div>
  </div>
</template>
<script>
  import { mapGetters } from "vuex";
  export default {
    name: "offline-banner",
    computed: {
      ...mapGetters([
        'isUserAuthenticated'
      ])
    }
  }
</script>