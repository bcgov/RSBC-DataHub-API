<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
      <label v-if="show_label" :for="id"><slot></slot></label>
      <span v-if="required" class="small text-danger"> *</span>
      <div class="form-check" v-for="(option, index) in options" :key="index">
        <input class="form-check-input"
               :id="id"
               v-model="attribute"
               type="radio" v-bind:value="option" :name="id"
               :disabled="disabled || hasFormBeenPrinted">
        <label class="form-check-label" :for="option">{{ option }}</label>
      </div>
      <div class="small text-danger">{{ errors[0] }}</div>
  </validation-provider>
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapMutations, mapGetters} from 'vuex';

export default {
  name: "RadioField",
  mixins: [FieldCommon],
  props: {
    type: String(),
    options: null
  },
  methods: {
    ...mapMutations(["updateFormField"])
  },
  computed: {
    ...mapGetters(["getAttributeValue", "hasFormBeenPrinted"])
  }
}
</script>
