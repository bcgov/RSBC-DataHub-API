<template>
  <div>
    <shadow-box class="bg-info p-3">
      <form-row>
         <multiselect id="ilo_multiselect" :disabled="disabled || hasFormBeenPrinted" @input="typeAheadUpdate" :options="getArrayOfImpoundLotOperators" placeholder="Search for an Impound Lot Operator" v-model="query"></multiselect>
      </form-row>
    </shadow-box>
    <br />
    <shadow-box class="p-3" style="background-color: lightgray;">
      <form-row>
          <text-field id="name" :disabled="disabled || hasFormBeenPrinted" fe_class="uppercase" fg_class="col-sm-12" :path="getPath" rules="required">Impound Lot Operator Name</text-field>
          <text-field id="lot_address" :disabled="disabled || hasFormBeenPrinted" fe_class="uppercase" fg_class="col-sm-5" :path="getPath" rules="required" >Public Lot Address</text-field>
          <text-field id="city" :disabled="disabled || hasFormBeenPrinted" fe_class="uppercase" fg_class="col-sm-4" :path="getPath" rules="required">City</text-field>
          <text-field id="phone" :disabled="disabled || hasFormBeenPrinted" fg_class="col-sm-3" input_mask="###-###-####" :path="getPath" rules="required">Public Phone Number</text-field>
      </form-row>
    </shadow-box>
  </div>
</template>
<script>
  import FieldCommon from "@/components/questions/FieldCommon";
  import FormRow from "@/components/forms/FormRow";
  import ShadowBox from "@/components/forms/ShadowBox";
  import TextField from "@/components/questions/TextField";
  import { mapGetters } from 'vuex';
  export default {
    name: "ImpoundLotOperator",
    components: {
      FormRow,
      ShadowBox,
      TextField
    },
    computed: {
      ...mapGetters([
        "hasFormBeenPrinted",
        "getAttributeValue",
        "getArrayOfImpoundLotOperators",
        "getImpoundLotOperatorObject"
      ]),
      getPath() {
        return this.path + "/" + this.id
      }
    },
    data(){
      return {
        query: '',
      }
    },
    methods: {
      typeAheadUpdate(e) {
        const ilo_object = this.getImpoundLotOperatorObject(e);
        const payload = {
          target: {
            value: ilo_object,
            path: this.path,
            id: this.id
          }
        };
        this.updateFormField(payload);
        this.query = '';
      }
    },
    mixins: [ FieldCommon ],
    props: {
      id: {
        default: 'impound_lot_operator',
        type: String
      },
      suggestions: {
        default: Array
      },
      path: {
        type: String
      }
    },
  }
</script>