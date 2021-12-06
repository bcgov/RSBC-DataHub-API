<template>
  <div id="app" class="card border-0 ml-4 mr-4">
    <div id="roadsafety-header" class="card-header">
      <div class="d-flex justify-content-between">
        <a href="/"><img width="300px" src="/assets/BCID_RoadSafetyBC_logo_transparent.png" ></a>
        <div class="d-flex align-items-end flex-column">
          <div class="font-weight-bold text-warning">
            DRAFT <span class="text-light small">{{ getAppVersion }}</span>
          </div>

          <div class="mt-auto small">
            <router-link to="/admin" v-if="isUserAnAdmin" class="text-white font-weight-bold">
              <span>Admin</span>
            </router-link>
            <span v-if="! isUserAnAdmin && isUserAuthenticated">User</span> {{ getKeycloakUsername }}
          </div>
        </div>
      </div>

    </div>
    <not-logged-in-banner v-if="isDisplayNotLoggedInBanner"></not-logged-in-banner>
    <div class="card-body">
      <offline-banner v-if="! $store.state.isOnline"></offline-banner>
      <router-view></router-view>
      <debug-component></debug-component>
    </div>
  </div>
</template>

<script>

import {mapGetters} from 'vuex';
import NotLoggedInBanner from "@/components/NotLoggedInBanner";
import OfflineBanner from '@/components/OfflineBanner'
import DebugComponent from "@/components/debugComponent";

export default {
  name: 'App',
  components: {DebugComponent, NotLoggedInBanner, OfflineBanner},
  computed: {
    ...mapGetters(['getAppVersion', "getKeycloakUsername", "isUserAnAdmin", "isUserAuthenticated",
    "isDisplayNotLoggedInBanner"]),
  },

}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  font-size: large;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: lightgray;
  margin-top: 60px;
}

.form-check {
    display: flex;
    align-items: center;
}
.form-check-label {
    margin-left: 10px;
}
.form-check .form-check-input[type=checkbox] {
    border-radius: .25em;
    height: 1.3em;
    width: 1.3em;
}
.form-check .form-check-input[type=radio] {
    border-radius: 25%;
    height: 1.3em;
    width: 1.3em;
}
.form-switch .form-check-input[type=checkbox] {
    border-radius: 1.3em;
    height: 1.3em;
    width: 1.3em;
}

.form-group label {
  font-size: medium;
  color: #343a40;
}

#roadsafety-header {
  background-color: #003366;

}

.row {
  margin: 0.5em 0.5em 0.5em 0.5em;
  padding: 0.5em 0.5em 0.5em 0.5em;
  vertical-align: center;

}

.lightgray {
    background-color: lightgray;
  }
.prohibition_number {
  color: red;
}

</style>
