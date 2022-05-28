<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
    <label v-if="show_label" :for="id"><slot></slot>
      <span v-if="required" class="text-danger"> *</span>
    </label>
    <vue-typeahead-bootstrap
          class="col-sm-12 mb-2"
          @input="typeAheadUpdate"
          placeholder="Province or State"
          :value="getProvinceName"
          :data="getArrayOfProvinceNames"
          :disabled="disabled || hasFormBeenPrinted"
          :inputName="id + '_typeahead'" />
    <div class="small text-danger">{{ errors[0] }}</div>
  </validation-provider>
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import VueTypeaheadBootstrap from 'vue-typeahead-bootstrap';
import { mapGetters, mapMutations } from 'vuex';

export default {
  name: "ProvinceAutocomplete",
  // data() {
  //   return {
  //     query: ''
  //   }
  // },
  mixins: [FieldCommon],
  computed: {
    ...mapGetters(["getArrayOfProvinceNames", "getProvinceObjectByName", "getAttributeValue", "hasFormBeenPrinted"]),
    getProvinceName() {
      const objectValue = this.getAttributeValue(this.path, this.id)
      if('objectCd' in objectValue) {
        return objectValue.objectDsc
      }
      return ''
    }
  },
  methods: {
    ...mapMutations(["updateFormField", "deleteFormField"]),
    typeAheadUpdate(e) {
      const provinceObject = this.getProvinceObjectByName(e)
      const payload = {target: {value: provinceObject, path: this.path, id: this.id }}
      if (e) {
        this.updateFormField(payload)
      } else {
        this.deleteFormField(payload)
      }
    }
  },
  components: {
    VueTypeaheadBootstrap
  }
}
</script>
