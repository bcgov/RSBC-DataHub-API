<template>
  <form-card title="Impound Lot">
      <form-row>
        <date-field id="impounded_dt" fg_class="col-sm-12">The motor vehicle was impounded on</date-field>
      </form-row>
      <form-row>
        <impound-lot-operator fg_class="col-sm-12">Impound Lot Operator</impound-lot-operator>
      </form-row>
  </form-card>
</template>

<script>

import CardsCommon from "@/components/forms/CardsCommon";
import {mapGetters, mapMutations} from 'vuex';
import ImpoundLotOperator from "@/components/questions/ImpoundLotOperator";


export default {
name: "VehicleImpoundmentCard",
  components: {ImpoundLotOperator},
  mixins: [CardsCommon],
  computed: {
    ...mapGetters(["getAttributeValue", "getArrayOfImpoundLotOperators"])
  },
  mounted() {
    // The vehicle is always impounded when using the Vehicle Impoundment (VI) form
    this.setFormAsImpounded()
  },
  methods: {
    ...mapMutations(["setFormAsImpounded"])
  }
}
</script>

<style scoped>

</style>