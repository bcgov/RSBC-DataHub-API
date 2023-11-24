<template>
  <div id="end-of-life-banner">
<!-- 
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
          What was supposed to be a small test with only a handful of agencies and RCMP detachments grew into a widescale deployment
          to almost 800 members from every independent agency and dozens of RCMP detachments across British Columbia.
        </p>
        <p class="card-text font-weight-bold mr-4 ml-4 text-dark text-left">
          THANK-YOU for making the Pilot a success!
        </p>
        <div class="card-text h6 mr-4 ml-4 text-muted text-left">Shout-outs</div>
        <p class="card-text h6 mr-4 ml-4 text-muted text-left">
          <ul>
            <li>Mike LEO, Stl'atl'imx Tribal Police Service &mdash; <span class="font-italic">in memoriam</span></li>
            <li>Everybody at CRD IRSU</li>
            <li>Grayson SMITH, Delta Police Department</li>
            <li>Greg SMITH, New Westminster Police Department</li>
            <li>RCMP "E" Division IM+T unit</li>
            <li>Brian SAMPSON, RCMP Integrated Impaired Driving Unit</li>
            <li>Mark BOUCHEY, Vancouver Police Department</li>
            <li>Robert GOUGH, Vancouver Police Department</li>
            <li>Stephen FRANCE, West Vancouver Police Department</li>
          </ul>
        </p>
      </div>
    </div>
-->
<!--
    <div v-else>
-->
      <div class="card bg-light mb-2 ml-5 mr-5 mt-4 pb-2 pt-4" style="border: 4px solid #003366 !important;">
        <span class="font-weight-bold h1 pb-2 pt-2 text-dark">
          Welcome to Digital Forms
        </span>
      </div>
      <div class="card-body mr-5 ml-5">
        <p class="card-text mr-4 ml-4 text-dark text-left">
          In the near future, Digital Forms will be upgraded to support end-to-end <span class="font-weight-bold">data
          submission</span> and electronic <span class="font-weight-bold">certificate of service</span>. This enhancement
          will eliminate the need to manually send copies of the 12-hour, 24-hour or Vehicle Impound documents to ICBC or
          RoadSafetyBC.
        </p>
      </div>
    </div>
<!--
  </div>
-->
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