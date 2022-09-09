<template>
  <form-container title="Immediate Roadside Prohibition" v-if="isMounted">
    <validation-observer v-slot="{handleSubmit, validate}">
      <form @submit.prevent="handleSubmit(onSubmit(validate))">
        <form-card title="Driver's Information">
          <form-row>
            <driver-licence-number id="drivers_number" :path="getPath"  :rules="bcdlNumberRules">Driver's Licence Number</driver-licence-number>
            <jurisdiction-field id="drivers_licence_jurisdiction" :path=getPath fg_class="col-sm-3">Prov / State / International</jurisdiction-field>
          </form-row>
          <form-row>
            <gender-field id="driver_gender" :path=getPath fg_class="col-sm-3">Gender</gender-field>
            <text-field id="expiry_year" :path=getPath fg_class="col-sm-4" placeholder="YYYY" rules="bcdlExpiryYear">License Expiry Year</text-field>
            <driver-licence-class v-if="isLicenceJurisdictionBC" id="dl_class" :path=getPath fg_class="col-sm-2">BCDL Class</driver-licence-class>
            <dob-field id="dob" :path=getPath fg_class="col-sm-3">Date of Birth</dob-field>
          </form-row>
          <form-row>
            <text-field id="last_name" :path=getPath fg_class="col-sm-5" placeholder="Last Name" rules="required|max:20">Last Name</text-field>
            <text-field id="first_name" :path=getPath fg_class="col-sm-7" placeholder="Given Names" rules="max:20">Given Names</text-field>
          </form-row>
          <form-row>
            <text-field id="address1" :path=getPath fg_class="col-sm-12" placeholder="Address" rules="required|max:25">Address</text-field>
          </form-row>
          <form-row>
            <text-field id="city" :path=getPath fg_class="col-sm-6" rules="required|max:15">City</text-field>
            <province-field id="province" :path=getPath fg_class="col-sm-2" rules="required">Prov / State</province-field>
            <text-field id="postal" :path=getPath fg_class="col-sm-4">Postal / Zip</text-field>
          </form-row>
        </form-card>
        <form-card title="Prohibition">
          <form-row>
            <text-field id="offence_address" :path="getPath" fg_class="col-sm-7" rules="required">Intersection or Address of Offence</text-field>
            <offence-city :path="getPath" fg_class="col-sm-5">City</offence-city>
          </form-row>
          <form-row>
            <date-field id="prohibition_start_date" :path="getPath" fg_class="col-sm-6"
                        rules="required|validDt|notFutureDt|notGtYearAgo">
              Date of Driving - care or control
            </date-field>
            <time-field id="prohibition_start_time" :path="getPath" fg_class="col-sm-6"
                        rules="required|validTime|notFutureDateTime:@prohibition_start_date">
              Time of Driving - care or control
            </time-field>
          </form-row>
          <form-row>
            <radio-field id="prohibition_type" :path="getPath" fg_class="col-sm-12" :options='[
               ["3-days-warn", "3 days WARN"],
               ["7-days-warn", "7 days WARN"],
               ["30-days-warn", "30 days WARN"],
               ["90-days-fail", "90 days FAIL"],
               ["90-days-refuse", "90 days REFUSAL"]
                ]'>
                Prohibition period and type:
            </radio-field>
          </form-row>
        </form-card>
        <form-card title="Vehicle Impoundment or Disposition">
            <form-row>
              <radio-field id="vehicle_impounded" :path="getPath"
                           fg_class="col-sm-4" :options='[["yes", "Yes"], ["no", "No"]]'
                           rules="required">Vehicle Impounded?
              </radio-field>
              <vi-number :path="getPath + '/vehicle_impounded_yes'"
                           v-if="doesAttributeExist(getPath, 'vehicle_impounded_yes')"
                           fg_class="col-sm-8"
                           rules="required">Vehicle Impoundment Number
              </vi-number>
            </form-row>
        </form-card>
        <form-card title="Driver's Licence">
            <form-row>
              <radio-field id="license_seized" :path="getPath"
                           fg_class="col-sm-6" :options='[["yes", "Yes"], ["no", "No"]]'
                           rules="required">Seized Driver's Licence?
              </radio-field>
            </form-row>
        </form-card>

        <form-card title="Officer">
          <form-row >
            <text-field id="file_number" :path="getPath" fg_class="col-sm-2" rules="required">Agency File #</text-field>
            <text-field id="agency"
                        :default_value="getCurrentUserObject.agency"
                        :path="getPath" rules="required" fg_class="col-sm-4">
              Agency</text-field>
            <text-field id="badge_number"
                        :default_value="getCurrentUserObject.badge_number"
                        :path="getPath" rules="required" fg_class="col-sm-2">
              Badge #</text-field>
            <text-field id="officer_name"
                        :default_value="getCurrentUserObject.last_name"
                        :path="getPath" rules="required" fg_class="col-sm-4">
              Last Name of Peace Officer Serving Prohibition Notice</text-field>
          </form-row>
        </form-card>
        <form-card title="Generate PDF for Printing">
          <div class="d-flex">
            <print-documents
              v-for="(document, index) in getDocumentsToPrint(name)" v-bind:key="index"
              :show_certificate="isCertificateOfServiceEnabled(getPath)"
              :path="getPath"
              :form_object="getCurrentlyEditedForm"
              :validate="validate"
              :variants="document.variants">
              {{ document.name }}
            </print-documents>
          </div>
        </form-card>
      </form>
    </validation-observer>
  </form-container>
</template>

<script>
import FormsCommon from "@/components/forms/FormsCommon";
import CardsCommon from "@/components/forms/CardsCommon";
import ViNumber from "@/components/questions/ViNumber";

export default {
  name: "ImmediateRoadsideProhibition",
  mixins: [FormsCommon, CardsCommon],
    props: {
    name: {
      type: String,
      default: 'IRP'
    }
  },
  mounted() {
    let payload = {form_type: this.name, form_id: this.id}
    this.editExistingForm(payload)
    this.setNewFormDefaults(payload)
    this.data = this.getCurrentlyEditedFormData
    this.isMounted = true
  },
  components: {
    ViNumber
  }
}
</script>