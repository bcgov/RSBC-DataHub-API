<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
    <label class="small" :for="id"><slot></slot>
      <span v-if="required" class="text-danger"> *</span>
      <span class="text-muted" v-if="isValidDate"> ({{ timeAgo }})</span>
    </label>
    <div class="col-xs-10">
      <div class="input-group mb-1">
        <input type="text"
           class="form-control form-control-sm " :disabled="disabled"
           placeholder="YYYY-MM-DD"
           :id="id"
           :value="getAttributeValue(id)"
           @input="updateFormField">
      </div>
      <div class="small text-danger ml-1">{{ errors[0] }}</div>
    </div>
  </validation-provider>
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import moment from 'moment';
import {mapGetters, mapMutations} from "vuex";

export default {
  name: "DateField",
  mixins: [FieldCommon],

  methods: {
    ...mapMutations(["updateFormField"]),
    setCurrentDateTime() {
      const payload = {id: this.id, value: this.getCurrentTime() }
      console.log('inside DateField setCurrentDateTime()')
      this.$store.commit("updateFormField", payload)
    },

    getCurrentTime() {
      return moment().format("YYYY-MM-DD")
    },
  },

  computed: {
    ...mapGetters(["getAttributeValue"]),
    dateObject() {
      return moment(this.getAttributeValue(this.id), 'YYYY-MM-DD', true);
    },
    isValidDate() {
      return this.dateObject.isValid()
    },
    timeAgo() {
      if(this.isValidDate) {
        return this.dateObject.fromNow()
      }
      return null
    },
    timeAgoString() {
      return this.timeAgo() + ' months ago'
    }
  }

}
</script>
