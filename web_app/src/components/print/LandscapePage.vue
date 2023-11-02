<template>
    <svg v-if="formData" class="svg-wrapper" :viewBox="viewbox">
      <image :href="baseURL + page.image.filename" :height="page.image.height + 'px'" :width="page.image.width + 'px'"/>
      <component
        v-for="(field, index) in fieldsToShow"
        v-bind:key="index"
        :is="fields[field].field_type + 'Component'"
        :start="fields[field].start"
        :field="fields[field]"
        :form_type="form_type"
        :form_id="form_id"
        :field_name="field"
        :form_data="formData">
      </component>
     Sorry, your browser does not support inline SVG.
    </svg>
</template>
<script>
import PageCommon from "@/components/print/PageCommon";
export default {
  name: "LandscapePage",
  mixins: [PageCommon]
}
</script>
<style scoped type="text/css">
@media print {
  html {
    margin: 0;
  }
  body {
    margin: 0;
  }
  #roadsafety-header {
   display: none;
  }
  #debug-component {
   display: none;
  }
  #not-logged-in-banner {
   display: none;
  }
  #end-of-life-banner {
   display: none;
  }
  .svg-wrapper {
    page-break-before:always;
    transform: rotate(-90deg) scale(1.2) translate(-200px);
  }
  @page {
    size: letter;
    margin: 0;
  }
}
</style>