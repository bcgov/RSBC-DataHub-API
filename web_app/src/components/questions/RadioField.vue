<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
      <label v-if="show_label" :for="id"><slot></slot></label>
      <span v-if="required" class="small text-danger"> *</span>
      <div class="form-check" v-for="option in options" :key="option[0]">
        <input class="form-check-input"
               :id="id"
               v-model="attribute"
               type="radio" v-bind:value="option[0]" :name="id"
               :disabled="disabled || hasFormBeenPrinted">
        <label class="form-check-label" :for="option[0]">{{ option[1] }}</label>
      </div>
      <div class="small text-danger">{{ errors[0] }}</div>
  </validation-provider>
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters, mapMutations} from 'vuex';

export default {
  name: "RadioField",
  mixins: [FieldCommon],
  props: {
    type: String(),
    options: null
  },
  methods: {
    ...mapMutations(["deleteFormField"])
  },
  computed: {
    ...mapGetters(["doesAttributeExist", "hasFormBeenPrinted"]),
    attribute: {
      get() {
        // loop through the options keys and check the existence of an attribute
        // with the pattern {id}_{key}
        var result = undefined
        this.options.forEach((option) => {
          if (this.doesAttributeExist(this.path, this.id + "_" + option[0] )) {
            result = option[0]
          }
        })
        return result
      },
      set(key) {
        // loop through the option keys and if an old key exists, delete it, otherwise save it
        this.options.forEach((option) => {
          const payload = {
            target: {
                path: this.path,
                id: this.id + "_" + option[0],
                value: {}
              }
          }
          if (key === option[0]) {
            this.updateFormField(payload)
          } else {
            this.deleteFormField(payload)
          }
        })
      }
    },
  }
}
</script>
