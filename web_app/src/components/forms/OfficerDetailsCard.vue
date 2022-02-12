<template>
  <form-card title="Officer">
    <form-row >
      <text-field id="agency" rules="required" fg_class="col-sm-6">Agency</text-field>
      <text-field id="badge_number" rules="required" fg_class="col-sm-2">Badge #</text-field>
      <text-field id="officer_name" rules="required" fg_class="col-sm-4">Last Name of Peace Officer Serving Prohibition Notice</text-field>
    </form-row>
  </form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";

export default {
  name: "OfficerDetailsCard",
  mixins: [CardsCommon]
}
</script>
