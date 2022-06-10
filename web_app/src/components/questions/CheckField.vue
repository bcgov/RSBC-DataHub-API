<template>
<div v-if="visible" class="form-group" :class="fg_class">
    <label v-if="show_label" :for="id"><slot></slot>
<!--      <span v-if="required" class="text-danger"> *</span>-->
    </label>
    <div class="form-check" v-for="option in options" :key="option[0]">
      <input class="form-check-input"
             :id="id"
             type="checkbox"
             @input="updateCheckBox"
             v-bind:value="option[0]"
             :name="option[0]"
             :disabled="disabled || hasFormBeenPrinted">
      <label class="form-check-label" :for="option[0]">{{ option[1] }}</label>
    </div>
<!--    <div class="small text-danger">{{ errors[0] }}</div>-->
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters} from 'vuex';

export default {
  name: "CheckField",
  mixins: [FieldCommon],
  props: {
    type: String(),
    options: null
  },
  methods: {
    updateCheckBox (event) {
        let key = event.target.id + "_" + event.target.value;
        const payload = {
          target: {
            path: this.path,
            id: key,
            value: {}
          }
        }
        console.log("updateCheckBox()", key, payload)
        if (event.target.checked) {
            this.updateFormField(payload)
        } else {
          // item exists; remove it
          if (this.doesAttributeExist(this.path, key)) {
            this.deleteFormField(payload)
          }
        }

    },
  },
  computed: {
    ...mapGetters(["checkBoxStatus", "hasFormBeenPrinted", "doesAttributeExist"]),
  }
}
</script>
