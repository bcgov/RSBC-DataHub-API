<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
    <label v-if="show_label" :for="id"><slot></slot>
      <span v-if="required" class="text-danger"> *</span>
    </label>
    <select :disabled="disabled" class="form-control" :id="id" @input="updateFormField">
      <option v-for="province in getArrayOfProvinces"
              :key="province.objectCd"
              :selected="province.objectCd === getAttributeValue(id)">
        {{ province.objectCd }}
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
  name: "ProvinceField",
  mixins: [FieldCommon],
  mounted () {
    // set initial value to BC
    this.$store.commit("updateFormField", { target: { id: this.id, value: "BC"}})
  },
  computed: {
    ...mapGetters(["getArrayOfProvinces", "getAttributeValue"])
  },
  methods: {
    ...mapMutations(["updateFormField"])
  }
}
</script>
