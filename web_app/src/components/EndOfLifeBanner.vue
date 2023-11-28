<template>
  <div id="end-of-life-banner">

    <!-- <div v-if="retirementAchievementUnlocked">
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
          As of <span style="color: red;">November 30, 2023</span>, our Pilot application has seen over 20 months of field testing.
          What was supposed to be a small test with only a handful of agencies and RCMP detachments grew into a widescale deployment
          to almost 800 members from every independent agency and dozens of RCMP detachments across British Columbia.
        </p>
        <p class="card-text font-weight-bold mr-4 ml-4 text-dark text-left">
          THANK-YOU for making the Pilot a continued success!
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

    <div v-else> -->
      <div class="card bg-light mb-2 ml-5 mr-5 mt-4 pb-2 pt-4" style="border: 4px dashed orange !important;">
        <span class="bg-light font-weight-bold h2 pb-2 pt-2 text-dark">
          <b-icon-exclamation-triangle-fill variant="danger" />&nbsp; {{daysBeforeRetirement}} days until updated 12-hour & 24-hour forms go into effect

        </span>
      </div>
      <div class="card-body mr-5 ml-5">
        <p class="card-text mr-4 ml-4 text-dark text-left">

          On November 30, 2023, the 12-hour and 24-hour forms will be upgraded to include a pre-filled
          <span class="font-weight-bold">certificate of service</span>.
        </p>
        <p class="card-text mr-4 ml-4 text-dark text-left">
          These documents must still be submitted <span class="font-weight-bold">manually</span>: i.e. submission by fax or mail, as appropriate.
        </p>
        <!-- <p class="card-text mr-4 ml-4 text-dark text-left">
          In the near future, Digital Forms will be further upgraded to support end-to-end <span class="font-weight-bold">electronic data submission</span>
          that will eliminate the need to manually send copies of the 12-hour, 24-hour or Vehicle Impound documents to ICBC or RoadSafetyBC.
        </p> -->
        <br />
        <p class="card-text font-weight-bold mr-4 ml-4 text-dark">
          <span style="text-decoration: underline;">Reminder About Paper Forms</span>
        </p>
        <p class="card-text mr-4 ml-4 text-dark h6">
          The new paper 12-hour and 24-hour forms <span style="text-decoration: underline;">must</span> be used starting <span style="color: red;">November 30, 2023 @ 00:00h PST</span>.
          <br />
          Any 12-hour suspension or 24-hour prohibition issued on old paper stock after this date <span class="font-weight-bold">will be DOA</span>.
        </p>
      </div>
    <!-- </div> -->

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