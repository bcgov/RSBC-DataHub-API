<template>
  <form-card title="Incident Details">
    <form-row>
      <memo-field :show_label=false id="incident_details" rules="max:765" fg_class="col-sm-12">Incident details</memo-field>
    </form-row>
  </form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";
import MemoField from "@/components/questions/MemoField";

export default {
  name: "IncidentDetailsCard",
  components: {MemoField},
  mixins: [CardsCommon]
}
</script>
