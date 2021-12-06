<script>
import CheckField from "@/components/questions/CheckField";
import DateField from "@/components/questions/DateField";
import DateTime from "@/components/questions/DateTime";
import DobField from "@/components/questions/DoBField";
import DriverLicenceNumber from "@/components/questions/DriverLicenceNumber";
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
import TypeAheadField from "@/components/questions/TypeAheadField";
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
    ...mapGetters(["getArrayOfBCCityNames", "getFormData"]),
    getFormObject() {
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
    DateTime,
    DobField,
    DriverLicenceNumber,
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
    TypeAheadField,
    ValidationObserver
  }
}
</script>
