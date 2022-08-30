<template>
  <form-card title="Immediate Roadside Prohibition">
    <form-row>
      <radio-field id="irp" :path="path"
                   fg_class="col-sm-6" :options='[["yes", "Yes"], ["no", "No"]]'
                   rules="required">Was an IRP issued as part of this vehicular impound?<br /><span class="text-muted">In accordance
                    with Section 215.46 and 253 of the Motor Vehicle Act</span>
      </radio-field>
    </form-row>
    <div v-if="getAttributeValue(path, 'irp_yes')">
      <form-row >
        <radio-field id="duration" :path="path + '/irp_yes'"
                     fg_class="col-sm-6" :options='[["3-day", "3-Day"], ["7-day", "7-Day"], ["30-day", "30-Day"]]'
                     rules="required">Duration
        </radio-field>
      </form-row>
      <form-row>
        <text-field id="ipr_number" :path="path + '/irp_yes'" fg_class="col-sm-3">IRP Number</text-field>
        <text-field id="form_id" :path="rootPath" :disabled="true" fg_class="col-sm-3">
          This VI Number <span class="small muted">(repeated here for your records)</span></text-field>
      </form-row>
    </div>

  </form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";

export default {
  name: "ImmediateRoadsideProhibition",
  mixins: [CardsCommon],
  computed: {
    rootPath() {
      return this.path.replace("/data", "")
    }
  }
}

</script>

<style scoped>

</style>