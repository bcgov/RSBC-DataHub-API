<template>
  <div>
    <shadow-box>
      <form-row>
         <multiselect v-model="query"
                      @input="typeAheadUpdate"
                   tag-placeholder="That's not an option"
                   :disabled="disabled || hasFormBeenPrinted"
                   placeholder="Search for an Impound Lot Operator"
                   :options="getArrayOfImpoundLotOperators"></multiselect>
      </form-row>
        <form-row>
          <text-field id="name" rules="required"
                      :disabled="disabled || hasFormBeenPrinted"
                      :path="getPath"
                      fg_class="col-sm-12">Impound Lot Operator Name</text-field>
          <text-field id="lot_address"
                      :disabled="disabled || hasFormBeenPrinted"
                      rules="required"
                      :path="getPath"
                      fg_class="col-sm-5">Public lot address</text-field>
          <text-field id="city"
                      :disabled="disabled || hasFormBeenPrinted"
                      rules="required"
                      :path="getPath"
                      fg_class="col-sm-4">City</text-field>
          <text-field id="phone"
                      :disabled="disabled || hasFormBeenPrinted"
                      rules="required"
                      :path="getPath"
                      fg_class="col-sm-3">Public phone</text-field>
        </form-row>
    </shadow-box>
  </div>

</template>

<script>


import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters} from 'vuex';
import FormRow from "@/components/forms/FormRow";
import TextField from "@/components/questions/TextField";
import ShadowBox from "@/components/forms/ShadowBox";

export default {
  name: "ImpoundLotOperator",
  mixins: [FieldCommon],
  props: {
    id: {
      type: String,
      default: 'impound_lot_operator'
    },
    suggestions: {
      default: Array
    },
    path: {
      type: String
    }
  },
  data(){
      return {
        query: '',
      }
    },
  computed: {
    ...mapGetters(["getAttributeValue", "hasFormBeenPrinted", "getArrayOfImpoundLotOperators", "getImpoundLotOperatorObject"]),
    getPath() {
      return this.path + "/" + this.id
    }
  },
  methods: {
    typeAheadUpdate(e) {
      const ilo_object = this.getImpoundLotOperatorObject(e)
      const payload = {target: {value: ilo_object, path: this.path, id: this.id }}
      this.updateFormField(payload)
      this.query = ''
    }
  },
  components: {
    ShadowBox,
    FormRow,
    TextField
  }
}
</script>