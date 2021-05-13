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
             @input="updateFormField">
        <div class="input-group-append" v-if="isLicenceJurisdictionBC">
          <button @click="populateDriversFromICBC(getCurrentlyEditedProhibitionIndex)"
                  class="btn-sm btn-primary text-white">ICBC Lookup
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
    ...mapGetters(['getCurrentlyEditedProhibitionIndex', "getAttributeValue", "isLicenceJurisdictionBC"]),
    isNumberTheCorrectLength() {
      return this.getAttributeValue(this.id) === 7
    }
  },
  methods: {
    ...mapMutations(['populateDriversFromICBC', 'updateFormField']),
  }
}
</script>

<style scoped>

</style>