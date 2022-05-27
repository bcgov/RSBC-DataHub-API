<template>
  <div v-if="formData" class="svg-wrapper">
    <svg width="100%" :viewBox="viewbox">
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
  </div>
</template>

<script>

import PageCommon from "@/components/print/PageCommon";

export default {
  name: "LandscapePage",
  mixins: [PageCommon]
}
</script>

<style scoped>

   .svg-wrapper {
     border-bottom: darkblue solid 1px;
   }

  @media print {
     #roadsafety-header {
       display: none;
     }
     #debug-component {
       display: none;
     }
     #not-authenticated-banner {
       display: none;
     }

    .svg-wrapper {
      margin-top: 25mm;
      border: none;
      page-break-before:always;
      -webkit-transform: rotate(-90deg);
      -moz-transform:rotate(-90deg);
      filter:progid:DXImageTransform.Microsoft.BasicImage(rotation=3);
    }

    @page {
      margin: 0;

    }
  }

</style>