<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
      <label v-if="show_label" :for="id"><slot></slot></label>
      <span v-if="required" class="small text-danger"> *</span>
      <div class="form-check" v-for="option in options" :key="option[0]">
        <input class="form-check-input"
               :id="id + '_' + option"
               v-model="attribute"
               type="radio" v-bind:value="option[1]" :name="id"
               :disabled="disabled || hasFormBeenPrinted">
        <label class="form-check-label" :for="option[1]">{{ option[1] }}</label>
      </div>
      <div class="small text-danger">{{ errors[0] }}</div>
  </validation-provider>
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";

export default {
  name: "RadioDescription",
  mixins: [FieldCommon],
  props: {
    type: String(),
    options: null
  }
}
</script>
