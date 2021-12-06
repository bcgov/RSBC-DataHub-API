<template>
<div v-if="visible" class="form-group" :class="fg_class">
    <label v-if="show_label" :for="id"><slot></slot></label>
    <div class="form-group form-check" v-for="option in options" :key="option.id">
      <input class="form-check-input"
             v-bind:id="option.id"
             v-bind:value="option.value"
             type="checkbox"
             @change="checkboxChanged"
             :disabled="disabled">
      <label class="form-check-label" :for="option.id" v-html="option.value"></label>
    </div>
<!--    <div class="small text-danger">{{ errors[0] }}</div>-->
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapActions, mapGetters} from 'vuex';

export default {
  name: "RichCheckField",
  mixins: [FieldCommon],
  props: {
    type: String(),
    options: null
  },
  methods: {
    ...mapActions(["updateRichCheckBox"]),
    checkboxChanged(event) {
      let payload = {
        id: this.id,
        event: event.target,
        form_object: this.getCurrentlyEditedFormObject
      }
      this.updateRichCheckBox(payload)
    }
  },
  computed: {
    ...mapGetters(["getAttributeValue", "getCurrentlyEditedFormObject"])
  }
}
</script>
