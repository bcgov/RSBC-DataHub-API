<template>
<div v-if="visible" class="form-group" :class="fg_class">
    <label v-if="show_label" :for="id"><slot></slot>
<!--      <span v-if="required" class="text-danger"> *</span>-->
    </label>
    <check-field-item :disabled="disabled || hasFormBeenPrinted"
                      class="form-check" v-for="option in options"
                      :key="option[0]"
                      :path="path"
                      :label="option[1]"
                      :id="id + '_' + option[0]">
    </check-field-item>
<!--    <div class="small text-danger">{{ errors[0] }}</div>-->
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters} from 'vuex';
import CheckFieldItem from "@/components/questions/CheckField/CheckFieldItem";

export default {
  name: "CheckField",
  components: {CheckFieldItem},
  mixins: [FieldCommon],
  props: {
    type: String(),
    options: null
  },
  computed: {
    ...mapGetters(["checkBoxStatus", "hasFormBeenPrinted", "doesAttributeExist"]),
  }
}
</script>
