<template>
<form-card title="Reasonable Grounds">
    <div>
      <form-row>
        <text-field id="ipr_number" fg_class="col-sm-6" >IRP Number</text-field>
      </form-row>
      <form-row>
        <radio-field id="impound_duration" fg_class="col-sm-12" :options='["3-Day", "7-Day", "30-Day"]'>
          Impoundment Duration
          <span class="text-muted">(in accordance with section 215.46 and 253 of the Motor Vehicle Act)</span>
        </radio-field>
      </form-row>
      <form-row>
        <rich-check-field id="reasons-seven-day" fg_class="col-sm-12" :options="seven_day_options">
          7-Day Impoundment for the following reason(s)
          <span class="text-muted">Section 251 and 253 of the Motor Vehicle Act</span>
        </rich-check-field>
        <text-field id="ul_prohibition_number" fg_class="col-sm-6">UL Prohibition Number</text-field>
      </form-row>
    </div>
</form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";
import RichCheckField from "@/components/questions/RichCheckField";

export default {
  name: "ReasonableGroundsCard",
  components: {RichCheckField},
  mixins: [CardsCommon],
  computed: {
    seven_day_options() {
      return [
          {
            id: "excessive",
            value: "Excessive Speed <span class='text-muted'>- Committing an offence under section 148 of " +
                "the Motor Vehicle Act</span>"
          },
          {
            id: "prohibited",
            value: "Prohibited <span class='text-muted'>- Driving while prohibited under the Motor Vehicle Act, " +
                "Criminal Code, Youth Justice Act or Youth Criminal Justice Act (Canada).</span>"
          },
          {
            id: "suspended",
            value: "Suspended <span class='text-muted'>- Driving while suspended under section 89 or section " +
                "232 of the Motor Vehicle Act.</span>"
          },
          {
            id: "racing",
            value: "Street Racing <span class='text-muted'>- Driving or operating a motor vehicle in a race as " +
                "defined in the Motor Vehicle Act and the officer intends to charge with an offence.</span>"
          },
          {
            id: "stunt",
            value: "Stunt Driving <span class='text-muted'>- Driving or operating a motor vehicle in a stunt as " +
                "defined in the Motor Vehicle Act and the officer intends to charge with an offence.</span>"
          },
          {
            id: "motorcycle-seating",
            value: "Motorcycle (seating) <span class='text-muted'>- Committing an offence under section 194 (1) " +
                "or (2) of the Motor Vehicle Act.</span>"
          },
          {
            id: "motorcycle-restrictions",
            value: "Motorcycle (restrictions) <span class='text-muted'>- Committing an offence under section " +
                "25(15) of the Motor Vehicle Act relating to a restriction or condition of a motorcycle learner " +
                "or novice driver’s licence.</span>"
          },
          {
            id: "unlicensed",
            value: "Unlicensed (UL) <span class='text-muted'> - Driving without a valid driver’s licence and with " +
                "a notice on the driving record indicating a previous conviction for driving while unlicensed</span>"
          },
      ]
    }
  }
}
</script>