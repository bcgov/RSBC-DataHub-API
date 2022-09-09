<script>

import TextField from "@/components/questions/TextField";
import ProvinceField from "@/components/questions/ProvinceField";
import JurisdictionField from "@/components/questions/JurisdictionField";
import DriverLicenceNumber from "@/components/questions/DriverLicenceNumber";
import GenderField from "@/components/questions/GenderField";
import PhoneField from "@/components/questions/PhoneField";
import EmailField from "@/components/questions/EmailField";
import DateField from "@/components/questions/DateField";
import DobField from "@/components/questions/DoBField";
import OffenceCity from "@/components/questions/OffenceCity";
import PlateNumber from "@/components/questions/PlateNumber";
import RadioField from "@/components/questions/RadioField";
import RadioDescription from "@/components/questions/RadioDescription";
import CheckField from "@/components/questions/CheckField/CheckField";
import ShadowBox from "@/components/forms/ShadowBox";
import FormCard from "@/components/forms/FormCard";
import FormRow from "@/components/forms/FormRow";
import TimeField from "@/components/questions/TimeField";
import VehicleColour from "@/components/questions/VehicleColour/VehicleColour";
import VehicleStyle from "@/components/questions/VehicleStyle/VehicleStyle";
import VehicleMakeModel from "@/components/questions/VehicleMakeModel";
import VehicleYear from "@/components/questions/VehicleYear";
import ReadOnlyElement from "@/components/questions/ReadOnlyElement";
import InLineCheckBox from "@/components/questions/InLineCheckBox";
import ImpoundLotOperator from "@/components/questions/ImpoundLotOperator";
import DriverLicenceClass from "@/components/questions/DriverLicenceClass";
import {mapGetters} from "vuex";


export default {
  name: "CardCommon",
  props: {
    isReadOnly: {
      default: false
    },
    path: {
      type: String
    }
  },
  computed: {
    ...mapGetters([
        "getAttributeValue",
        "getArrayOfAgencies",
        "doesAttributeExist",
        "hasFormBeenPrinted",
        "isLicenceJurisdictionBC",
        "getCurrentUserObject"
    ]),
    bcdlNumberRules() {
      if (this.getAttributeValue(this.path + '/drivers_licence_jurisdiction', 'objectCd') === "BC") {
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
    DriverLicenceClass,
    EmailField,
    FormCard,
    FormRow,
    GenderField,
    InLineCheckBox,
    ImpoundLotOperator,
    JurisdictionField,
    OffenceCity,
    PhoneField,
    PlateNumber,
    ProvinceField,
    RadioField,
    RadioDescription,
    ReadOnlyElement,
    ShadowBox,
    TextField,
    TimeField,
    VehicleColour,
    VehicleMakeModel,
    VehicleStyle,
    VehicleYear
  }
}
</script>

<style scoped>

</style>