<template>
  <div class="form-group" :class="fg_class">
    <validation-provider :name="id" :rules="rules" v-slot="{ errors, required }">
      <label v-if="show_label" :for="id"><slot></slot>
        <span v-if="required" class="text-danger"> *</span>
      </label>
      <input class="form-control lowercase" :disabled="disabled || hasFormBeenPrinted" :id="id" :placeholder="placeholder" type="text" v-model="attribute">
      <div class="small text-danger">{{ errors[0] }}</div>
    </validation-provider>
  </div>
</template>
<script>
  import FieldCommon from "@/components/questions/FieldCommon";
  export default {
    name: "EmailField",
    mixins: [ FieldCommon ],
    props: {
      placeholder: String,
    },
  }
</script>