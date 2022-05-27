<template>
  <text :x="adjustedStart.x" :y="adjustedStart.y" v-if="renderValue"
        class="fontText"
        :id="field_name"
        fill="darkblue">{{ renderValue }}
  </text>
</template>

<script>
import RenderCommon from "@/components/print/RenderCommon";

export default {
  name: "BarcodeComponent",
  mixins: [RenderCommon],
  props: {
    value: {
      type: String
    }
  }
}
</script>

<style scoped>

  .fontText {
    font-family: "barcode",serif;
    font-weight: normal;
    font-size: 14pt;
  }

</style>