<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
    <label :for="id"><slot></slot></label>
    <span v-if="required" class="small text-danger"> *</span>
    <vue-typeahead-bootstrap :input-class="errors.length > 0 ? 'border-danger bg-warning' : ''" @input="typeAheadUpdate" :value="getAttributeValue(id)" :data=suggestions :disabled="disabled" />
    <div class="small text-danger">{{ errors[0] }}</div>
  </validation-provider>
</div>
</template>

<script>

import VueTypeaheadBootstrap from 'vue-typeahead-bootstrap';
import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters} from 'vuex';

export default {
  name: "TypeAheadField",
  mixins: [FieldCommon],
  props: {
    suggestions: {
      default: Array
    }
  },
  computed: {
    ...mapGetters(["getAttributeValue"]),
  },
  methods: {
    typeAheadUpdate(e) {
      const payload = {target: {value: e, id: this.id }}
      this.$store.commit("updateFormField", payload)
    }
  },
  components: {
    VueTypeaheadBootstrap
  }
}
</script>