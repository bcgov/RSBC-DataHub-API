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
        <span v-if="!retirementAchievementUnlocked">
          <router-link :to="{ name: prohibition.form_type, params: { id: prohibition.form_id } }">
            <span class="btn btn-success mr-3">&nbsp; Edit &nbsp;</span>
          </router-link>
          &nbsp;
        </span>
        <b-button class="btn btn-danger mr-3 color-warning" v-b-modal="'modal_' + prohibition.form_id">Delete</b-button>
        <b-modal :id="'modal_' + prohibition.form_id" title="Confirm Delete" @ok="deleteSpecificForm(prohibition)" ok-title="Delete" ok-variant="danger">
          <p>Form has not been printed. Are you sure you want to delete it?</p>
          <p class="text-danger"><b-icon-exclamation-triangle-fill variant="warning" />&nbsp; WARNING: This cannot be undone.</p>
        </b-modal>
      </h6>
      <div v-if="!isFormEditable(prohibition)">
        <div v-for="(document, index) in getDocumentsToPrint(prohibition.form_type)" v-bind:key="index">
          <print-documents v-if="document.reprint" :form_object="prohibition" :validate="() => { return true }" :variants="document.variants">
            Print Again
          </print-documents>
        </div>
      </div>
    </td>
  </tr>
</template>
<script>
  import PrintDocuments from "@/components/forms/PrintDocuments";
  import { mapGetters, mapActions, mapMutations } from 'vuex';
  export default {
    name: "RecentProhibitionRow",
    components: {
      PrintDocuments
    },
    computed: {
      ...mapGetters(["isFormEditable", "getServedStatus", "getDocumentsToPrint", "retirementAchievementUnlocked"])
    },
    data() {
      return {
        display_spinner: false
      }
    },
    methods: {
      ...mapMutations(["editExistingForm"]),
      ...mapActions(["deleteSpecificForm", "saveFormAndGeneratePDF"])
    },
    props: {
      prohibition: {}
    }
  }
</script>