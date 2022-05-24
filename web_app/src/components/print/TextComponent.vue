<template>
  <text :x="adjustedStart.x" :y="adjustedStart.y" v-if="renderValue"
        :class="fontSizeClass"
        fill="darkblue">{{ renderValue }}
  </text>
</template>

<script>

import RenderCommon from "@/components/print/RenderCommon";
import moment from "moment-timezone";

export default {
  mixins: [RenderCommon],
  name: "TextComponent",
  computed: {
    renderValue() {
      if (this.field.function) {
        const value = this[this.field.function](this.getPath, this.field.parameters)
        if (value) {
          return value.toUpperCase()
        }
        return ''
      }
      return "txt()"
    },
  },
  methods: {
    getValuesConcatenatedWithCommas(form_path, attributes_array) {
      let attributeValues = []
      attributes_array.forEach( (attribute) => {
          let value = this.getStringValue(form_path, attribute)
          if (value) {
              attributeValues.push(value)
          }
      })
      return attributeValues.join(", ")
    },

    getFormattedDate(form_path, [attribute, format_string]) {
      let value = this.getStringValue(form_path, attribute)
      if (value) {
        const date_time = moment(value, 'YYYYMMDD', true)
        return date_time.format(format_string)
      }
      return ''
    },

    getFormattedTime(form_path, [attribute, format_string]) {
      let value = this.getStringValue(form_path, attribute)
      if (value) {
        const date_time = moment(value, 'HHmm', true)
        return date_time.format(format_string)
      }
      return ''
    },

    getAreaCode(form_path, attribute) {
      let value = this.getStringValue(form_path, attribute)
      if (value) {
        return value.substr(0,3)
      }
      return ''
    },

    getPhone(form_path, attribute) {
      let value = this.getStringValue(form_path, attribute)
      if (value) {
        return value.substr(4,3) + "-" + value.substr(6,9)
      }
      return ''
    },

    getJurisdictionCode(form_path, attribute) {
      return this.getStringValue(form_path + '/' + attribute, 'objectCd')
    },

    conditionalLabel(form_path, [attribute, label]) {
      if(this.isExists(form_path, attribute)) {
        return label
      }
      return ''
    },

    label(form_path, attribute) {
      return attribute
    },

    concatenateDateAndTime(form_path, attributes_array) {
      let dateValue = this.getStringValue(form_path, attributes_array[0])
      let timeValue = this.getStringValue(form_path, attributes_array[1])
      if (dateValue && timeValue) {
          const date_time = moment(dateValue + ' ' + timeValue, 'YYYYMMDD HHmm', true)
          return date_time.format("YYYY-MM-DD HH:mm")
      }
      return ' ';
    },

    getStringValueWithSuffix(form_path, attribute_array) {
      let value = this.getStringValue(form_path, attribute_array[0])
      if (value) {
        return value + ' ' + attribute_array[1]
      }
      return ''
    },


  }
}
</script>

<style scoped>
  .fontLarge {
    font-size: 3.5pt;
  }
  .fontMedium {
    font-size: 3pt;
  }
  .fontSmall {
    font-size: 2pt;
  }
</style>