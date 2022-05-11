<template>
  <tr v-if="prohibition">
    <td>
      {{ prohibition.data.last_name }},
      {{ prohibition.data.first_name }}
      ({{ prohibition.data.drivers_number }})
    </td>
    <td>{{ prohibition.form_type }}</td>
    <td>{{ getServedStatus(prohibition) }}</td>
    <td><span class="text-muted text-secondary">{{ prohibition.form_id }}</span></td>
    <td>
      <h6 v-if="isFormEditable(prohibition)">
        <b-icon-trash variant="danger" @click="deleteSpecificForm(prohibition)"></b-icon-trash>&nbsp;
        <router-link :to="{ name: prohibition.form_type, params: { id: prohibition.form_id}}">
          <b-icon-pen variant="primary"></b-icon-pen>
        </router-link>
      </h6>
      <div v-if="! isFormEditable(prohibition)">
        <div v-for="(document, index) in getDocumentsToPrint(prohibition.form_type)" v-bind:key="index">
          <print-documents
            v-if="document.reprint"
            :form_object="prohibition"
            :validate="() => { return true }"
            :variants="document.variants">
            Print again
          </print-documents>
        </div>

      </div>
    </td>
  </tr>
</template>

<script>

import { mapMutations, mapGetters, mapActions } from 'vuex';
import PrintDocuments from "@/components/forms/PrintDocuments";

export default {
  name: "RecentProhibitionRow",
  props: {
    prohibition: {}
  },
  data() {
    return {
      display_spinner: false
    }
  },
  computed: {
    ...mapGetters(["isFormEditable", "getServedStatus", "getDocumentsToPrint"])
  },
  methods: {
    ...mapMutations(["editExistingForm"]),
    ...mapActions(["deleteSpecificForm", "saveFormAndGeneratePDF"]),
  },
  components: {
    PrintDocuments
  }
}
</script>
