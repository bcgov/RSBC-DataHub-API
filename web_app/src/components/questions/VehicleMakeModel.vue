<template>
  <div class="form-group" :class="fg_class">
    <validation-provider :name="id" :rules="rules" v-slot="{ errors, required }">
      <label :for="id">Vehicle Make and Model
        <span v-if="required" class="text-danger"> *</span>
      </label>
      <multiselect :id="id" @input="updateVehicle" label="search" :options="getArrayOfVehicleMakeModel" placeholder="Search for a vehicle make and model" tag-placeholder="That make and model isn't found" track-by="search" :value="getAttributeValue(path, id)"></multiselect>
      <div class="small text-danger">{{ errors[0] }}</div>
    </validation-provider>
  </div>
</template>
<script>
  import FieldCommon from "@/components/questions/FieldCommon";
  import { mapGetters } from "vuex";
  export default {
    name: "VehicleMakeModel",
    computed: {
      ...mapGetters([
          "getArrayOfVehicleMakeModel"
      ])
    },
    methods: {
      updateVehicle(event) {
        const payload = {
          "target": {
            "path": this.path,
            "id": this.id,
            "value": event
          }
        }
        this.updateFormField(payload);
      }
    },
    mixins: [ FieldCommon ],
    props: {
      id: {
        default: 'vehicle_make',
        type: String
      }
    }
  }
</script>
<style scoped>
  .form-group label {
    padding-bottom: 0.7em;
  }
</style>