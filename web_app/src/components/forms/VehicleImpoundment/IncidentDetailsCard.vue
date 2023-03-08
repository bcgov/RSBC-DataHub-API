<template>
  <form-card title="Incident Details">
    <form-row>
      <in-line-check-box id="incident_details_attached" :option="true" :path=path>Will a separate document be attached?</in-line-check-box>
    </form-row>
    <form-row>
      <memo-field id="incident_details" fe_class="uppercase" fg_class="col-sm-12" max_length="650" :path=path rules="max:650" :show_label=false>Incident details</memo-field>
    </form-row>
  </form-card>
</template>
<script>
  import CardsCommon from "@/components/forms/CardsCommon";
  import InLineCheckBox from "@/components/questions/InLineCheckBox";
  import MemoField from "@/components/questions/MemoField";
  export default {
    name: "IncidentDetailsCard",
    components: {
      InLineCheckBox,
      MemoField
    },
    mixins: [ CardsCommon ]
  }
</script>