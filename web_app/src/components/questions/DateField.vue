<template>
  <div v-if="visible" class="form-group" :class="fg_class">
    <validation-provider :name="id" :rules="rules" v-slot="{ errors, required }">
      <label :for="id">
        <slot></slot>
        <span v-if="required" class="text-danger"> *</span>
        <span class="small text-muted"> YYYYMMDD</span>
      </label>
      <b-input-group class="mb-3">
        <b-form-input autocomplete="off" :id="id" placeholder="YYYYMMDD" type="text" v-mask="'########'" v-model="attribute"></b-form-input>
        <b-input-group-append>
          <b-form-datepicker button-only :disabled="disabled || hasFormBeenPrinted" :id="id + '_button'" @input="updateDate" label-reset-button="Clear" locale="en-CA" right reset-button></b-form-datepicker>
        </b-input-group-append>
      </b-input-group>
      <div class="small text-danger ml-1">{{ errors[0] }}</div>
    </validation-provider>
  </div>
</template>
<script>
  import FieldCommon from "@/components/questions/FieldCommon";
  import { mapGetters, mapMutations } from "vuex";
  export default {
    name: "DateField",
    computed: {
      ...mapGetters([
        "getAttributeValue",
        "hasFormBeenPrinted"
      ]),
      getDatePickerValue() {
        const dateString = this.getAttributeValue(this.path, this.id);
        if (dateString) {
          return dateString.slice(0,4) + '-' + dateString.slice(5,2) + '-' + dateString.slice(7,2);
        } else {
          return '';
        }
      }
    },
    methods: {
      ...mapMutations([
        "updateFormField"
      ]),
      updateDate(event) {
        const payload = {"target": {
          "id": this.id,
          "path": this.path,
          "value": event.replace(/-/gi, "")
        }}
        this.updateFormField(payload);
      },
    },
    mixins: [ FieldCommon ]
  }
</script>