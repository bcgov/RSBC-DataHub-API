<template>
  <div>
    <loading-resources v-if=" ! allResourcesLoaded"></loading-resources>
    <user-not-permitted-banner v-if="isDisplayUserNotAuthorizedBanner"></user-not-permitted-banner>
    <welcome-login-card v-if="isDisplayWelcomeLoginCard"></welcome-login-card>
    <issue-prohibitions v-if="isDisplayIssueProhibitions"></issue-prohibitions>
    <recent-prohibitions v-if="isRecentProhibitions && allResourcesLoaded"></recent-prohibitions>
    <feedback-welcome v-if="isDisplayFeedbackBanner"></feedback-welcome>
  </div>
</template>

<script>

import IssueProhibitions from "@/components/IssueProhibitions";
import FeedbackWelcome from "@/components/FeedbackWelcome";
import RecentProhibitions from "@/components/RecentProhibitions";
import UserNotPermittedBanner from "@/components/UserNotPermittedBanner";
import {mapGetters} from "vuex";
import WelcomeLoginCard from "@/components/WelcomeLoginCard";
import LoadingResources from "@/components/loading/LoadingResources";

export default {
  name: "Home",
  components: {
    LoadingResources,
     WelcomeLoginCard,
     UserNotPermittedBanner,
     RecentProhibitions,
     FeedbackWelcome,
     IssueProhibitions
  },
  computed: {
    ...mapGetters([
      "allResourcesLoaded",
      "isUserHasAtLeastOneFormId",
      'isRecentProhibitions',
      'getFormData',
      'isDisplayIssueProhibitions',
      'getCurrentlyEditedFormObject',
      'isDisplayUserNotAuthorizedBanner',
      'isDisplayFeedbackBanner',
      'isDisplaySearchRecentProhibition',
      'isDisplayWelcomeLoginCard'
    ]),
  },
}
</script>

<style scoped>

</style>