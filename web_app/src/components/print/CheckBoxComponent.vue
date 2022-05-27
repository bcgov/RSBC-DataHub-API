<template>
  <text :x="adjustedStart.x" :y="adjustedStart.y"
        class="fontText"
        :id="field_name"
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
  methods: {
    // temporary hack
    isExistsAndNotBc(form_path, [isExistsAttribute, jurisdictionCd]) {
      // the last item in the attributes_array is the attribute to display
      const jurisdiction = this.getStringValue(form_path, jurisdictionCd)
      if (jurisdiction && jurisdiction !== 'BC') {
        if (this.isExists(form_path, isExistsAttribute)) {
          return true;
        }
      }
      return false;
    }
  },
  computed: {
    renderValue() {
      if (this.field.function) {
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