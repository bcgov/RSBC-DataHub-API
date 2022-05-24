<template>
  <text :x="adjustedStart.x" :y="adjustedStart.y"
        class="fontText"
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