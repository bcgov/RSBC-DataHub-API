<script>

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
    fg_class: String,
    display_validation_errors: Boolean,
    rules: Object(),
    errors: Array()
  }
}
</script>
