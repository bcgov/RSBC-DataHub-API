<template>
<div v-if="visible" class="form-group" :class="fg_class">
    <label v-if="show_label" :for="id"><slot></slot></label>
    <input type="text"
         class="form-control"
         :id="id"
         :disabled=true
         placeholder="seeking ICBC approval">
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";


export default {
  name: "WaitForICBCField",
  mixins: [FieldCommon],
}
</script>
