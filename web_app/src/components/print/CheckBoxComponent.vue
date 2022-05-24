<template>
  <text :x="adjustedStart.x" :y="adjustedStart.y"
        class="fontText"
        fill="darkblue" v-html="renderValue">
  </text>
</template>

<script>
import RenderCommon from "@/components/print/RenderCommon";

export default {
  mixins: [RenderCommon],
  name: "CheckboxComponent",
  props: {
    value: {
      type: String
    }
  },
  computed: {
    renderValue() {
      if (["isExists"].includes(this.field.function)) {
        if (this[this.field.function](this.getPath, this.field.parameters)) {
          return "&#10004;"
        }
      } else {
        return '?'
      }
      return ""
    },
  }
}
</script>

<style scoped>

   .fontText {
       font-size: 5pt;
   }

</style>