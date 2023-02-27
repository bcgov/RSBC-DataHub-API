<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
    <label v-if="show_label" :for="id"><slot></slot>
      <span v-if="required" class="text-danger"> *</span>
    </label>
    <multiselect :value="getAttributeValue(path, id)"
                   @input="updateJurisdiction"
                   :disabled="disabled || hasFormBeenPrinted"
                   :id="id"
                   label="objectDsc"
                   track-by="objectCd"
                   placeholder="Search for a Jurisdiction"
                   :options="getArrayOfJurisdictions">
    </multiselect>
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
      const bc = this.getArrayOfJurisdictions.filter(j => j.objectCd === "BC")[0]
      this.$store.commit("updateFormField", { target: { id: this.id, path: this.path, value: bc}})
    }
  },
  computed: {
    ...mapGetters(["getArrayOfJurisdictions", "getAttributeValue", "hasFormBeenPrinted", "getJurisdictionByFullName"])
  },
  methods: {
    ...mapMutations(["updateFormField"]),
    updateJurisdiction(event) {
      console.log("updateJurisdiction()", event)
      const payload = {
        "target": {
          "path": this.path,
          "id": this.id,
          "value": event
        }
      }
      this.updateFormField(payload)
    }
  }
}
</script>
