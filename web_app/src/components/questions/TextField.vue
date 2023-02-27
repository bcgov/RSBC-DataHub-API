<template>
  <div v-if="visible" class="form-group" :class="fg_class">
    <validation-provider :name="id" :rules="rules" v-slot="{ errors }">
      <label v-if="show_label" :for="id"><slot></slot>
        <span v-if="!isShowOptional" class="text-danger"> *</span>
        <span v-if="!!hint_text" class="small text-muted"> {{ hint_text }}</span>
      </label>
      <input class="form-control" :class="errors.length > 0 ? fe_class + 'border-danger bg-warning' : fe_class" :disabled="disabled || hasFormBeenPrinted" :id="id" :placeholder="placeholder" :type="input_type" v-mask="input_mask" v-model="attribute">
      <div class="small text-danger">
        {{ errors[0] }}
      </div>
    </validation-provider>
  </div>
</template>
<script>
  import FieldCommon from "@/components/questions/FieldCommon";
  import { mapGetters } from "vuex";
  export default {
    name: "TextField",
    computed: {
      ...mapGetters([
          "getAttributeValue",
          "hasFormBeenPrinted"
      ]),
    },
    mixins: [ FieldCommon ],
    mounted() {
      if(this.default_value) {
        this.attribute = this.default_value;
      }
    },
    props: {
      default_value: {
        type: String
      },
      hint_text: String,
      input_mask: String,
      input_type: {
        default: "text",
        type: String
      },
      placeholder: String
    }
  }
</script>