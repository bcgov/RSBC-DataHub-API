<template>
  <form-card title="Officer">
    <form-row >
      <text-field id="agency" :default_value="getCurrentUserObject.agency" fe_class="uppercase" fg_class="col-sm-6" :path="path" rules="required">Agency or RCMP Detachment</text-field>
      <text-field id="badge_number" :default_value="getCurrentUserObject.badge_number" fg_class="col-sm-2" :path="path" rules="required">PRIME ID</text-field>
      <text-field id="officer_name" :default_value="getCurrentUserObject.last_name" fe_class="uppercase" fg_class="col-sm-4" :path="path" rules="required">Last Name of Peace Officer Serving Prohibition Notice</text-field>
    </form-row>
  </form-card>
</template>
<script>
  import CardsCommon from "@/components/forms/CardsCommon";
  import { mapGetters } from "vuex";
  export default {
    name: "OfficerDetailsCard",
    computed: {
      ...mapGetters([
        "getCurrentUserObject"
      ])
    },
    mixins: [ CardsCommon ]
  }
</script>