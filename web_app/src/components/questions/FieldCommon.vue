<script>

import { mapMutations, mapGetters } from 'vuex';

export default {
  name: "FieldCommon",
  props: {
    id: String,
    disabled: {
      type: Boolean,
      default: false
    },
    show_label: {
      type: Boolean,
      default: true
    },
    visible: {
      type: Boolean,
      default: true
    },
    path: {
      type: String
    },
    fg_class: String,
    display_validation_errors: Boolean,
    rules: {}
  },
  computed: {
    attribute: {
      get() {
        return this.getAttributeValue(this.path, this.id)
      },
      set(value) {
        const payload = {
          target: {
            path: this.path,
            id: this.id,
            value: value
          }
        }
        return this.updateFormField(payload)
      }
    },
    glowClass() {
      if (this.errors) {
        return "form-control border-danger"
      }
      return 'form-control'
    },
    ...mapGetters([
        "doesAttributeExist",
        "getAttributeValue",
        "hasFormBeenPrinted",
        "hasFormBeenPrinted"
    ])
  },
  methods: {
    ...mapMutations(["updateFormField", "deleteFormField"])
  }
}
</script>
