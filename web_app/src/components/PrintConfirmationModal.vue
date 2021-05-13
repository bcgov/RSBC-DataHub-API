<template>
  <div>
    <b-modal id="printConfirmationModal" hide-footer hide-header>
      <div class="d-block text-center">
        <h3>The prohibition has been sent to RoadSafety</h3>
        <p class="text-muted small">
          The completed prohibition has been downloaded to your computer.
          Open the prohibition with Adobe Acrobat, print it and serve it
          to the citizen.
        </p>
      </div>
      <div class="w-100 text-center">
        <b-button class="mt-3" variant="success" @click="okayAcknowledged">Ok</b-button>
      </div>

    </b-modal>
  </div>
</template>

<script>

import {mapMutations} from 'vuex';

export default {
  name: "PrintConfirmationModal",
  methods: {
      ...mapMutations(["stopEditingCurrentForm"]),
      okayAcknowledged() {
        this.stopEditingCurrentForm();
        this.$bvModal.hide('printConfirmationModal')
      },
    }
}
</script>