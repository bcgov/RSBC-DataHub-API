<template>
  <form-card title="Officer">
    <form-row >
      <text-field id="agency"
                  :default_value="getCurrentUserObject.agency"
                  :path="path" rules="required" fg_class="col-sm-6">
        Agency</text-field>
      <text-field id="badge_number"
                  :default_value="getCurrentUserObject.badge_number"
                  :path="path" rules="required" fg_class="col-sm-2">
        Badge #</text-field>
      <text-field id="officer_name"
                  :default_value="getCurrentUserObject.last_name"
                  :path="path" rules="required" fg_class="col-sm-4">
        Last Name of Peace Officer Serving Prohibition Notice</text-field>
    </form-row>
  </form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";
import {mapGetters} from "vuex";

export default {
  name: "OfficerDetailsCard",
  mixins: [CardsCommon],
  computed: {
    ...mapGetters(["getCurrentUserObject"])
  }
}
</script>
