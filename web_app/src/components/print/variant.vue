<template>
  <div>
    <component
        v-for="(page, index) in variant.pages"
        :is="page.orientation"
        :key="index"
        :page="page"
        :fields="document.fields"
        :viewbox="document.viewbox"
        :form_type="form_type"
        :form_id="form_id">
    </component>
  </div>
</template>
<script>
import Landscape from "@/components/print/LandscapePage"
import Portrait from "@/components/print/PortraitPage";
export default {
  name: "variant",
  props: {
    name: {
      type: String
    },
    variant: {
      type: Object
    },
    document: {
      type: Object
    },
    form_type: {
      type: String
    },
    form_id: {
      type: String
    }
  },
  computed: {
    selectPageType() {
      return this.variant.orientation
    }
  },
  components: {
    Portrait,
    Landscape
  }
}
</script>
<style type="text/css">
  .fontText {
    font-size: 3pt;
  }
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
    #not-logged-in-banner {
      display: none;
    }
    #end-of-life-banner {
      display: none;
    }
    .svg-wrapper {
      margin-top: 25mm;
      border: none;
    }
    @page {
      margin: 0;
    }
  }
</style>