<template>
  <div>
    <form-row>
      <div v-if="visible" class="form-group" :class="fg_class">
        <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
          <span v-if="required" class="small text-danger"> *</span>
          <vue-typeahead-bootstrap
              :input-class="errors.length > 0 ? 'border-danger bg-warning' : ''"
              @hit="typeAheadUpdate"
              placeholder="Search for an impound lot operator"
              v-model="query"
              :data="getArrayOfImpoundLotOperators"
              :disabled="disabled || hasFormBeenPrinted"
              :inputName="id + '_typeahead'" />
          <div class="small text-danger">{{ errors[0] }}</div>
        </validation-provider>
        <shadow-box class="mt-3">
          <form-row>
            <text-field id="ilo_name" :disabled="true"
                        :placeholder="getAttributeValue(id).name"
                        fg_class="col-sm-12">Impound Lot Operator Name</text-field>
          </form-row>
          <form-row>
            <text-field id="ilo_address" :disabled="true"
                        :placeholder="getAttributeValue(id).lot_address"
                        fg_class="col-sm-5">Public lot address</text-field>
            <text-field id="ilo_city" :disabled="true"
                        :placeholder="getAttributeValue(id).city"
                        fg_class="col-sm-4">City</text-field>
            <text-field :id="ilo_phone" :disabled="true"
                        :placeholder="getAttributeValue(id).phone"
                        fg_class="col-sm-3">Public phone</text-field>
          </form-row>
        </shadow-box>
      </div>
    </form-row>
  </div>

</template>

<script>


import VueTypeaheadBootstrap from 'vue-typeahead-bootstrap';
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
    }
  },
  data(){
      return {
        query: '',
      }
    },
  computed: {
    ...mapGetters(["getAttributeValue", "hasFormBeenPrinted", "getArrayOfImpoundLotOperators", "getImpoundLotOperatorObject"]),
  },
  methods: {
    typeAheadUpdate(e) {
      const ilo_object = this.getImpoundLotOperatorObject(e)
      const payload = {target: {value: ilo_object, id: this.id }}
      this.$store.commit("updateFormField", payload)
    }
  },
  components: {
    ShadowBox,
    FormRow,
    TextField,
    VueTypeaheadBootstrap
  }
}
</script>