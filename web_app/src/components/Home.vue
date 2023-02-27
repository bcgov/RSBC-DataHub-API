<template>
  <div>
    <loading-resources v-if="!allResourcesLoaded"></loading-resources>
    <user-not-permitted-banner v-if="isDisplayUserNotAuthorizedBanner"></user-not-permitted-banner>
    <welcome-login-card v-if="isDisplayWelcomeLoginCard"></welcome-login-card>
    <issue-prohibitions v-if="isDisplayIssueProhibitions"></issue-prohibitions>
    <recent-prohibitions v-if="isRecentProhibitions && allResourcesLoaded"></recent-prohibitions>
    <feedback-welcome v-if="isDisplayFeedbackBanner"></feedback-welcome>
  </div>
</template>
<script>
import FeedbackWelcome from "@/components/FeedbackWelcome";
import IssueProhibitions from "@/components/IssueProhibitions";
import LoadingResources from "@/components/loading/LoadingResources";
import RecentProhibitions from "@/components/RecentProhibitions";
import UserNotPermittedBanner from "@/components/UserNotPermittedBanner";
import WelcomeLoginCard from "@/components/WelcomeLoginCard";
import { mapGetters } from "vuex";
export default {
  name: "Home",
  components: {
    FeedbackWelcome,
    IssueProhibitions,
    LoadingResources,
    RecentProhibitions,
    UserNotPermittedBanner,
    WelcomeLoginCard
  },
  computed: {
    ...mapGetters([
      "allResourcesLoaded",
      "isUserHasAtLeastOneFormId",
      'getCurrentlyEditedFormObject',
      'getFormData',
      'isDisplayFeedbackBanner',
      'isDisplayIssueProhibitions',
      'isDisplaySearchRecentProhibition',
      'isDisplayUserNotAuthorizedBanner',
      'isDisplayWelcomeLoginCard',
      'isRecentProhibitions'
    ]),
  },
}
</script>