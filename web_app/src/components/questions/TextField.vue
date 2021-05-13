<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
    <label v-if="show_label" class="small" :for="id"><slot></slot>
      <span v-if="required" class="text-danger"> *</span>
    </label>
    <input type="text"
         class="form-control form-control-sm"
         :id="id"
         :disabled="disabled"
         :placeholder="placeholder"
         :value="getAttributeValue(id)"
          @input="updateFormField">
    <div class="small text-danger">{{ errors[0] }}</div>
  </validation-provider>
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters, mapMutations} from "vuex";


export default {
  name: "TextField",
  mixins: [FieldCommon],
  props: {
    placeholder: String,
  },
  computed: {
    ...mapGetters(["getAttributeValue"]),
  },
  methods: {
    ...mapMutations(["updateFormField"])
  }
}
</script>
