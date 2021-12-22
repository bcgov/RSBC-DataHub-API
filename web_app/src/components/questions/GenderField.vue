<template>
<div class="form-group" :class="form_group_class">
  <label class="small" :for="form_group.id">{{ form_group.label }}
    <span v-if="isFieldRequired" class="text-danger">*</span>
  </label>
  <select :type="form_group.input_type"
         :class="errorClass"
         class="form-control form-control-sm"
         :id="form_group.id"
         :placeholder="form_group.placeholder"
          :value="form_group.value"
          @input="update">
      <option>Male</option>
      <option>Female</option>
      <option>Other</option>
  </select>
  <div v-if="fieldHasErrors" class="small text-danger">{{ errorMessage }}</div>
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";

export default {
  name: "GenderField",
  mixins: [FieldCommon]

}
</script>
