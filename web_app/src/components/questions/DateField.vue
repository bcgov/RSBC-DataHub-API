<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
    <label :for="id"><slot></slot>
      <span v-if="required" class="text-danger"> *</span>
      <span class="small text-muted"> YYYYMMDD</span>
    </label>
    <b-input-group class="mb-3">
      <b-form-input
        :id="id"
        v-model="attribute"
        type="text"
        placeholder="YYYYMMDD"
        autocomplete="off"
      ></b-form-input>
      <b-input-group-append>
        <b-form-datepicker
          button-only
          right
          :id="id"
          :disabled="disabled || hasFormBeenPrinted"
          @input="updateDate"
          reset-button
          locale="en-CA"
          label-reset-button="Clear"
          placeholder="Choose a date"
        ></b-form-datepicker>
      </b-input-group-append>
    </b-input-group>
    <div class="small text-danger ml-1">{{ errors[0] }}</div>
  </validation-provider>
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters, mapMutations} from "vuex";

export default {
  name: "DateField",
  mixins: [FieldCommon],

  methods: {
    ...mapMutations(["updateFormField"]),
    updateDate(event) {
      const payload = {"target": {
          "id": this.id,
          "path": this.path,
          "value": event.replace(/-/gi, "")
        }}
      this.updateFormField(payload);
    },
  },

  computed: {
    ...mapGetters(["getAttributeValue", "hasFormBeenPrinted"]),
    getDatePickerValue() {
      const dateString = this.getAttributeValue(this.path, this.id)
      if (dateString) {
        return dateString.slice(0,4) + '-' + dateString.slice(5,2) + '-' + dateString.slice(7,2)
      } else {
        return ''
      }

    }
  }

}
</script>
