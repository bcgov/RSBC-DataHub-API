<template>
  <div v-if="visible" class="form-group" :class="fg_class">
    <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
      <label :for="id"><slot></slot></label>
      <span v-if="required" class="small text-danger"> *</span>
      <multiselect v-model="attribute"
                   tag-placeholder="That's not an option"
                   :disabled="disabled || hasFormBeenPrinted"
                   placeholder="Search for a BC city or town name"
                   :options="getArrayOfBCCityNames"></multiselect>
      <div class="small text-danger">{{ errors[0] }}</div>
    </validation-provider>
  </div>
</template>

<script>

// This TypeAhead Field will NOT update when the state changes
// Do not use this component for fields that update from an ICBC query

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters} from 'vuex';

export default {
  name: "OffenceCity",
  mixins: [FieldCommon],
  props: {
    id: {
      type: String,
      default: "offence_city"
    },
    suggestions: {
      default: Array
    }
  },
  data() {
    return {
      query: ''
    }
  },
  computed: {
    ...mapGetters(["getAttributeValue", "hasFormBeenPrinted", "getArrayOfBCCityNames"]),
  },
}
</script>