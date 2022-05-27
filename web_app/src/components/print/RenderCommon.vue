<script>

import {mapGetters} from 'vuex';
import checkDigit from "@/helpers/checkDigit";

export default {
  name: "RenderCommon",
  props: {
    start: {
      type: Object
    },
    field: {
      type: Object
    },
    form_type: {
      type: String
    },
    form_id: {
      type: String
    },
    form_data: {
      type: Object
    },
    field_name: {
      type: String
    }
  },
  computed: {
    ...mapGetters(["getAttributeValue"]),
    fontSizeClass() {
      if (this.field.font_size >= 12) {
        return "fontLarge"
      }
      if (this.field.font_size > 10 && this.field.font_size < 12) {
        return "fontMedium"
      }
      if (this.field.font_size <= 10 ) {
        return "fontSmall"
      }
      return "fontText"
    },
    adjustedStart() {
      // Temporary workaround while determining how x,y coordinates should be adjusted for SVG
      if (this.form_type === "VI") {
        return {
          x: this.start.x,
          y: this.start.y + 10
        }
      }
      if (this.form_type === "24Hour") {
        return {
          x: this.start.x - 26,
          y: this.start.y - 5.5
        }
      }
      if (this.form_type === "12Hour") {
        return {
          x: this.start.x - 24,
          y: this.start.y - 0
        }
      }
      return {
        x: this.start.x,
        y: this.start.y
      }
    },
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
    getPath() {
      return `forms/${this.form_type}/${this.form_id}/data`
    },
  },
  methods: {
    getStringValue(form_path, path_and_attribute) {
      let pathArray = form_path.split("/")
      pathArray = pathArray.concat(path_and_attribute.split('/'))
      const attribute = pathArray.pop()
      const path = pathArray.join("/")
      return this.getAttributeValue(path, attribute);
    },

    getFormattedFormId() {
      const sixDigitString = this.form_id.substr(2,7)
      return this.form_id.substr(0,2) + "-" + sixDigitString

    },

    getFormIdWithCheckDigit() {
      const sixDigitString = this.form_id.substr(2,7)
      const digit = checkDigit.checkDigit(sixDigitString)
      return this.form_id.substr(0,2) + "-" + sixDigitString + digit

    },

    getFormIdForBarCode() {
        const sixDigitString = this.form_id.substr(2,7)
        const digit = checkDigit.checkDigit(sixDigitString)
        return "*" + sixDigitString + digit + "*"
    },

    isExists(form_path, attribute) {
      return this.getStringValue(form_path, attribute) !== undefined
    },

    isMultipleExists(form_path, attributes_array) {
      attributes_array.forEach( (attribute) => {
        if( ! this.isExists(form_path, attribute)) {
          return false
        }
      })
      return true
    }


  }
}
</script>

<style scoped>
   .fontText {
       font-size: 3pt;
   }
</style>
