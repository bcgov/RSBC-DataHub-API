<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
    <div class="d-flex justify-content-between mb-2">
      <div>
        <label :for="id">Vehicle Style
          <span v-if="required" class="text-danger"> *</span>
        </label>
      </div>
      <b-button v-b-modal:vehicle-style class="btn btn-primary">Edit</b-button>
    </div>
    <multiselect :value="getAttributeValue(path, id)"
                   @input="updateStyle"
                   :disabled="disabled || hasFormBeenPrinted"
                   tag-placeholder="That style isn't an option"
                   placeholder="Search for a vehicle style"
                   label="name"
                   track-by="code"
                   :options="getArrayOfVehicleStyles"></multiselect>
    <div class="small text-danger">{{ errors[0] }}</div>
  </validation-provider>
  <!-- Modal Start -->
  <b-modal id="vehicle-style" title="Choose a vehicle style" :ok-only="true" size="lg" :hide-header="true">
    <div class="card">
      <div class="card-body">
        <b-container>
          <b-row v-for="(row, key) in rows" :key="key">
            <style-card
               :vehicle_style="style"
               :selected="getAttributeValue(path, id)"
               @toggle-style="toggleStyle"
               v-for="style in row" :key="style.code">
            </style-card>
          </b-row>
        </b-container>
      </div>
    </div>

  </b-modal>
  <!-- Modal End -->
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters} from "vuex";
import StyleCard from "@/components/questions/VehicleStyle/StyleCard";

export default {
  name: "VehicleStyle",
  components: {StyleCard},
  mixins: [FieldCommon],
  props: {
    id: {
      type: String,
      default: "vehicle_type"
    },
    placeholder: String,
    default_value: {
      type: String
    },
    input_type: {
      type: String,
      default: "text"
    },

  },
  computed: {
    ...mapGetters(["getAttributeValue", "hasFormBeenPrinted", "getArrayOfVehicleStyles"]),
    rows() {
      let rows = []
      let rowCount = Math.ceil(this.getArrayOfVehicleStyles.length / this.maxColumns)
      for (let row = 0; row < rowCount; row++) {
        rows.push(this.getArrayOfVehicleStyles.slice(row * this.maxColumns, row * this.maxColumns + this.maxColumns ))
      }
      return rows
    }
  },
  methods: {
    toggleStyle(event) {
      const currentValue = this.getAttributeValue(this.path, this.id);
      if(currentValue && event.code === currentValue.code) {
        console.log("removeStyle()", event)
        // remove selection
        this.updateStyle(null)
      } else {
        console.log("toggleStyle()", event)
        this.updateStyle(event);
      }

    },
    updateStyle(event) {
      console.log("updateStyle()", event, this.path, this.id)
      const payload = {
        "target": {
          "path": this.path,
          "id": this.id,
          "value": event
        }
      }
      this.updateFormField(payload)
    }
  },
  data() {
    return {
      maxColumns: 3
    }
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

