<script>
import TextComponent from "@/components/print/TextComponent";
import CheckboxComponent from "@/components/print/CheckBoxComponent";
import BarcodeComponent from "@/components/print/BarcodeComponent";
import MemoComponent from "@/components/print/MemoComponent";
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
    },
    baseURL() {
      return process.env.BASE_URL
    }
  },
  components: {
    TextComponent,
    CheckboxComponent,
    BarcodeComponent,
    MemoComponent
  }
}
</script>

