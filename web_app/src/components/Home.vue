<template>
  <div>
    <loading-resources v-if=" ! allResourcesLoadedInfo"></loading-resources>
    <user-not-permitted-banner v-if="isDisplayUserNotAuthorizedBannerInfo"></user-not-permitted-banner>
    <welcome-login-card v-if="isDisplayWelcomeLoginCardInfo"></welcome-login-card>
    <issue-prohibitions v-if="isDisplayIssueProhibitionsInfo"></issue-prohibitions>
    <!-- <recent-prohibitions v-if="isRecentProhibitions() && allResourcesLoadedInfo"></recent-prohibitions> -->
    <feedback-welcome v-if="isDisplayFeedbackBannerInfo"></feedback-welcome>
  </div>
</template>

<script>

import IssueProhibitions from "@/components/IssueProhibitions";
import FeedbackWelcome from "@/components/FeedbackWelcome";
// import RecentProhibitions from "@/components/RecentProhibitions";
import UserNotPermittedBanner from "@/components/UserNotPermittedBanner";
import {mapGetters} from "vuex";
import WelcomeLoginCard from "@/components/WelcomeLoginCard";
import LoadingResources from "@/components/loading/LoadingResources";

import {allResourcesLoaded, isDisplayUserNotAuthorizedBanner, isDisplayIssueProhibitions, isDisplayFeedbackBanner, isDisplayWelcomeLoginCard} from "@/utils/display"

export default {
  name: "Home",
  components: {
    LoadingResources,
     WelcomeLoginCard,
     UserNotPermittedBanner,
    //  RecentProhibitions,
     FeedbackWelcome,
     IssueProhibitions
  },
  computed: {
    isDisplayUserNotAuthorizedBannerInfo(){
      return isDisplayUserNotAuthorizedBanner()
    },
    isDisplayIssueProhibitionsInfo(){
      return isDisplayIssueProhibitions()
    },
    isDisplayFeedbackBannerInfo(){
      return isDisplayFeedbackBanner()
    },
    isDisplayWelcomeLoginCardInfo(){
      return isDisplayWelcomeLoginCard()
    },
    allResourcesLoadedInfo(){
      return allResourcesLoaded()
    }
    // ...mapGetters([
      // "allResourcesLoaded",
      // "isUserHasAtLeastOneFormId",
      // 'isRecentProhibitions',
      // 'getFormData',
      // 'isDisplayIssueProhibitions',
      // 'getCurrentlyEditedFormObject',
      // 'isDisplayUserNotAuthorizedBanner',
      // 'isDisplayFeedbackBanner',
      // 'isDisplaySearchRecentProhibition',
      // 'isDisplayWelcomeLoginCard'
    // ]),
  },
  methods: {
    isRecentProhibitions(){
      const state = this.$store.state
      for (const form_type in state.forms) {
          // console.log('form_type', form_type)
          for (const form_object in state.forms[form_type]) {
              if("data" in state.forms[form_type][form_object]) {
                  // the 'data' attribute is added when the form is first edited
                  return true
              }
          }
      }
      return false
    }
  }
}
</script>

<style scoped>

</style>