<template>
  <text :x="adjustedStart.x" :y="adjustedStart.y" v-if="renderValue"
        :class="field.class"
        :id="field_name"
        fill="darkblue">{{ renderValue }}
  </text>
</template>

<script>
import RenderCommon from "@/components/print/RenderCommon";
import checkDigit from "@/helpers/checkDigit";

export default {
  name: "BarcodeComponent",
  mixins: [RenderCommon],
  props: {
    value: {
      type: String
    }
  },
  methods: {
    getFormIdForBarCode() {
        const sixDigitString = this.form_id.substr(2,7)
        const digit = checkDigit.checkDigit(sixDigitString)
        return "*" + sixDigitString + digit + "*"
    },
  }
}
</script>

<style scoped>

  .font12 {
    font-family: "barcode",serif;
    font-weight: normal;
    font-size: 12pt;
  }

  .font14 {
    font-family: "barcode",serif;
    font-weight: normal;
    font-size: 14pt;
  }

</style>