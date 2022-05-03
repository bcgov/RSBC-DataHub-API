<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
    <label :for="id"><slot></slot></label>
    <span v-if="required" class="small text-danger"> *</span>
    <vue-typeahead-bootstrap :input-class="errors.length > 0 ? 'border-danger bg-warning' : ''"
                             @hit="typeAheadUpdate"
                             v-model="query"
                             :data="getArrayOfImpoundLotOperators"
                             :disabled="disabled || hasFormBeenPrinted"
                             :inputName="id + '_typeahead'" />
    <div class="small text-danger">{{ errors[0] }}</div>
  </validation-provider>
</div>
</template>

<script>

import VueTypeaheadBootstrap from 'vue-typeahead-bootstrap';
import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters} from 'vuex';

export default {
  name: "ImpoundLotOperator",
  mixins: [FieldCommon],
  props: {
    id: {
      type: String,
      default: 'impound_lot_operator'
    },
    suggestions: {
      default: Array
    }
  },
  data(){
      return {
        query: '',
      }
    },
  computed: {
    ...mapGetters(["getAttributeValue", "hasFormBeenPrinted", "getArrayOfImpoundLotOperators", "getImpoundLotOperatorObject"]),
  },
  methods: {
    typeAheadUpdate(e) {
      const ilo_object = this.getImpoundLotOperatorObject(e)
      const payload = {target: {value: ilo_object, id: this.id }}
      this.$store.commit("updateFormField", payload)
    }
  },
  components: {
    VueTypeaheadBootstrap
  }
}
</script>