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
   font-size: 2pt;
 }
</style>