<template>
  <div id="end-of-life-banner">
    <div v-if="retirementAchievementUnlocked">
      <div class="card bg-warning mb-2 ml-5 mr-5 mt-4 pb-2 pt-4" style="border: 4px dashed red !important;">
        <span class="bg-warning font-weight-bold h2 pb-2 pt-2 text-dark">
          <b-icon-star-fill variant="danger" />&nbsp; Digital Forms 2.0 IS HERE!&nbsp;<b-icon-star-fill variant="danger" />
          <br />
          <span class="h4">
          Please connect to the Internet and <a href="."><span style="text-decoration: underline;">reload</span></a> this page.
          </span>
        </span>
      </div>
      <div class="card-body mr-5 ml-5">
        <p class="card-text mr-4 ml-4 text-dark text-left">
          On <span style="color: red;">November 30, 2023</span>, our Pilot application was retired after 20 months of field testing.
          What was supposed to be a small test of only two agencies and three RCMP detachments grew into a widescale deployment to
          over 700 members from every independent agency and dozens of RCMP detachments across British Columbia.
        </p>
        <p class="card-text font-weight-bold mr-4 ml-4 text-dark text-left">
          THANK-YOU for making the Pilot a success!
        </p>
        <div class="card-text h6 mr-4 ml-4 text-muted text-left">Shoutouts</div>
        <p class="card-text h6 mr-4 ml-4 text-muted text-left">
          <ul>
            <li>Bryce PEDERSEN (ret'd), BC Highway Patrol</li>
            <li>Everybody at CRD IRSU</li>
            <li>Grayson SMITH, Delta Police Department</li>
            <li>Greg SMITH, New Westminster Police Department</li>
            <li>RCMP "E" Division IM+T unit</li>
            <li>Brian SAMPSON, RCMP Integrated Imparied Driving Unit</li>
            <li>Robert GOUGH, Vancouver Police Department</li>
          </ul>
        </p>
      </div>
    </div>
    <div v-else>
      <div class="card bg-warning mb-2 ml-5 mr-5 mt-4 pb-2 pt-4" style="border: 4px dashed red !important;">
        <span class="bg-warning font-weight-bold h2 pb-2 pt-2 text-dark">
          <b-icon-exclamation-triangle-fill variant="danger" />&nbsp; {{daysBeforeRetirement}} Days Until SYSTEM RETIREMENT
        </span>
      </div>
      <div class="card-body mr-5 ml-5">
        <p class="card-text mr-4 ml-4 text-dark text-left">
          On <span style="color: red;">November 30, 2023</span>, the Digital Forms system will be upgraded to support end-to-end
          <span class="font-weight-bold">data submission</span> and electronic <span class="font-weight-bold">certificate of
          service</span>. This enhancement will eliminate the need to manually send copies of the 12-hour, 24-hour or Vehicle Impound
          documents to ICBC or RoadSafetyBC.
        </p>
        <p class="card-text font-weight-bold mr-4 ml-4 text-dark">
          <span style="text-decoration: underline;">Reminder About Paper Forms</span>
        </p>
        <p class="card-text mr-4 ml-4 text-dark text-left">
          The new paper 12-hour and 24-hour forms <span style="text-decoration: underline;">must</span> be used starting <span style="color: red;">November 30, 2023 @ 00:00h PST</span>.
          <br />
          Any 12-hour suspension or 24-hour prohibition issued on old paper stock after this date <span class="font-weight-bold">will be DOA</span>.
        </p>
      </div>
    </div>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  name: "EndOfLifeBanner",
  computed: {
    ...mapGetters(["daysBeforeRetirement", "retirementAchievementUnlocked"]),
  }
};
</script>