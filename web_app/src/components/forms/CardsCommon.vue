<script>
  import CheckField from "@/components/questions/CheckField";
  import DateField from "@/components/questions/DateField";
  import DobField from "@/components/questions/DoBField";
  import DriverLicenceNumber from "@/components/questions/DriverLicenceNumber";
  import EmailField from "@/components/questions/EmailField";
  import FormCard from "@/components/forms/FormCard";
  import FormRow from "@/components/forms/FormRow";
  import FormStep from "@/components/forms/FormStep";
  import GenderField from "@/components/questions/GenderField";
  import ImpoundLotOperator from "@/components/questions/ImpoundLotOperator";
  import InLineCheckBox from "@/components/questions/InLineCheckBox";
  import JurisdictionField from "@/components/questions/JurisdictionField";
  import OffenceCity from "@/components/questions/OffenceCity";
  import PhoneField from "@/components/questions/PhoneField";
  import PlateNumber from "@/components/questions/PlateNumber";
  import ProvinceField from "@/components/questions/ProvinceField";
  import RadioDescription from "@/components/questions/RadioDescription";
  import RadioField from "@/components/questions/RadioField";
  import ReadOnlyElement from "@/components/questions/ReadOnlyElement";
  import ShadowBox from "@/components/forms/ShadowBox";
  import TextField from "@/components/questions/TextField";
  import TimeField from "@/components/questions/TimeField";
  import VehicleColour from "@/components/questions/VehicleColour/VehicleColour";
  import VehicleMakeModel from "@/components/questions/VehicleMakeModel";
  import VehicleStyle from "@/components/questions/VehicleStyle/VehicleStyle";
  import VehicleYear from "@/components/questions/VehicleYear";
  import { mapGetters } from "vuex";
  export default {
    name: "CardCommon",
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
      ImpoundLotOperator,
      InLineCheckBox,
      JurisdictionField,
      OffenceCity,
      PhoneField,
      PlateNumber,
      ProvinceField,
      RadioDescription,
      RadioField,
      ReadOnlyElement,
      ShadowBox,
      TextField,
      TimeField,
      VehicleColour,
      VehicleMakeModel,
      VehicleStyle,
      VehicleYear
    },
    computed: {
      ...mapGetters([
        "doesAttributeExist",
        "hasFormBeenPrinted",
        "getAttributeValue",
        "getArrayOfAgencies"
      ]),
      bcdlNumberRules() {
        if (this.getAttributeValue(this.path + '/drivers_licence_jurisdiction', 'objectDsc') === "British Columbia") {
          return {
            'bcdlNumberRule': true
          }
        }
        return {}
      }
    },
    props: {
      isReadOnly: {
        default: false
      },
      path: {
        type: String
      }
    },
  }
</script>