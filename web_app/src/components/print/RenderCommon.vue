<script>

import printFunctions from "@/helpers/printFunctions";

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
    }
  },
  computed: {
    adjustedStart() {
      // Temporary workaround while determining how x,y coordinates should be adjusted
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
        console.log("renderValue()", this.field.parameters, this.form_data)
        return printFunctions[this.field.function](this.form_data, this.field.parameters)
      }
      return "fn()"
    }
  }
}
</script>

<style scoped>
   .fontText {
       font-size: 3pt;
   }
</style>
