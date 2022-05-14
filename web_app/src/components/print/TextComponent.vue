<template>
  <text :x="adjustedStart.x" :y="adjustedStart.y" v-if="renderValue"
        :class="fontSizeClass"
        fill="darkblue">{{ renderValue }}
  </text>
</template>

<script>

import RenderCommon from "@/components/print/RenderCommon";

export default {
  mixins: [RenderCommon],
  name: "TextComponent",
  computed: {
    fontSizeClass() {
      if (this.field.font_size === 14) {
        return "fontMedium"
      }
      if (this.field.font_size === 8) {
        return "fontSmall"
      }
      return "fontText"
    }
  }
}
</script>

<style scoped>
  .fontMedium {
    font-size: 3pt;
  }
  .fontSmall {
    font-size: 2pt;
  }
</style>