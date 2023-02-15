<template>
  <form-card title="Impoundment for Immediate Roadside Prohibition">
    <form-row>
      <radio-field id="irp" fg_class="col-sm-6" :options='[["yes", "Yes"], ["no", "No"]]' :path="path" rules="required">
        Was an IRP issued as part of this vehicular impound?
        <br />
        <span class="text-muted">In accordance with Section 215.46 and 253 of the Motor Vehicle Act</span>
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
        <text-field id="form_id" fg_class="col-sm-3" :disabled="true" :path="rootPath">
          This VI Number <span class="small muted">(repeated here for your records)</span>
        </text-field>
      </form-row>
    </div>
  </form-card>
</template>
<script>
  import CardsCommon from "@/components/forms/CardsCommon";
  export default {
    name: "ImmediateRoadsideProhibition",
    computed: {
      rootPath() {
        return this.path.replace("/data", "");
      }
    },
    mixins: [ CardsCommon ]
  }
</script>