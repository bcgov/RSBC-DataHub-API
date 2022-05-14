<template>
  <text :x="adjustedStart.x" :y="adjustedStart.y" v-if="renderValue"
        class="fontText"
        fill="darkblue">&#10004;
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
  }
}
</script>

<style scoped>

   .fontText {
       font-size: 5pt;
   }

</style>