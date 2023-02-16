<template>
  <div v-if="visible" class="form-group" :class="fg_class">
    <validation-provider :name="id" :rules="rules" v-slot="{ errors, required }">
      <label v-if="show_label" :for="id"><slot></slot>
        <span v-if="required" class="text-danger"> *</span>
      </label>
      <multiselect :disabled="disabled || hasFormBeenPrinted" :id="id" @input="updateProvinceByObject" label="objectDsc" :options="getArrayOfProvinces" placeholder="" track-by="objectCd" :value="getAndUpdateProvince()"></multiselect>
      <div class="small text-danger">{{ errors[0] }}</div>
    </validation-provider>
  </div>
</template>
<script>
  import FieldCommon from "@/components/questions/FieldCommon";
  import { mapGetters, mapMutations } from 'vuex';
  export default {
    name: "ProvinceField",
    computed: {
      ...mapGetters([
        "getArrayOfProvinces",
        "getAttributeValue",
        "hasFormBeenPrinted"
      ])
    },
    mixins: [ FieldCommon ],
    methods: {
      ...mapMutations([
        "updateFormField"
      ]),
      getAndUpdateProvince() {
        let province = this.getAttributeValue(this.path, this.id);
        if (typeof province  === "string") {
          this.updateProvinceByCode(province);
        }
        return province;
      },
      updateProvinceByCode(event) {
        const province = this.getArrayOfProvinces.filter(j => j.objectCd === event)[0];
        this.$store.commit("updateFormField", {
          target: {
            id: this.id,
            path: this.path,
            value: province
          }
        });
      },
      updateProvinceByObject(event) {
        const payload = {
          "target": {
            "id": this.id,
            "path": this.path,
            "value": event
          }
        }
        this.updateFormField(payload);
      },
    },
    mounted() {
      // set initial value to 'BC' if value not set
      if (this.defaultToBritishColumbia) {
        if (!this.getAttributeValue(this.path, this.id)) {
          this.updateProvinceByCode("BC");
        }
      }
    },
    props: {
      defaultToBritishColumbia: {
        default: true,
        type: Boolean
      }
    }
  }
</script>