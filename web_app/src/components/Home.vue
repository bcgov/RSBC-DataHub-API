<template>
  <div>
    <user-not-permitted-banner v-if="isDisplayUserNotAuthorizedBanner"></user-not-permitted-banner>
    <welcome-login-card v-if="isDisplayWelcomeLoginCard"></welcome-login-card>
    <issue-prohibitions v-if="isDisplayIssueProhibitions"></issue-prohibitions>
    <recent-prohibitions v-if="isRecentProhibitions"></recent-prohibitions>
    <prohibition-search v-if="isDisplaySearchRecentProhibition"></prohibition-search>
    <feedback-welcome v-if="isDisplayFeedbackBanner"></feedback-welcome>
  </div>
</template>

<script>

import IssueProhibitions from "@/components/IssueProhibitions";
import FeedbackWelcome from "@/components/FeedbackWelcome";
import ProhibitionSearch from "@/components/ProhibitionSearch";
import RecentProhibitions from "@/components/RecentProhibitions";
import UserNotPermittedBanner from "@/components/UserNotPermittedBanner";
import {mapGetters} from "vuex";
import WelcomeLoginCard from "@/components/WelcomeLoginCard";

export default {
  name: "Home",
  components: {
     WelcomeLoginCard,
     UserNotPermittedBanner,
     RecentProhibitions,
     ProhibitionSearch,
     FeedbackWelcome,
     IssueProhibitions
  },
  computed: {
    ...mapGetters([
        "isUserHasAtLeastOneFormId",
        "getArrayOfCommonCarColors",
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