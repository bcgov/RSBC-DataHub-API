<template>
  <form-card title="Impoundment for Driving Behaviour">
      <div>
        <p>7-Day Impoundment for the following reason(s):</p>
        <form-row>
          <in-line-check-box id="reason_excessive_speed" :option="true" :path=path>Excessive Speed
            <span class='text-muted'>- Committing an offence under section 148 of the Motor Vehicle Act</span>
          </in-line-check-box>
        </form-row>
        <form-row>
          <in-line-check-box id="reason_prohibited" :option="true" :path=path>Prohibited
            <span class='text-muted'>- Driving while prohibited under the Motor Vehicle Act,
                "Criminal Code, Youth Justice Act or Youth Criminal Justice Act (Canada).</span>
          </in-line-check-box>
        </form-row>
        <form-row>
          <in-line-check-box id="reason_suspended" :option="true" :path=path>Suspended
            <span class='text-muted'>- Driving while suspended under section 89 or section
                232 of the Motor Vehicle Act.</span>
          </in-line-check-box>
        </form-row>
        <form-row>
          <in-line-check-box id="reason_racing" :option="true" :path=path>Street Racing
            <span class='text-muted'>- Driving or operating a motor vehicle in a race as
                defined in the Motor Vehicle Act and the officer intends to charge with an offence.</span>
          </in-line-check-box>
        </form-row>
        <form-row>
          <in-line-check-box id="reason_stunt" :option="true" :path=path>Stunt Driving
            <span class='text-muted'>- Driving or operating a motor vehicle in a stunt as
                defined in the Motor Vehicle Act and the officer intends to charge with an offence.</span>
          </in-line-check-box>
        </form-row>
        <form-row>
          <in-line-check-box id="reason_motorcycle_seating" :option="true" :path=path>Motorcycle (seating)
            <span class='text-muted'>- Committing an offence under section 194 (1)
                or (2) of the Motor Vehicle Act.</span>
          </in-line-check-box>
        </form-row>
        <form-row>
          <in-line-check-box id="reason_motorcycle_restrictions" :option="true" :path=path>Motorcycle (restrictions)
            <span class='text-muted'>- Committing an offence under section 25(15) of the Motor Vehicle Act
              relating to a restriction or condition of a motorcycle learner or novice driver’s licence.</span>
          </in-line-check-box>
        </form-row>
        <form-row>
          <in-line-check-box id="reason_unlicensed" :option="true" :path=path>Unlicensed (UL)
            <span class='text-muted'> - Driving without a valid driver’s licence and with a notice on
              the driving record indicating a previous conviction for driving while unlicensed.</span>
          </in-line-check-box>
        </form-row>
      </div>
  </form-card>
</template>
<script>
  import CardsCommon from "@/components/forms/CardsCommon";
  import InLineCheckBox from "@/components/questions/InLineCheckBox";
  export default {
    name: "SevenDayImpoundCard",
    components: { InLineCheckBox },
    mixins: [ CardsCommon ]
  }
</script>