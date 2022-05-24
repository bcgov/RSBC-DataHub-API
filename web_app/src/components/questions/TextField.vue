<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors }">
    <label v-if="show_label" :for="id"><slot></slot>
      <span v-if=" ! isShowOptional" class="text-danger"> *</span>
    </label>
    <input :type="input_type"
         class="form-control"
           :class="errors.length > 0 ? 'border-danger bg-warning' : ''"
         :id="id"
         :disabled="disabled || hasFormBeenPrinted"
         :placeholder="placeholder"
         v-model="attribute">
    <div class="small text-danger">{{ errors[0] }}</div>
  </validation-provider>
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters} from "vuex";


export default {
  name: "TextField",
  mixins: [FieldCommon],
  props: {
    placeholder: String,
    input_type: {
      type: String,
      default: "text"
    },
  },
  computed: {
    ...mapGetters(["getAttributeValue", "hasFormBeenPrinted"]),
    isShowOptional() {
      if(this.rules) {
        return ! this.rules.includes('required')
      }
      return true
    }
  }
}
</script>

<style>


</style>
