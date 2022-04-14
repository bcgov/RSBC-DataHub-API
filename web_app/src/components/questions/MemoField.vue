<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors }">
    <label v-if="show_label" :for="id"><slot></slot>
      <span v-if=" ! isShowOptional" class="text-danger"> *</span>
    </label>
    <textarea
          rows="10"
         class="form-control"
           :class="errors.length > 0 ? 'border-danger bg-warning' : ''"
         :id="id"
         :disabled="disabled || hasFormBeenPrinted"
         :placeholder="placeholder"
         v-model="attribute">
    </textarea>
    <div class="small text-danger">{{ errors[0] }}</div>
  </validation-provider>
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters, mapMutations} from "vuex";


export default {
  name: "MemoField",
  mixins: [FieldCommon],
  props: {
    placeholder: String,
  },
  computed: {
    ...mapGetters(["getAttributeValue", "hasFormBeenPrinted"]),
    isShowOptional() {
      if(this.rules) {
        return ! this.rules.includes('required')
      }
      return true
    }
  },
  methods: {
    ...mapMutations(["updateFormField"])
  }
}
</script>

<style>


</style>
