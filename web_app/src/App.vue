<template>
  <div id="app" class="container">
    <div class="row">
      <div id="header" class="card w-100">
          <div class="card-title">
            <div class="d-flex flex-row pt-3 pl-3 pr-3">
              <img width="300px" src="@/assets/BCID_RoadSafetyBC_logo_transparent.png" >
            </div>
          </div>
      </div>
    </div>
    <offline-banner v-if="isNetworkOnline"></offline-banner>
    <component v-if="isFormBeingEdited" :data="getCurrentlyEditedForm.data"
               :is="getSelectedFormComponent" :name="getCurrentlyEditedForm.short_name">
    </component>
    <recent-prohibitions v-if="isRecentProhibitions && ! isFormBeingEdited"></recent-prohibitions>
    <issue-prohibitions v-if=" ! isFormBeingEdited"></issue-prohibitions>
    <prohibition-search v-if=" ! isFormBeingEdited"></prohibition-search>
    <feedback-welcome v-if=" ! isFormBeingEdited"></feedback-welcome>


  </div>
</template>

<script>

import OfflineBanner from "./components/OffineBanner.vue"
import IssueProhibitions from "@/components/IssueProhibitions";
import TwelveHourProhibition from "@/components/forms/TwelveHourProhibition";
import TwentyFourHourProhibition from "@/components/forms/TwentyFourHourProhibition";
import ImmediateRoadsideProhibition from "@/components/forms/ImmediateRoadsideProhibition";
import FeedbackWelcome from "@/components/FeedbackWelcome";
import ProhibitionSearch from "@/components/ProhibitionSearch";
import RecentProhibitions from "@/components/RecentProhibitions";
import { mapGetters, mapMutations } from 'vuex';

export default {
  name: 'App',
  components: {
    RecentProhibitions,
    ProhibitionSearch,
    FeedbackWelcome,
    OfflineBanner,
    IssueProhibitions,
    TwelveHourProhibition,
    TwentyFourHourProhibition,
    ImmediateRoadsideProhibition
  },
  computed: {
    ...mapGetters(['isFormBeingEdited',"getSelectedFormComponent","getCurrentlyEditedForm","isRecentProhibitions","isNetworkOnline"]),
  },

  methods: {
    ...mapMutations(["networkOffline","networkBackOnline"])
  },

  // created: function () {
  //     window.addEventListener('offline', this.offline);
  //     window.addEventListener('online', this.online);
  // },
  //
  // destroyed: function () {
  //     window.removeEventListener('offline', this.offline);
  //     window.removeEventListener('online', this.online);
  // }

}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: lightgray;
  margin-top: 60px;
}

#header.card {
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
