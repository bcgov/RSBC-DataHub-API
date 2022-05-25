<template>
<div class="card-body text-dark text-left">
  <div class="card w-100">
    <div class="card-header lightgray text-dark font-weight-bold pt-2 pb-2">
      <div class="row p-0 m-0">
          <div class="col-6 pt-1 pl-0">Registered Owner</div>
          <div class="col-6 text-right">
            <div class="custom-control custom-switch">
              <div type="button" @click="populateOwnerFromDriver" class="btn btn-secondary btn-sm small">Fill from driver</div>
           </div>
          </div>
      </div>
    </div>
      <div class="card-body lightgray" v-if="! isReadOnly">
        <div>
          <form-row>
            <in-line-check-box fg_class="col-sm-12"
                         id="corp_owner"
                         :path="path" :option="true">Owned by corporate entity</in-line-check-box>
          </form-row>
          <form-row v-if="doesAttributeExist(path, 'corp_owner_true')">
            <text-field id="name" :path="path + '/corp_owner_true'" fg_class="col-sm-12" rules="max:40">
              Corporation Name</text-field>
          </form-row>
          <form-row v-if="! doesAttributeExist(path, 'corp_owner_true')">
            <text-field id="owners_last_name" :path="path + '/corp_owner_false'"  fg_class="col-sm-6" rules="max:20">
              Owner's Last Name</text-field>
            <text-field id="owners_first_name" :path="path + '/corp_owner_false'" fg_class="col-sm-6" rules="max:20">
              Owner's First Name</text-field>
          </form-row>
          <form-row>
            <text-field id="owners_address1" :path="path + '/owner_person'" fg_class="col-sm-12" placeholder="Address" rules="max:25">Address Line</text-field>
          </form-row>
          <form-row>
            <type-ahead-field id="owners_city" :path=path fg_class="col-sm-4" :suggestions="getArrayOfBCCityNames" rules="max:20">City</type-ahead-field>
            <province-field id="owners_province" :path=path fg_class="col-sm-2">Prov / State</province-field>
            <text-field id="owners_postal" :path=path fg_class="col-sm-2">Postal / Zip</text-field>
            <phone-field id="owners_phone" :path=path fg_class="col-sm-4" rules="phone">Phone</phone-field>
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
    ...mapGetters(["checkBoxStatus"])
  }
}
</script>