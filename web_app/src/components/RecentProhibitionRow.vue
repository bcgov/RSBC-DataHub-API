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
      <div v-if="! isFormEditable(prohibition)" @click="triggerPrint" class="btn btn-primary small">
        Print again
        <b-spinner v-if="display_spinner" small label="Loading..."></b-spinner>
      </div>
    </td>
  </tr>
</template>

<script>

import { mapMutations, mapGetters, mapActions } from 'vuex';

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
    ...mapGetters(["isFormEditable", "getServedStatus"])
  },
  methods: {
    ...mapMutations(["editExistingForm"]),
    ...mapActions(["deleteSpecificForm", "saveFormAndGeneratePDF"]),
    triggerPrint() {
      console.log('inside triggerPrint()', this.display_spinner, this.getFormObject);
      this.display_spinner = true;
      this.saveFormAndGeneratePDF(this.prohibition)
          .then(() => {
            this.display_spinner = false;
          })
          .catch(() => {
            this.display_spinner = false;
          })

    }
  }
}
</script>
