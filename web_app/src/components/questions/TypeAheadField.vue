<template>
  <div v-if="visible" class="form-group" :class="fg_class">
    <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
      <label :for="id"><slot></slot></label>
      <span v-if="required" class="small text-danger"> *</span>
      <vue-typeahead-bootstrap :input-class="errors.length > 0 ? 'border-danger bg-warning' : ''"
                               @input="typeAheadUpdate"
                               v-model="query"
                               :data=suggestions
                               :disabled="disabled || hasFormBeenPrinted"
                               :inputName="id + '_typeahead'" />
      <div class="small text-danger">{{ errors[0] }}</div>
    </validation-provider>
  </div>
</template>

<script>

// This TypeAhead Field will NOT update when the state changes
// Do not use this component for fields that update from an ICBC query

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
  data() {
    return {
      query: ''
    }
  },
  computed: {
    ...mapGetters(["getAttributeValue", "hasFormBeenPrinted"]),
  },
  methods: {
    typeAheadUpdate(e) {
      console.log("typeAheadUpdate()", e)
      const payload = {
        target: {
          value: e.toUpperCase(),
          id: this.id,
          path: this.path
        }
      }
      this.updateFormField(payload)
    }
  },
  components: {
    VueTypeaheadBootstrap
  }
}
</script>