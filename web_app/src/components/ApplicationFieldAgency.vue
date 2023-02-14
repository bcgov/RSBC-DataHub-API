<template>
  <div v-if="visible" class="form-group" :class="fg_class">
    <label :for="id">
      <slot></slot>
    </label>
    <span class="small text-danger"> *</span>
    <multiselect :class="localErrors.length > 0 ? 'border-danger bg-warning' : ''" :id="id" placeholder="" @input="modified" v-model="attributeAgency" label="agency_name" track-by="vjur" :options="getArrayOfAgencies">
    </multiselect>
    <div class="small text-danger">{{ localErrors[0] }}</div>
  </div>
</template>

<script>
  import Vue from 'vue'
  import FieldCommon from "@/components/questions/FieldCommon";
  import { mapGetters } from 'vuex';
  export default {
    name: "ApplicationFieldAgency",
    mixins: [FieldCommon],
    data() {
      return {
        attributeAgency: ''
      }
    },
    props: {
      errors: [],
      fg_class: String,
      id: {
        type: String,
        default: "agency_name"
      },
      show_label: {
        type: Boolean,
        default: true
      },
      visible: {
        type: Boolean,
        default: true
      },
    },
    computed: {
      ...mapGetters(["getArrayOfAgencies"]),
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
          id: "agency",
          value: this.attributeAgency.agency_name
        });
      }
    }
  }
</script>