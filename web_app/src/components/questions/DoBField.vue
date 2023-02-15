<template>
  <div class="form-group" :class="fg_class">
    <validation-provider :name="id" rules="validDt|dob" v-slot="{ errors, required }">
      <label v-if="show_label" :for="id">
        Date of Birth
        <span class="small text-muted"> YYYYMMDD</span>
        <span v-if="required" class="text-danger"> *</span>
        <span v-if="isValidDate" class="text-muted"> ({{ yearsOld }} yrs)</span>
      </label>
      <div class="col-xs-10">
        <input class="form-control" :class="errors.length > 0 ? 'border-danger bg-warning' : ''" :disabled="disabled || hasFormBeenPrinted" :id="id" placeholder="" type="text" v-mask="'########'" v-model="attribute">
        <div class="small text-danger">{{ errors[0] }}</div>
      </div>
    </validation-provider>
  </div>
</template>
<script>
  import moment from 'moment';
  import FieldCommon from "@/components/questions/FieldCommon";
  import { mapGetters } from 'vuex';
  export default {
    name: "DoBField",
    computed: {
      ...mapGetters([
        "getAttributeValue",
        "hasFormBeenPrinted"
      ]),
      isValidDate() {
        return moment(this.getAttributeValue(this.path, this.id)).isValid();
      },
      yearsOld() {
        return moment().diff(moment(this.getAttributeValue(this.path, this.id)), 'years');
      }
    },
    mixins: [ FieldCommon ]
  }
</script>