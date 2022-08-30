<template>
  <span v-if="displayCheckDigit" id="check-digit">{{ checkDigit }}</span>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "CheckDigit",
  props: {
    form_object: Object
  },
  computed: {
    ...mapGetters(["getFormIdCheckDigit"]),
    checkDigit() {
      return this.getFormIdCheckDigit(this.form_object);
    },
    displayCheckDigit() {
      return this.checkDigit !== ''
    }
  }
}
</script>

<style scoped>

</style>