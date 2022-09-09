<template>
  <div>
    <print-confirmation
        :form_type="form_type"
        :id="id"
        :show_certificate="isCertificateOfServiceEnabled(getPath)">
    </print-confirmation>
    <variant v-for="(value, name) in getVariants"
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
import PrintConfirmation from "@/components/print/PrintConfirmation";

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
      ...mapGetters(['getFormData', "isVehicleImpounded", "isCertificateOfServiceEnabled"]),
      document() {
        return print_layout[this.form_type]
      },
      // Remove ILO Copy if not needed
      getVariants() {
        if(this.form_type === '12Hour' || this.form_type === '24Hour') {
            if ( ! this.isVehicleImpounded(this.getPath)) {
                // remove page for impound lot operator if vehicle not impounded
                delete this.document.variants['ilo']
            }
        }
        return this.document.variants
      },
      getPath() {
      return `forms/${this.form_type}/${this.id}/data`
    }
    },
    components: {
      variant,
      PrintConfirmation
    }
}
</script>

<style scoped>

  @media print {

     #is-served {
       display: none;
     }

  }

</style>

