<template>
    <div class="card-deck">
      <prohibition-card v-for="form in allForms"
                        :key="form.short_name"
                        :form="form">

      </prohibition-card>

    </div>
</template>

<script>

import ProhibitionCard from "@/components/ProhibitionCard";

export default {
  name: "IssueProhibitions",
  data() {
    return {
      selected_form: {
        short_name: null,
        full_name: null
      }
    }
  },
  methods: {
      serveForm() {
        this.$store.commit("setFormToServe", this.selected_form)
      }
  },
  computed: {
     allForms() {
       return this.$store.getters.getAllAvailableForms;
     }
  },
  components: {
    ProhibitionCard
  }
}
</script>

<style scoped>

</style>