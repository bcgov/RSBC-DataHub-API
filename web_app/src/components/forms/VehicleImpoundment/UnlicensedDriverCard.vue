<template>
  <form-card title="Unlicensed Driver">
    <form-row>
      <text-field id="ul_prohibition_number" fg_class="col-sm-6" :path="path" v-mask="'##-#######'">UL Prohibition Number</text-field>
      <div class="col-sm-6">
          This VI Number <span class="small muted">(repeated here for your records)</span>
          <p class="p-1 mt-2 bg-light rounded">
            <span class="prohibition_number">{{ getDashedFormNumber }}<check-digit :form_object="form_object"></check-digit></span>
          </p>
        </div>
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
  import CheckDigit from "@/components/forms/CheckDigit";
  import { mapGetters } from 'vuex'
  export default {
    name: "UnlicensedDriverCard",
    components: { CheckDigit },
    computed: {
      ...mapGetters([
        'getCurrentlyEditedFormId',
        'getFormIdCheckDigit'
      ]),
      getDashedFormNumber() {
        let dashedFormNumber = "";
        for (let x = 0; x < this.getCurrentlyEditedFormId.length; x++) {
          (x == 2) ? dashedFormNumber += "-" + this.getCurrentlyEditedFormId[x] : dashedFormNumber += this.getCurrentlyEditedFormId[x];
        }
        return dashedFormNumber;
      }
    },
    mixins: [ CardsCommon ],
    props: {
      form_object: Object
    }
  }
</script>
<style scoped>
  #check-digit {
    background: lightgrey;
    padding: 0 2px 0 2px;
  }
</style>