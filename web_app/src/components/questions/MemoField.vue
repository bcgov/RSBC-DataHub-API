<template>
  <div v-if="visible" class="form-group" :class="fg_class">
    <validation-provider :name="id" :rules="rules" v-slot="{ errors }">
      <label v-if="show_label" :for="id">
        <slot></slot>
        <span v-if="!isShowOptional" class="text-danger"> *</span>
      </label>
      <textarea class="form-control" :class="errors.length > 0 ? fe_class + 'border-danger bg-warning' : fe_class" :disabled="disabled || hasFormBeenPrinted" :id="id" :placeholder="placeholder" rows="10" v-model="attribute"></textarea>
      <div class="small text-danger">{{ errors[0] }}</div>
    </validation-provider>
  </div>
</template>
<script>
  import FieldCommon from "@/components/questions/FieldCommon";
  import { mapGetters, mapMutations } from "vuex";
  export default {
    name: "MemoField",
    computed: {
      ...mapGetters([
        "getAttributeValue",
        "hasFormBeenPrinted"
      ]),
      isShowOptional() {
        if (this.rules) {
          return ! this.rules.includes('required');
        }
          return true;
        }
    },
    methods: {
      ...mapMutations([
        "updateFormField"
      ])
    },
    mixins: [ FieldCommon ],
    props: {
      placeholder: String,
    }
  }
</script>