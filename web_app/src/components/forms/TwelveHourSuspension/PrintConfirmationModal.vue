<template>
  <div>
    <b-modal id="printConfirmationModal" hide-footer hide-header>
      <div class="d-block text-center">
        <h3>Was the prohibition printed and served to the driver?</h3>
        <p class="text-muted small">
          When you click "Yes" below, RoadSafety and ICBC will be sent a copy of the prohibition and
          the driver's record will be updated.  If you click "No", you'll be returned to the previous
          screen and the prohibition will not be sent.
        </p>
      </div>
      <div class="d-flex flex-row justify-content-between">
        <b-button class="mt-3" variant="danger" @click="confirmNotServedToDriver">No, not served</b-button>
        <b-button class="mt-3" variant="success" @click="confirmServedToDriver">Yes, served to driver</b-button>
      </div>

    </b-modal>
  </div>
</template>

<script>

import {mapMutations} from 'vuex';
import moment from "moment";

export default {
  name: "PrintConfirmationModal",
  methods: {
      ...mapMutations(["stopEditingCurrentForm", "markFormStatusAsServed"]),
      confirmServedToDriver() {
        this.markFormStatusAsServed(moment.now())
        this.$store.dispatch("saveCurrentFormToDB", this.$store.state.currently_editing_form_object)
        this.$bvModal.hide('printConfirmationModal')
        this.stopEditingCurrentForm();
      },
      confirmNotServedToDriver() {
        this.$bvModal.hide('printConfirmationModal')
      },
    }
}
</script>