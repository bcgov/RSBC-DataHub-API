<script>
  import CheckField from "@/components/questions/CheckField";
  import DateField from "@/components/questions/DateField";
  import DobField from "@/components/questions/DoBField";
  import DriverLicenceNumber from "@/components/questions/DriverLicenceNumber";
  import EmailField from "@/components/questions/EmailField";
  import FormCard from "@/components/forms/FormCard";
  import FormContainer from "@/components/forms/FormContainer";
  import FormRow from "@/components/forms/FormRow";
  import FormStep from "@/components/forms/FormStep";
  import GenderField from "@/components/questions/GenderField";
  import PhoneField from "@/components/questions/PhoneField";
  import PlateNumber from "@/components/questions/PlateNumber";
  import ProvinceField from "@/components/questions/ProvinceField";
  import RadioField from "@/components/questions/RadioField";
  import ShadowBox from "@/components/forms/ShadowBox";
  import TextField from "@/components/questions/TextField";
  import { mapGetters, mapMutations } from "vuex";
  import { ValidationObserver } from 'vee-validate';
  export default {
    name: "FormsCommon",
    components: {
      CheckField,
      DateField,
      DobField,
      DriverLicenceNumber,
      EmailField,
      FormCard,
      FormContainer,
      FormRow,
      FormStep,
      GenderField,
      PhoneField,
      PlateNumber,
      ProvinceField,
      RadioField,
      ShadowBox,
      TextField,
      ValidationObserver
    },
    computed: {
      ...mapGetters(["getFormData", "getCurrentlyEditedForm"]),
      getPath() {
        return `forms/${this.name}/${this.id}/data`
      },
      formObject() {
        return {
          form_id: this.id,
          form_type: this.name
        }
      }
    },
    data() {
      return {
        data: {},
        isMounted: false,
        display_spinner: false,
        isNotValid: false,
        rerender: 1
      }
    },
    methods: {
      ...mapMutations([
        "editExistingForm",
        "setNewFormDefaults"
      ])
    },
    props: {
        name: {
          type: String
        },
        id: {}
    }
  }
</script>