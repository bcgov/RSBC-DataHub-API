<template>
<div class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
    <label v-if="show_label" class="small" :for="id">
      Date of Birth
      <span v-if="required" class="text-danger">*</span>
      <span class="text-muted" v-if="isValidDate"> ({{ yearsOld }} yrs)</span>
    </label>
    <div class="col-xs-10">
      <input type="text"
           :id="id"
           class="form-control form-control-sm"
           placeholder="YYYY-MM-DD"
           :value="getAttributeValue(id)"
            @input="updateFormField">
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
    ...mapMutations(['updateFormField'])
  },
  computed: {
    ...mapGetters(["getAttributeValue"]),
    yearsOld() {
      return moment().diff(moment(this.getAttributeValue(this.id)), 'years')
    },
    yearsAgo() {
      return moment(this.getAttributeValue(this.id)).fromNow()
    },
    isValidDate() {
      return moment(this.getAttributeValue(this.id)).isValid()
    },
  }

}
</script>
