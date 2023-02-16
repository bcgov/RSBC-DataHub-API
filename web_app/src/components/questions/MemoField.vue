<template>
  <div v-if="visible" class="form-group" :class="fg_class">
    <validation-provider :name="id" :rules="rules" v-slot="{ errors }">
      <label v-if="show_label" :for="id">
        <slot></slot>
        <span v-if="!isShowOptional" class="text-danger"> *</span>
      </label>
      <div style="float:right">
        <span class="text-dark" > {{ charsRemaining }} / {{  max_length }}</span><span class="small text-muted"> &nbsp;characters</span>
      </div>
      <textarea class="form-control" :class="errors.length > 0 ? fe_class + 'border-danger bg-warning' : fe_class" :disabled="disabled || hasFormBeenPrinted" :id="id" @input="assertMaxChars()" :placeholder="placeholder" rows="5" v-model="attribute"></textarea>
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
      charsRemaining() {
        return (this.getAttributeValue(this.path, this.id) !== undefined) ? this.getAttributeValue(this.path, this.id).length : 0;
      },
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
      ]),
      assertMaxChars() {
        if (this.attribute.length >= this.max_length) {
          this.attribute = this.attribute.substring(0, this.max_length);
        }
      }
    },
    mixins: [ FieldCommon ],
    props: {
      max_length: String,
      placeholder: String,
    }
  }
</script>