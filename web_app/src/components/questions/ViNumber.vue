<template>
  <div v-if="visible" class="form-group" :class="fg_class">
          <multiselect v-model="query"
                       @input="typeAheadUpdate"
                   id="vi_number_lookup"
                   label="label"
                   track-by="vi_number"
                   tag-placeholder="That's not an option"
                   :disabled="disabled || hasFormBeenPrinted"
                   placeholder="Search for recent VI number by driver's name"
                   :options="getArrayOfRecentViNumbers">
      </multiselect>
    <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
      <label :for="id"><slot></slot></label>
      <span v-if="required" class="small text-danger"> *</span>
        <input type="text"
         class="form-control"
         :class="errors.length > 0 ? 'border-danger bg-warning' : ''"
         :id="id"
         :disabled="disabled || hasFormBeenPrinted"
         v-model="attribute">
      <div class="small text-danger">{{ errors[0] }}</div>
    </validation-provider>
  </div>
</template>

<script>


import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters} from 'vuex';

export default {
  name: "ViNumber",
  mixins: [FieldCommon],
  props: {
    id: {
      type: String,
      default: "vi_number"
    },
    suggestions: {
      default: Array
    }
  },
  data() {
    return {
      query: ''
    }
  },
  computed: {
    ...mapGetters(["getAttributeValue", "hasFormBeenPrinted", "getArrayOfRecentViNumbers"]),

  },
  methods: {
    typeAheadUpdate(e) {
      const payload = {target: {value: e.vi_number, path: this.path, id: this.id }}
      this.updateFormField(payload)
      this.query = ''
    }
  },
}
</script>