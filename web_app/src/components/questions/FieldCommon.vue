<script>
  import Multiselect from 'vue-multiselect'
  import { mapMutations, mapGetters } from 'vuex';
  export default {
    name: "FieldCommon",
    components: { Multiselect },
    computed: {
      ...mapGetters([
        "doesAttributeExist",
        "getAttributeValue",
        "hasFormBeenPrinted"
      ]),
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
          return this.updateFormField(payload);
        }
      },
      glowClass() {
        if (this.errors) {
          return "form-control border-danger";
        }
        return "form-control";
      },
      isShowOptional() {
        if (this.rules) {
          return ! this.rules.includes('required');
        }
        return true;
      }
    },
    props: {
      disabled: {
        type: Boolean,
        default: false
      },
      display_validation_errors: Boolean,
      fe_class: String,
      fg_class: String,
      id: String,
      path: {
        type: String
      },
      rules: {},
      show_label: {
        type: Boolean,
        default: true
      },
      visible: {
        type: Boolean,
        default: true
      }
    },
    methods: {
      ...mapMutations(["updateFormField", "deleteFormField"])
    }
  }
</script>