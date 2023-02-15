<template>
  <div v-if="visible" class="form-group" :class="fg_class">
    <label v-if="show_label" :for="id">
      <slot></slot>
    </label>
    <span class="small text-danger"> *</span>
    <input :type="input_type" class="form-control" :class="localErrors.length > 0 ? fe_class + 'border-danger bg-warning' : fe_class" :id="id" :disabled="disabled" :placeholder="placeholder" @change="modified" v-model="attribute" />
    <div class="small text-danger">{{ localErrors[0] }}</div>
  </div>
</template>

<script>
  import Vue from 'vue'
  export default {
    name: "ApplicationField",
    data() {
      return {
        attribute: ''
      }
    },
    props: {
      disabled: {
        default: false,
        type: Boolean
      },
      errors: [],
      fg_class: String,
      fe_class: String,
      id: String,
      input_type: {
        type: String,
        default: 'text'
      },
      placeholder: String,
      show_label: {
        type: Boolean,
        default: true
      },
      visible: {
        type: Boolean,
        default: true
      }
    },
    computed: {
      localErrors() {
        if (this.id in this.errors) {
          return this.errors[this.id]
        } else {
          return []
        }
      }
    },
    methods: {
      modified() {
        Vue.set(this.errors, this.id, [])
        this.$emit('modified', {
          id: this.id,
          value: this.attribute
        });
      }
    }
  }
</script>