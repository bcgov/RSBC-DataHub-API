<template>
  <form-card title="Impoundment for Immediate Roadside Prohibition">
    <form-row>
      <radio-field id="irp" fg_class="col-sm-9" hint_text="In accordance with Section 215.46 and 253 of the Motor Vehicle Act" :options='[["yes", "Yes"], ["no", "No"]]' :path="path" rules="required">
        Was an IRP issued as part of this vehicular impound?
      </radio-field>
    </form-row>
    <div v-if="getAttributeValue(path, 'irp_yes')">
      <form-row>
        <radio-field id="duration" fg_class="col-sm-12" :options='[["3-day", "3-Day IRP"], ["7-day", "7-Day IRP"], ["30-day", "30-Day IRP"], ["90-day", "90-day IRP"]]' :path="path + '/irp_yes'" rules="required">
          IRP Duration
        </radio-field>
      </form-row>
      <form-row>
        <div class="col-sm-12">
          Vehicle
          <span v-if="getAttributeValue(path + '/irp_yes', 'duration_3-day')" >may be (at officer's discretion)</span>
          <span v-else-if="getAttributeValue(path + '/irp_yes', 'duration_7-day')">may be (at officer's discretion)</span>
          <span v-else-if="getAttributeValue(path + '/irp_yes', 'duration_30-day') || getAttributeValue(path + '/irp_yes', 'duration_90-day')" class="font-weight-bold text-danger">must be</span>
          impounded for
          <p class="p-1 mt-2 bg-light rounded">
          <span class="prohibition_number" id="impoundment_length">
            <span v-if="getAttributeValue(path + '/irp_yes', 'duration_3-day')">3</span>
            <span v-else-if="getAttributeValue(path + '/irp_yes', 'duration_7-day')">7</span>
            <span v-else-if="getAttributeValue(path + '/irp_yes', 'duration_30-day') || getAttributeValue(path + '/irp_yes', 'duration_90-day')">30</span>
            <span v-else>0</span>
          </span> days
          </p>
        </div>
      </form-row>
      <form-row>
        <text-field id="ipr_number" fg_class="col-sm-6" :path="path + '/irp_yes'" v-mask="'##-#######'">IRP Number</text-field>
        <div class="col-sm-6">
          This VI Number <span class="small muted">(repeated here for your records)</span>
          <p class="p-1 mt-2 bg-light rounded">
            <span class="prohibition_number">{{ getDashedFormNumber }}<check-digit :form_object="form_object"></check-digit></span>
          </p>
        </div>
      </form-row>
    </div>
  </form-card>
</template>
<script>
  import CardsCommon from "@/components/forms/CardsCommon";
  import CheckDigit from "@/components/forms/CheckDigit";
  import { mapGetters } from 'vuex'
  export default {
    name: "ImmediateRoadsideProhibition",
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
      },
      // rootPath() {
      //   return this.path.replace("/data", "");
      // }
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