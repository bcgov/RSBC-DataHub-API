<template>
  <div class="card-body text-dark text-left">
    <div class="card w-100">
      <div class="card-header lightgray text-dark font-weight-bold pt-2 pb-2">
        <div class="row p-0 m-0">
          <div class="col-6 pt-1 pl-0">Registered Owner</div>
          <div class="col-6 text-right">
            <div class="custom-control custom-switch">
              <div class="btn btn-outline-primary btn-sm small" @click="populateOwnerFromDriver(path)" :disabled="hasFormBeenPrinted" type="button">Copy from Driver's Information</div>
            </div>
          </div>
        </div>
      </div>
      <div class="card-body lightgray">
        <div>
          <form-row>
            <in-line-check-box fg_class="col-sm-12" id="corp_owner" :path="path" :option="true" >Vehicle is owned by a company?</in-line-check-box>
          </form-row>
          <form-row v-if="doesAttributeExist(path, 'corp_owner_true')">
            <text-field fe_class="uppercase" fg_class="col-sm-12" id="name" :path="path + '/corp_owner_true'" rules="max:40">Company Name</text-field>
          </form-row>
          <form-row v-if="!doesAttributeExist(path, 'corp_owner_true')">
            <text-field id="owners_last_name" fe_class="uppercase" fg_class="col-sm-4" :path="path + '/corp_owner_false'" rules="max:20">Owner's Surname</text-field>
            <text-field id="owners_first_name" fe_class="capitalize" fg_class="col-sm-5" :path="path + '/corp_owner_false'" rules="max:20">Owner's First Name</text-field>
            <dob-field id="owner_dob" fg_class="col-sm-3" :path="path + '/corp_owner_false'" rules="dob8|dob"></dob-field>
          </form-row>
          <form-row>
            <text-field id="owners_address1" fe_class="uppercase" fg_class="col-sm-8" :path="path" placeholder="" rules="lt25">Street Address</text-field>
            <text-field id="owners_city" fe_class="uppercase" fg_class="col-sm-4" :path="path" rules="max:20">City</text-field>
          </form-row>
          <form-row>
            <province-field id="owners_province" fg_class="col-sm-2" :path="path">Province / State</province-field>
            <text-field id="owners_postal" fe_class="uppercase" fg_class="col-sm-2" :path="path">Postal / ZIP</text-field>
            <phone-field id="owners_phone" fg_class="col-sm-4" :path="path" rules="phone">Phone Number</phone-field>
            <email-field id="owners_email" fg_class="col-sm-4" :path="path" rules="email">Email Address</email-field>
          </form-row>
          <form-row>
            <in-line-check-box id="driver_is_owner" :path="path" :option="true">Driver is the registered owner?</in-line-check-box>
          </form-row>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import CardsCommon from "@/components/forms/CardsCommon";
  import { mapActions } from "vuex";
  export default {
    name: "VehicleOwnerCard",
    data() {
      return {
        owner_id: "owner_is_driver",
        owner_option: "Driver is the vehicle owner",
      };
    },
    methods: {
      ...mapActions([
        "populateOwnerFromDriver"
      ]),
    },
    mixins: [ CardsCommon ],
    props: {
      title: String,
    }
  };
</script>