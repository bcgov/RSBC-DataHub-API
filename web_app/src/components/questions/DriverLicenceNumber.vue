<template>
  <div v-if="visible" class="form-group">
    <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
      <label v-if="show_label" class="small" :for="id"><slot></slot>
        <span v-if="required" class="text-danger"> *</span>
      </label>
      <div class="input-group mb-3">
        <input type=text
             class="form-control form-control-sm"
             :id="id"
             placeholder="Driver's Licence Number"
             :value="getAttributeValue(id)"
             @input="update">
        <div class="input-group-append">
          <button @click="populateDriversFromICBC(getCurrentlyEditedProhibitionNumber)"
                  class="btn-sm" :class="icbcLookupButtonClass" >ICBC Lookup
          </button>
        </div>
      </div>
      <div class="small text-danger">{{ errors[0] }}</div>
    </validation-provider>
  </div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters, mapMutations} from 'vuex';

export default {
  name: "DriversLicenceNumber",
  mixins: [FieldCommon],
  computed: {
    ...mapGetters(['getCurrentlyEditedProhibitionNumber', "getAttributeValue"]),
    isNumberTheCorrectLength() {
      return this.getAttributeValue(this.id) === 7
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
    ...mapMutations(['populateDriversFromICBC']),
  }
}
</script>

<style scoped>

</style>