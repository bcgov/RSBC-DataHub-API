<template>
  <switch>
    <foreignObject :x="adjustedStart.x" :y="adjustedStart.y" :width="field.max_width" :height="field.max_height">
      <p class="memoText" :id="field_name">{{ renderValue }}</p>
    </foreignObject>
  </switch>
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
  methods: {
    officerReport(form_path, attribute) {
      let result_string = ''
      let value = this.getStringValue(form_path, attribute)
      let video = this.isExists(form_path, "operating_grounds_video") ? ' VIDEO SURVEILLANCE. ' : undefined
      if (video) {
        result_string = video;
      }
      if (value) {
        result_string = result_string + value
      }
      return result_string
    },
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
   font-size: 2.5pt;
   color: darkblue;
   text-align: left;
 }
</style>