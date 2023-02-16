<template>
  <form-card title="Unlicensed Driver">
    <form-row>
      <text-field id="ul_prohibition_number" fg_class="col-sm-2" :path="path" v-mask="'##-#######'">
      UL Prohibition Number
      </text-field>
    </form-row>
    <form-row>
      <radio-field  id="suspected_bc_resident" :options="[['yes', 'Yes'], ['no', 'No']]" :path="path">
        Does the officer have grounds to believe that the Driver resides in British Columbia? (explain in incident details)
      </radio-field>
    </form-row>
  </form-card>
</template>
<script>
  import CardsCommon from "@/components/forms/CardsCommon";
  export default {
    name: "UnlicensedDriverCard",
    mixins: [ CardsCommon ]
  }
</script>