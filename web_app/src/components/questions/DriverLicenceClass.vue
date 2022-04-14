<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
    <label v-if="show_label" :for="id"><slot></slot>
      <span v-if="required" class="text-danger"> *</span>
    </label>
    <input type="number"
           :disabled="disabled || hasFormBeenPrinted"
           :id="id"
           class="form-control"
             :class="errors.length > 0 ? 'border-danger bg-warning' : ''"
           v-model="attribute">
    <div class="small text-danger">{{ errors[0] }}</div>
  </validation-provider>
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import { mapGetters, mapMutations } from 'vuex';

export default {
  name: "DriverLicenceClass",
  mixins: [FieldCommon],

  computed: {
    ...mapGetters(["getAttributeValue"])
  },
  methods: {
    ...mapMutations(["updateFormField"])
  }

}
</script>
