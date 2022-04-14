<template>
  <form-card title="Officer">
    <form-row >

      <text-field id="badge_number" rules="required" fg_class="col-sm-3">Badge #</text-field>
      <text-field id="officer_name" rules="required" fg_class="col-sm-9">Last Name of Peace Officer Serving Prohibition Notice</text-field>
    </form-row>
    <form-row>
      <type-ahead-field id="agency" rules="required" fg_class="col-sm-8" :suggestions="getArrayOfAgencies">
        Agency
      </type-ahead-field>
      <text-field id="file_number" fg_class="col-sm-4" rules="required">Agency File #</text-field>
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
