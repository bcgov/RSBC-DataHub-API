<template>
<form-card title="Reasonable Grounds">
    <div>
      <shadow-box>
        <form-row>
          <text-field id="offence_address" fg_class="col-sm-8" rules="required|max:22">Intersection or Address of Offence</text-field>
          <type-ahead-field id="offence_city" fg_class="col-sm-4"
                            :suggestions="getArrayOfBCCityNames"
                            :rules="offenceCityRules">City
          </type-ahead-field>
        </form-row>
        <form-row>
          <date-field id="prohibition_start_date" fg_class="col-sm-5"
                      rules="required|validDt|notFutureDt|notGtYearAgo">
            Date of Driving, care or control
          </date-field>
          <time-field id="prohibition_start_time" fg_class="col-sm-4"
                      rules="required|validTime|notFutureDateTime:@prohibition_start_date">
            Time
          </time-field>
        </form-row>
      </shadow-box>
      <shadow-box>
        <p>3, 7  or 30 Day Impoundment <span class="text-muted">In accordance
          with Section 215.46 and 253 of the Motor Vehicle Act</span>
        </p>
        <form-row>
          <in-line-check-box id="impound_duration_3" fg_class="col-sm-2" :option=true>
          3-Day
          </in-line-check-box>
          <in-line-check-box id="impound_duration_7" fg_class="col-sm-2" :option=true>
            7-Day
          </in-line-check-box>
          <in-line-check-box id="impound_duration_30" fg_class="col-sm-2" :option=true>
            30-Day
          </in-line-check-box>
          <text-field id="ipr_number" fg_class="col-sm-6" v-if="isIRP">IRP Number</text-field>
        </form-row>
      </shadow-box>
      <shadow-box>
        <p>7-Day Impoundment for the following reason(s)
            <span class="text-muted">Section 251 and 253 of the Motor Vehicle Act</span>
        </p>
        <form-row>
          <in-line-check-box id="reason_excessive_speed" :option="true">Excessive Speed
            <span class='text-muted'>- Committing an offence under section 148 of the Motor Vehicle Act</span>
          </in-line-check-box>
        </form-row>
        <form-row>
          <in-line-check-box id="reason_prohibited" :option="true">Prohibited
            <span class='text-muted'>- Driving while prohibited under the Motor Vehicle Act,
                "Criminal Code, Youth Justice Act or Youth Criminal Justice Act (Canada).</span>
          </in-line-check-box>
        </form-row>
        <form-row>
          <in-line-check-box id="reason_suspended" :option="true">Suspended
            <span class='text-muted'>- Driving while suspended under section 89 or section
                232 of the Motor Vehicle Act.</span>
          </in-line-check-box>
        </form-row>
        <form-row>
          <in-line-check-box id="reason_racing" :option="true">Street Racing
            <span class='text-muted'>- Driving or operating a motor vehicle in a race as
                defined in the Motor Vehicle Act and the officer intends to charge with an offence.</span>
          </in-line-check-box>
        </form-row>
        <form-row>
          <in-line-check-box id="reason_stunt" :option="true">Stunt Driving
            <span class='text-muted'>- Driving or operating a motor vehicle in a stunt as
                defined in the Motor Vehicle Act and the officer intends to charge with an offence.</span>
          </in-line-check-box>
        </form-row>
        <form-row>
          <in-line-check-box id="reason_motorcycle_seating" :option="true">Motorcycle (seating)
            <span class='text-muted'>- Committing an offence under section 194 (1)
                or (2) of the Motor Vehicle Act.</span>
          </in-line-check-box>
        </form-row>
        <form-row>
          <in-line-check-box id="reason_motorcycle_restrictions" :option="true">Motorcycle (restrictions)
            <span class='text-muted'>- Committing an offence under section 25(15) of the Motor Vehicle Act
              relating to a restriction or condition of a motorcycle learner or novice driver’s licence.</span>
          </in-line-check-box>
        </form-row>
        <form-row>
          <in-line-check-box id="reason_unlicensed" :option="true">Unlicensed (UL)
            <span class='text-muted'> - Driving without a valid driver’s licence and with a notice on
               the driving record indicating a previous conviction for driving while unlicensed.</span>
          </in-line-check-box>
        </form-row>
        <form-row>
          <text-field v-if="getAttributeValue('reason_unlicensed')" id="ul_prohibition_number" fg_class="col-sm-6">
            UL Prohibition Number
          </text-field>
        </form-row>
        <form-row>
          <radio-field v-if="getAttributeValue('reason_unlicensed')" id="suspected_bc_resident" :options="['Yes', 'No']">
            Does the officer have grounds to believe that the Driver resides in British Columbia? (explain in incident details)
          </radio-field>
        </form-row>
      </shadow-box>
    </div>
</form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";
import InLineCheckBox from "@/components/questions/InLineCheckBox";
import {mapGetters} from "vuex";

export default {
  name: "ReasonableGroundsCard",
  components: {InLineCheckBox},
  mixins: [CardsCommon],
  computed: {
    ...mapGetters(['getAttributeValue']),
    isIRP() {
      return (this.getAttributeValue("impound_duration_3") ||
      this.getAttributeValue("impound_duration_7") ||
          this.getAttributeValue("impound_duration_30"))
    }
  }
}
</script>