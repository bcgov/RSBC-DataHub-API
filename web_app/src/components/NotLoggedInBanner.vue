<template>
    <div id="not-authenticated-banner" class="card-header bg-secondary text-left small pt-1 pb-1">
      <div class="d-flex justify-content-between align-items-center">
        <div><span class="font-weight-bold" id="logged-in-status">Not logged in</span>.
          Driver's licence and vehicle licence plate lookups are not available.
        </div>
        <div>
          <router-link to="/login" class="text-white font-weight-bold">
            <div class="btn btn-primary btn-sm m-0" id="login-button">Login</div>
          </router-link>
        </div>
      </div>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class OfflineBanner extends Vue {

}
</script>