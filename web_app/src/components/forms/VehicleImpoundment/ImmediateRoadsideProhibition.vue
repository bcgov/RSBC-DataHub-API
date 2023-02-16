<template>
  <form-card title="Impoundment for Immediate Roadside Prohibition">
    <form-row>
      <radio-field id="irp" fg_class="col-sm-9" hint_text="In accordance with Section 215.46 and 253 of the Motor Vehicle Act" :options='[["yes", "Yes"], ["no", "No"]]' :path="path" rules="required">
        Was an IRP issued as part of this vehicular impound?
      </radio-field>
    </form-row>
    <div v-if="getAttributeValue(path, 'irp_yes')">
      <form-row >
        <radio-field id="duration" fg_class="col-sm-6" :options='[["3-day", "3-Day Vehicle Impoundment (Optional for 3-Day IRPs)"], ["7-day", "7-Day Vehicle Impoundment (Optional for 7-Day IRPs)"], ["30-day", "30-Day Vehicle Impoundment (MANDATORY for 30-Day and 90-Day IRPs)"]]' :path="path + '/irp_yes'" rules="required">
          Vehicle Impound Duration
        </radio-field>
      </form-row>
      <form-row>
        <text-field id="ipr_number" fg_class="col-sm-3" :path="path + '/irp_yes'" v-mask="'##-#######'">IRP Number</text-field>
        <div class="col-sm-">
          This VI Number <span class="small muted">(repeated here for your records)</span>
          <p class="shadow p-1 mt-2 border bg-light rounded">
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
      rootPath() {
        return this.path.replace("/data", "");
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