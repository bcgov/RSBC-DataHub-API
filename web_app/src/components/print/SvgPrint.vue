<template>
  <div>
    <variant v-for="(value, name) in document.variants"
       v-bind:key="name"
       :document="document"
       :variant="value"
       :form_type="form_type"
       :form_id="id">
    </variant>
  </div>
</template>

<script>

import print_layout from "../../config/print_layout.json";
import variant from "./variant"
import {mapGetters} from "vuex";

export default {
    name: "SvgPrint",
    props: {
      form_type: {
        type: String
      },
      id: {
        type: String,
      },
    },
    computed: {
      ...mapGetters(['getFormData']),
      document() {
        return print_layout[this.form_type]
      }
    },
    components: {
      variant
    }
}
</script>

