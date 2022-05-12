<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <div class="form-check">
    <input class="form-check-input" :id="id" type="checkbox" v-model="attribute"
           :disabled="disabled || hasFormBeenPrinted"
           :value="option" :name="id">
    <label class="form-check-label" :for="id"><slot></slot></label>
  </div>
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters, mapMutations} from 'vuex';

export default {
  name: "InLineCheckBox",
  mixins: [FieldCommon],
  props: {
    type: String(),
    option: null
  },
  methods: {
    ...mapMutations(["updateCheckBox", "updateFormField"])
  },
  computed: {
    ...mapGetters(["checkBoxStatus", "hasFormBeenPrinted"])
  }
}
</script>
