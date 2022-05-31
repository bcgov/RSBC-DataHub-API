<template>
  <text :x="adjustedStart.x" :y="adjustedStart.y"
        class="memoText"
        :id="field_name"
        fill="darkblue">{{ renderValue }}
  </text>
</template>

<script>
import RenderCommon from "@/components/print/RenderCommon";

export default {
  mixins: [RenderCommon],
  name: "MemoComponent",
  props: {
    value: {
      type: String
    }
  },
  computed: {
    renderValue() {
      const value = this[this.field.function](this.getPath, this.field.parameters)
      if (value) {
        return value
      } else {
        return ''
      }
    }
  }
}
</script>

<style>
 .memoText {
   font-size: 2pt;
 }
</style>