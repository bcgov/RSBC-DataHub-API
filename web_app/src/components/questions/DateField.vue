<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
    <label :for="id"><slot></slot>
      <span v-if="required" class="text-danger"> *</span>
      <span class="small text-muted"> YYYYMMDD</span>
      <span class="text-muted" v-if="isValidDate"> ({{ timeAgo }})</span>
    </label>
    <div class="col-xs-10">
      <div class="input-group mb-1">
        <input type="text"
           class="form-control " :disabled="disabled"
           placeholder="YYYYMMDD"
           :id="id"
           :value="getAttributeValue(id)"
           @input="setDateTime">
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
    setDateTime(e) {
      const isoDate = e.target.value;
      const payload = {target: {id: this.id, value: isoDate }}
      this.$store.commit("updateFormField", payload)
    },
  },

  computed: {
    ...mapGetters(["getAttributeValue"]),
    dateObject() {
      return moment(this.getAttributeValue(this.id), 'YYYYMMDD', true);
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
