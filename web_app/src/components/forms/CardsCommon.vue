<script>

import TextField from "@/components/questions/TextField";
import ProvinceField from "@/components/questions/ProvinceField";
import JurisdictionField from "@/components/questions/JurisdictionField";
import DriverLicenceNumber from "@/components/questions/DriverLicenceNumber";
import TypeAheadField from "@/components/questions/TypeAheadField";
import GenderField from "@/components/questions/GenderField";
import PhoneField from "@/components/questions/PhoneField";
import EmailField from "@/components/questions/EmailField";
import DateField from "@/components/questions/DateField";
import DobField from "@/components/questions/DoBField";
import PlateNumber from "@/components/questions/PlateNumber";
import RadioField from "@/components/questions/RadioField";
import CheckField from "@/components/questions/CheckField";
import ShadowBox from "@/components/forms/ShadowBox";
import FormStep from "@/components/forms/FormStep";
import FormCard from "@/components/forms/FormCard";
import FormRow from "@/components/forms/FormRow";
import TimeField from "@/components/questions/TimeField";
import ReadOnlyElement from "@/components/questions/ReadOnlyElement";
import InLineCheckBox from "@/components/questions/InLineCheckBox";
import {mapGetters} from "vuex";


export default {
  name: "CardCommon",
  props: {
    id: String,
    isReadOnly: {
      default: false
    }
  },
  computed: {
    ...mapGetters(["getAttributeValue", "getArrayOfBCCityNames", "getArrayOfAgencies"]),
    offenceCityRules() {
      return {
        required: true,
        inCities: this.getArrayOfBCCityNames
      }
    },
    bcdlNumberRules() {
      if (this.getAttributeValue('drivers_licence_jurisdiction') === "British Columbia") {
        return {
          'bcdlNumberRule': true
        }
      }
      return {}
    }
  },
  components: {
    CheckField,
    DateField,
    DobField,
    DriverLicenceNumber,
    EmailField,
    FormCard,
    FormRow,
    FormStep,
    GenderField,
    InLineCheckBox,
    JurisdictionField,
    PhoneField,
    PlateNumber,
    ProvinceField,
    RadioField,
    ReadOnlyElement,
    ShadowBox,
    TextField,
    TimeField,
    TypeAheadField
  }
}
</script>

<style scoped>

</style>