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
        <router-link :to="{ name: prohibition.form_type, params: { id: prohibition.form_id } }">
          <span class="btn btn-success mr-3">&nbsp; Edit &nbsp;</span>
          <!-- <b-icon-pen variant="primary"></b-icon-pen> -->
        </router-link>
        &nbsp; &nbsp;
        <!-- <b-icon-trash variant="danger" @click="deleteSpecificForm(prohibition)"></b-icon-trash> -->

        <b-button class="btn btn-danger mr-3 color-warning" v-b-modal.modal-1>Delete</b-button>
        <b-modal id="modal-1" title="Delete Form" hide-footer>
          <p>Are you sure you want to delete this form?</p>
          <p class="text-muted">This function cannot be undone.</p>
          <b-button class="btn btn-danger mr-3 color-warning" @click="deleteSpecificForm(prohibition)">Delete</b-button>
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
      ...mapGetters(["isFormEditable", "getServedStatus", "getDocumentsToPrint"])
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