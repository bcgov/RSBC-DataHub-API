<template>
  <div v-if="formData" class="svg-wrapper">
    <svg width="100%" :viewBox="viewbox">
      <image :href="process.env.BASE_URL + page.image.filename" :height="page.image.height + 'px'" :width="page.image.width + 'px'"/>
      <component
        v-for="(field, index) in fieldsToShow"
        v-bind:key="index"
        :is="fields[field].field_type + 'Component'"
        :start="fields[field].start"
        :field="fields[field]"
        :form_type="form_type"
        :form_id="form_id"
        :form_data="formData">
      </component>
     Sorry, your browser does not support inline SVG.
    </svg>
  </div>
</template>

<script>

import TextComponent from "@/components/print/TextComponent";
import CheckboxComponent from "@/components/print/CheckBoxComponent";
import BarcodeComponent from "@/components/print/BarcodeComponent";
import {mapGetters} from "vuex";

export default {
  name: "LandscapePage",
  props: {
    page: {
      type: Object,
    },
    fields: {
      type: Object
    },
    form_type: {
      type: String
    },
    form_id: {
      type: String
    },
    viewbox: {
      type: String
    }
  },
  computed: {
    ...mapGetters(["getForm"]),
    image() {
      return this.page.image;
    },
    fieldsToShow() {
      return this.page.show_fields;
    },
    formData() {
        return this.getForm(this.form_type, this.form_id)
    },
    viewBox() {
      return this.page.viewBox;
    }
  },
  components: {
    TextComponent,
    CheckboxComponent,
    BarcodeComponent
  }
}
</script>

