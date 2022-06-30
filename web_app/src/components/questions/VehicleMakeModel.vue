<template>
  <div class="form-group" :class="fg_class">
    <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
      <label :for="id">Vehicle Make and Model
        <span v-if="required" class="text-danger"> *</span>
      </label>
      <multiselect :value="getAttributeValue(path, id)"
                    :id="id"
                     @input="updateVehicle"
                     tag-placeholder="That make and model isn't found"
                     placeholder="Search for a vehicle make and model"
                     label="search"
                     track-by="search"
                     :options="getArrayOfVehicleMakeModel">
      </multiselect>
      <div class="small text-danger">{{ errors[0] }}</div>
    </validation-provider>
  </div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters} from "vuex";
export default {
  name: "VehicleMakeModel",
  mixins: [FieldCommon],
  props: {
    id: {
      type: String,
      default: 'vehicle_make'
    }
  },
  computed: {
    ...mapGetters(["getArrayOfVehicleMakeModel"])
  },
  methods: {
    updateVehicle(event) {
      console.log("updateVehicle()", event)
      const payload = {
        "target": {
          "path": this.path,
          "id": this.id,
          "value": event
        }
      }
      this.updateFormField(payload)
    }
  }

}
</script>

<style scoped>

.form-group label {
  padding-bottom: 0.7em;
}

</style>