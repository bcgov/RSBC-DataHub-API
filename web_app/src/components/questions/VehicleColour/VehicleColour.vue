<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors }">
      <div class="d-flex justify-content-between mb-2">
        <div>
          <label :for="id">Vehicle Colour(s)</label>
        </div>
        <b-button v-b-modal:vehicle-colour class="btn btn-primary">Edit</b-button>
      </div>
      <multiselect :value="getAttributeValue(path, id)"
                   @input="updateColor"
                   tag-placeholder="That colour isn't an option"
                   :disabled="disabled || hasFormBeenPrinted"
                   placeholder="Search for a car colour"
                   label="display_name"
                   track-by="code"
                   :options="colours"
                   :multiple="true" :taggable="true"></multiselect>
    <div class="small text-danger">{{ errors[0] }}</div>
  </validation-provider>
  <!-- Modal Start -->
  <b-modal id="vehicle-colour" title="Choose one or two colours" :ok-only="true" size="lg" :hide-header="true">
    <div class="card">
      <p class="card-header">
        <span class="h4">Selected Colour(s)</span>
        <span class="text-muted"> - click colour tiles below to add / remove</span>
      </p>
      <div class="card-body">
        <div class="h4" v-if="currentValue.length > 0">
          <multiselect :value="getAttributeValue(path, id)"
                       @input="updateColor"
                   tag-placeholder="That colour isn't an option"
                   placeholder="Search for a car colour"
                   label="display_name"
                   track-by="code"
                   :options="colours"
                   :multiple="true" :taggable="true"></multiselect>
        </div>
        <span class="text-muted" v-if="currentValue.length === 0">None selected</span>
      </div>
    </div>
    <b-container>
      <b-row v-for="(row, key) in rows" :key="key">
        <colour-sample :colour="colour"
                       :selected="getAttributeValue(path, id)"
                       @toggle-colour="toggleColour"
                       v-for="colour in row" :key="colour.code">
        </colour-sample>
      </b-row>
    </b-container>
  </b-modal>
  <!-- Modal End -->
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import {mapGetters} from "vuex";
import ColourSample from "@/components/questions/VehicleColour/ColourSample";

export default {
  name: "VehicleColour",
  components: {ColourSample},
  mixins: [FieldCommon],
  props: {
    id: {
      type: String,
      default: "vehicle_color"
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
    ...mapGetters(["getAttributeValue", "hasFormBeenPrinted"]),
    currentValue() {
        const value = this.getAttributeValue(this.path, this.id);
        if (value) {
          return value
        }
        return []
    },
    rows() {
      let rows = []
      let rowCount = Math.ceil(this.colours.length / this.maxColumns)
      for (let row = 0; row < rowCount; row++) {
        rows.push(this.colours.slice(row * this.maxColumns, row * this.maxColumns + this.maxColumns ))
      }
      return rows
    }
  },
  mounted() {
    if( ! this.getAttributeValue(this.path, this.id)) {
      this.updateColor([])
    }
  },
  methods: {
    toggleColour(colour) {
      const colourIndex = this.selectedColourIndex(colour)
      let localValue = this.getAttributeValue(this.path, this.id)
      if(colourIndex !== undefined) {
        console.log("colourIndex", colourIndex, colour)
        localValue.splice(colourIndex, 1)
      } else {
        if(localValue.length < 2) {
          localValue.push(colour)
        }
      }
      this.updateColor(localValue)
    },
    selectedColourIndex(colour) {
      let i;
      for(i = 0; i < this.currentValue.length; i++) {
        if(this.currentValue[i].code === colour.code) {
          return i;
        }
      }
      return undefined;
    },
    updateColor(event) {
      console.log("updateColor()", event, this.path, this.id)
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
      colours: [
       {
         "code": "BGE",
         "display_name": "BEIGE",
         "colour_class": "beige"
       },
       {
         "code": "BLK",
         "display_name": "BLACK",
         "colour_class": "black"
       },
       {
         "code": "BLU",
         "display_name": "BLUE",
         "colour_class": "blue"
       },
       {
         "code": "BRN",
         "display_name": "BROWN",
         "colour_class": "brown"
       },
       {
         "code": "BRZ",
         "display_name": "BRONZE",
         "colour_class": "bronze"
       },
       {
         "code": "BUR",
         "display_name": "BURGUNDY",
         "colour_class": "burgundy"
       },
       {
         "code": "CPR",
         "display_name": "COPPER",
         "colour_class": "copper"
       },
       {
         "code": "CRM",
         "display_name": "CREAM/IVORY",
         "colour_class": "ivory"
       },
       {
         "code": "DBL",
         "display_name": "DARK BLUE",
         "colour_class": "darkblue"
       },
       {
         "code": "DGR",
         "display_name": "DARK GREEN",
         "colour_class": "darkgreen"
       },
       {
         "code": "GLD",
         "display_name": "GOLD",
         "colour_class": "gold"
       },
       {
         "code": "GRN",
         "display_name": "GREEN",
         "colour_class": "green"
       },
       {
         "code": "GRY",
         "display_name": "GREY",
         "colour_class": "grey"
       },
       {
         "code": "LBL",
         "display_name": "LIGHT BLUE",
         "colour_class": "lightblue"
       },
       {
         "code": "LGR",
         "display_name": "LIGHT GREEN",
         "colour_class": "lightgreen"
       },
       {
         "code": "MRN",
         "display_name": "MAROON",
         "colour_class": "maroon"
       },
       {
         "code": "ONG",
         "display_name": "ORANGE",
         "colour_class": "orange"
       },
       {
         "code": "OTH",
         "display_name": "OTHER",
         "colour_class": "other"
       },
       {
         "code": "PLE",
         "display_name": "PURPLE",
         "colour_class": "purple"
       },
       {
         "code": "PNK",
         "display_name": "PINK",
         "colour_class": "pink"
       },
       {
         "code": "PRI",
         "display_name": "PRIMER",
         "colour_class": "primer"
       },
       {
         "code": "RED",
         "display_name": "RED",
         "colour_class": "red"
       },
       {
         "code": "SIL",
         "display_name": "SILVER",
         "colour_class": "silver"
       },
       {
         "code": "TAN",
         "display_name": "TAN",
         "colour_class": "tan"
       },
       {
         "code": "TRQ",
         "display_name": "TURQUOISE",
         "colour_class": "turquoise"
       },
       {
         "code": "WHI",
         "display_name": "WHITE",
         "colour_class": "white"
       },
       {
         "code": "YEL",
         "display_name": "YELLOW",
         "colour_class": "yellow"
       }
      ],
      maxColumns: 4
    }
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

