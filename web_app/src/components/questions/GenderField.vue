<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
    <label v-if="show_label" :for="id"><slot></slot>
      <span v-if="required" class="text-danger"> *</span>
    </label>
    <select :disabled="disabled || hasFormBeenPrinted" class="form-control" :id="id" v-model="attribute">
      <option>Gender Diverse</option>
      <option>Female</option>
      <option>Male</option>
      <option>Unknown</option>
    </select>
    <div class="small text-danger">{{ errors[0] }}</div>
  </validation-provider>
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";

export default {
  name: "GenderField",
  mixins: [FieldCommon]

}
</script>
