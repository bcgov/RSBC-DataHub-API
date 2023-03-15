<template>
  <div class="card-header bg-danger pt-2 pb-2">
    <div class="d-flex justify-content-between align-items-center">
      <div>
        &nbsp;
      </div>
      <div class="text-white">
        <span class="font-weight-bold h4" id="logged-in-status"><b-icon-exclamation-triangle-fill variant="warning" />&nbsp; <span style="text-decoration: underline;">You are not signed in!12</span></span>
        &nbsp;
        <span class="h5">Driver's licence and plate lookups will be unavailable.</span>
      </div>
      <div>
        <b-icon icon="arrow-right" animation="cylon" scale="2.5" variant="white"></b-icon> &nbsp; &nbsp;
        <router-link to="/login">
          <div class="btn btn-warning m-1 text-dark font-weight-bold" id="login-button">Sign In</div>
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