<script>
import CheckField from "@/components/questions/CheckField/CheckField";
import DateField from "@/components/questions/DateField";
import DobField from "@/components/questions/DoBField";
import DriverLicenceNumber from "@/components/questions/DriverLicenceNumber";
import EmailField from "@/components/questions/EmailField";
import FormCard from "@/components/forms/FormCard";
import FormContainer from "@/components/forms/FormContainer";
import FormRow from "@/components/forms/FormRow";
import GenderField from "@/components/questions/GenderField";
import JurisdictionField from "@/components/questions/JurisdictionField";
import PhoneField from "@/components/questions/PhoneField";
import PrintDocuments from "@/components/forms/PrintDocuments";
import PlateNumber from "@/components/questions/PlateNumber";
import ProvinceField from "@/components/questions/ProvinceField";
import RadioField from "@/components/questions/RadioField";
import ShadowBox from "@/components/forms/ShadowBox";
import TextField from "@/components/questions/TextField";
import { ValidationObserver } from 'vee-validate';
import {mapGetters, mapMutations} from "vuex";


export default {
  name: "FormsCommon",
    props: {
      name: {
        type: String
      },
      id: {},
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
  computed: {
    ...mapGetters(["getFormData", "getCurrentlyEditedForm", "getDocumentsToPrint", "isCertificateOfServiceEnabled"]),
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
  methods: {
    ...mapMutations(["editExistingForm", "setNewFormDefaults"])
  },
  components: {
    CheckField,
    DateField,
    DobField,
    DriverLicenceNumber,
    EmailField,
    FormCard,
    FormContainer,
    FormRow,
    GenderField,
    JurisdictionField,
    PhoneField,
    PlateNumber,
    PrintDocuments,
    ProvinceField,
    RadioField,
    ShadowBox,
    TextField,
    ValidationObserver
  }
}
</script>
