<template>
  <form-card title="Incident Details">
    <form-row>
      <in-line-check-box id="incident_details_attached" :path=path :option="true">Incident Details Attached</in-line-check-box>
    </form-row>
    <form-row>
      <memo-field :show_label=false id="incident_details" :path=path rules="max:765" fg_class="col-sm-12">Incident details</memo-field>
    </form-row>
  </form-card>
</template>

<script>
  import CardsCommon from "@/components/forms/CardsCommon";
  import InLineCheckBox from "@/components/questions/InLineCheckBox";
  import MemoField from "@/components/questions/MemoField";
  export default {
    name: "IncidentDetailsCard",
    components: {InLineCheckBox, MemoField},
    mixins: [CardsCommon]
  }
</script>
