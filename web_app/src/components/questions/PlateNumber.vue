<template>
  <div v-if="visible" class="form-group" :class="fg_class">
    <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
      <label v-if="show_label" class="small" :for="id"><slot></slot>
        <span v-if="required" class="text-danger"> *</span>
      </label>
      <div class="input-group mb-3">
        <input type=text
             class="form-control form-control-sm"
             :id="id"
             placeholder="Plate"
             :value="getAttributeValue(id)"
             @input="updateFormField">
        <div class="input-group-append" v-if="isPlateJurisdictionBC">
          <button @click="populateFromICBCPlateLookup" class="btn-sm btn-primary">ICBC Lookup</button>
        </div>
        <div class="small text-danger">{{ errors[0] }}</div>
      </div>
    </validation-provider>
  </div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters, mapMutations} from "vuex";

export default {
  name: "PlateNumber",
  mixins: [FieldCommon],
  computed: {
    ...mapGetters(["getAttributeValue", "isPlateJurisdictionBC"]),
    isNumberTheCorrectLength() {
      return this.getAttributeValue(this.id) >= 3
    },
    icbcLookupButtonClass() {
      if (this.isNumberTheCorrectLength) {
        return " btn-primary text-white "
      } else {
        return " btn-secondary text-muted "
      }
    }
  },
  methods: {
    ...mapMutations(["populateFromICBCPlateLookup", "updateFormField"])
  }
}
</script>

<style scoped>

</style>