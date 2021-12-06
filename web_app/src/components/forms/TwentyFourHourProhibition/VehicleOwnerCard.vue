<template>
<div class="card-body text-dark text-left">
  <div class="card w-100">
    <div class="card-header lightgray text-dark font-weight-bold pt-2 pb-2">
      <div class="row p-0 m-0">
          <div class="col-6 pt-1 pl-0">Registered Owner</div>
          <div class="col-6 text-right">
            <div class="custom-control custom-switch">
              <div type="button" @click="populateOwnerFromDriver" class="btn btn-outline-primary btn-sm small">Fill from driver</div>
           </div>
          </div>
      </div>
    </div>
      <div class="card-body lightgray" v-if="! isReadOnly">
        <div>
          <form-row>
            <check-field fg_class="col-sm-12" :show_label="false" id="corporate_owner" :options="['Owned by corporate entity']" >Corporation</check-field>
          </form-row>
          <form-row>
            <text-field v-if="corporateOwner" id="owners_corporation" fg_class="col-sm-12">Corporation Name</text-field>
            <text-field v-if="!corporateOwner" id="owners_last_name" fg_class="col-sm-6">Owner's Last Name</text-field>
            <text-field v-if="!corporateOwner" id="owners_first_name" fg_class="col-sm-6">Owner's First Name</text-field>
          </form-row>
          <form-row>
            <text-field id="owners_address1" fg_class="col-sm-12" placeholder="Address" rules="lt25">Address Line 1</text-field>
          </form-row>
          <form-row>
            <type-ahead-field id="owners_city" fg_class="col-sm-4" :suggestions="getArrayOfBCCityNames">City</type-ahead-field>
            <province-field id="owners_province" fg_class="col-sm-2">Province</province-field>
            <text-field id="owners_postal" fg_class="col-sm-2">Postal</text-field>
            <phone-field id="owners_phone" fg_class="col-sm-4" rules="phone">Phone</phone-field>
          </form-row>
        </div>
      </div>
    </div>
</div>
</template>

<script>
import {mapGetters, mapMutations} from "vuex";
import CardsCommon from "@/components/forms/CardsCommon";

export default {
  name: "VehicleOwnerCard",
  props: {
    title: String
  },
  mixins: [CardsCommon],
  data() {
    return {
      owner_id: "owner_is_driver",
      owner_option: "Driver is the vehicle owner",
    }
  },
  methods: {
    ...mapMutations(["populateOwnerFromDriver"])
  },
  computed: {
    ...mapGetters(["checkBoxStatus", "corporateOwner"])
  }
}
</script>