<template>
    <div class="card border-light bg-secondary">
      <div class="card-header text-white text-left font-weight-bold small pl-3 pt-1 pb-1 bg-primary">
        {{ form.full_name }}
      </div>
      <div class="card-body bg-light">
      <p class="card-text text-dark">{{ form.description }}</p>
      <p class="card-text"><small class="text-muted">Last updated: {{ lastUpdatedFriendly }}</small></p>
        <button @click="serveForm" type="submit" class="btn btn-primary">View {{ form.short_name }} Form</button>
    </div>
    </div>
</template>

<script>

import moment from 'moment';

export default {
  name: "IssueProhibitions",
  props: {
      form: {}
  },
  methods: {
      serveForm() {
        this.$store.commit("setNewFormToEdit", this.form)
      }
  },
  computed: {
     allForms() {
       return this.$store.getters.getAllAvailableForms;
     },
     lastUpdatedFriendly() {
       return moment(this.form.last_updated).fromNow()
     }

  }
}
</script>
