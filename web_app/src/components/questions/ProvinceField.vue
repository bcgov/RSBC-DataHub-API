<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
    <label v-if="show_label" :for="id"><slot></slot>
      <span v-if="required" class="text-danger"> *</span>
    </label>
    <multiselect :value="getAttributeValue(path, id)"
                   @input="updateProvince"
                   :disabled="disabled || hasFormBeenPrinted"
                   :id="id"
                   tag-placeholder="That isn't an option"
                   label="objectDsc"
                   track-by="objectCd"
                   placeholder="Search for a Province or State"
                   :options="getArrayOfProvinces">
    </multiselect>
    <div class="small text-danger">{{ errors[0] }}</div>
  </validation-provider>
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import { mapGetters, mapMutations } from 'vuex';

export default {
  name: "ProvinceField",
  props: {
    defaultToBc: {
      type: Boolean,
      default: true
    }
  },
  mixins: [FieldCommon],
  mounted () {
    if(this.defaultToBc) {
      // set initial value to BC
      const bc = this.getArrayOfProvinces.filter(j => j.objectCd === "BC")[0]
      this.$store.commit("updateFormField", { target: { id: this.id, path: this.path, value: bc}})
    }
  },
  computed: {
    ...mapGetters(["getArrayOfProvinces", "getAttributeValue", "hasFormBeenPrinted"])
  },
  methods: {
    ...mapMutations(["updateFormField"]),
    updateProvince(event) {
      console.log("updateProvince()", event)
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
