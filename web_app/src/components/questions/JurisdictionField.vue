<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
    <label v-if="show_label" :for="id"><slot></slot>
      <span v-if="required" class="text-danger"> *</span>
    </label>
    <select :disabled="disabled || hasFormBeenPrinted" class="form-control" :id="id" @input="updateJurisdictionByEvent">
      <option v-for="jurisdiction in getArrayOfJurisdictions"
              :key="jurisdiction.objectCd"
              :selected="jurisdiction.objectDsc === getObjectDscIfExists">
        {{ jurisdiction.objectDsc }}
      </option>
    </select>
    <div class="small text-danger">{{ errors[0] }}</div>
  </validation-provider>
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import { mapGetters, mapMutations } from 'vuex';

export default {
  name: "JurisdictionObject",
  mixins: [FieldCommon],
  mounted () {
    // set initial value to BC if value not set
    if( ! this.getAttributeValue(this.path, this.id)) {
      const bc = this.getArrayOfProvinces.filter(j => j.objectCd === "BC")[0]
      this.$store.commit("updateFormField", { target: { id: this.id, path: this.path, value: bc}})
    }
  },
  computed: {
    ...mapGetters(["getArrayOfJurisdictions", "getAttributeValue", "hasFormBeenPrinted", "getJurisdictionByFullName"]),
    getObjectDscIfExists() {
      const value = this.getAttributeValue(this.path, this.id)
      if (value && 'objectDsc' in value) {
        return value.objectDsc
      }
      return ''
    }
  },
  methods: {
    ...mapMutations(["updateFormField"]),
    updateJurisdictionByEvent(e) {
      const jurisdictionName = e.target.value;
      this.updateJurisdictionByName(jurisdictionName)
    },
    updateJurisdictionByName(name) {
      const jurisdictionObject = this.getJurisdictionByFullName(name)
      console.log("jurisdictionUpdate()", name, jurisdictionObject)
      const payload = {target: {value: jurisdictionObject, id: this.id, path: this.path }}
      this.$store.commit("updateFormField", payload)
    }
  }
}
</script>
