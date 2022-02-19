<template>
  <div v-if="visible" class="form-group" :class="fg_class">
    <validation-provider :rules="rules" :name="id" v-slot="{ errors }">
      <label :for="id"><slot></slot>
        <span class="small text-muted"> HHMM in Pacific Time</span>
      </label>
      <div class="col-xs-10">
        <div class="form-row">
            <input type="text"
                   :id="id"
                   class="form-control "
                      :class="errors.length > 0 ? 'border-danger bg-warning' : ''"
                   :disabled="disabled"
                   placeholder="HHMM"
                   :name="id"
                   v-model="attribute">
        </div>
        <div class="small text-danger ml-1">{{ errors[0] }}</div>
      </div>
    </validation-provider>
  </div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters, mapMutations} from "vuex";

export default {
  name: "TimeField",
  mixins: [FieldCommon],
   computed: {
     ...mapGetters(["getAttributeValue"])
   },
  methods: {
    ...mapMutations(["updateFormField"])
  }

}
</script>
