<template>
<div class="form-group" :class="fg_class">
  <validation-provider rules="dob" :name="id" v-slot="{ errors, required }">
    <label v-if="show_label" :for="id">
      Date of Birth
      <span class="small text-muted"> YYYYMMDD</span>
      <span v-if="required" class="text-danger"> *</span>
      <span class="text-muted" v-if="isValidDate"> ({{ yearsOld }} yrs)</span>
    </label>
    <div class="col-xs-10">
      <input type="text"
           :disabled="disabled"
           :id="id"
           class="form-control"
             :class="errors.length > 0 ? 'border-danger bg-warning' : ''"
           placeholder="YYYYMMDD"
           v-model="attribute">
      <div class="small text-danger">{{ errors[0] }}</div>
    </div>
  </validation-provider>
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters, mapMutations} from 'vuex';
import moment from 'moment';

export default {
  name: "DoBField",
  mixins: [FieldCommon],
  methods: {
    ...mapMutations(['updateFormField']),
  },
  computed: {
    ...mapGetters(["getAttributeValue"]),
    yearsOld() {
      return moment().diff(moment(this.getAttributeValue(this.id)), 'years')
    },
    isValidDate() {
      return moment(this.getAttributeValue(this.id)).isValid()
    },
  }

}
</script>
