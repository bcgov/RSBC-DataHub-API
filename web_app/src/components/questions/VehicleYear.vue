<template>
  <div class="form-group" :class="fg_class">
    <label :for="id">Vehicle Year</label>
    <multiselect :id="id" @input="updateVehicle" :options="getArrayOfVehicleYears" placeholder="Select a vehicle year" tag-placeholder="That year isn't found" :value="getAttributeValue(path, id)"></multiselect>
  </div>
</template>
<script>
  import FieldCommon from "@/components/questions/FieldCommon";
  import { mapGetters } from "vuex";
  export default {
    name: "VehicleYear",
    computed: {
      ...mapGetters([
        "getArrayOfVehicleYears"
      ])
    },
    methods: {
      updateVehicle(event) {
        console.log("updateVehicle()", event)
        const payload = {
          "target": {
            "id": this.id,
            "path": this.path,
            "value": event
          }
        }
        console.log("Payload is: " + payload);
        this.updateFormField(payload);
      }
    },
    mixins: [ FieldCommon ],
    props: {
      id: {
        default: 'vehicle_year',
        type: String
      }
    },
  }
</script>
<style scoped>
  .form-group label {
    padding-bottom: 0.7em;
  }
</style>