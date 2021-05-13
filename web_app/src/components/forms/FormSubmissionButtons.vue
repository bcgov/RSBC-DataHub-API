<template>
  <div class="w-100">
      <div class="form-row float-right mb-3 mr-3">
    <button @click="deleteSpecificForm(getCurrentlyEditedProhibitionIndex)" class="btn btn-danger m-1">Delete</button>
    <button @click="saveDoNotPrint" type="submit" class="btn btn-success m-1">Save, complete later</button>
    <button @click="saveAndPrint" class="btn btn-success m-1">Save and Serve</button>
  </div>
  </div>
</template>

<script>

import { mapMutations, mapGetters, mapActions } from 'vuex';

export default {
  name: "FormSubmissionButtons",
  computed: {
    ...mapGetters(["getCurrentlyEditedProhibitionIndex", "getCurrentlyEditedProhibitionNumber", "getXdfFileName"])
  },
  methods: {
    ...mapActions(["saveDoNotPrint", "deleteSpecificForm"]),
    ...mapMutations(["markFormStatusAsServed", "saveFormsToLocalStorage"]),

    saveAndPrint() {
      // this.$v.$touch()
      const prohibition_index = this.getCurrentlyEditedProhibitionIndex;
      this.xml_file = this.$store.getters.generateXFDF(prohibition_index);
      const downloadElement = document.createElement("a");
      const href = window.URL.createObjectURL(this.xml_file); //create the download url
      downloadElement.href = href;
      downloadElement.download =  this.getXdfFileName(prohibition_index);
      document.body.appendChild(downloadElement);
      downloadElement.click(); //click to file
      document.body.removeChild(downloadElement); //remove the element
      window.URL.revokeObjectURL(href); //release the object  of the blob
      this.markFormStatusAsServed();
      this.saveFormsToLocalStorage();
      this.$bvModal.show('printConfirmationModal')
    }
  }
}
</script>