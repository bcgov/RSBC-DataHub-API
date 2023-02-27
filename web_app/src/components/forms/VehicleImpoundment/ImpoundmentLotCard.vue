<template>
  <form-card title="Impound Lot">
      <form-row>
        <date-field id="impounded_dt" :path=path rules="required|validDt|notFutureDt|notGtYearAgo" fg_class="col-sm-12">Date of Vehicle Impoundment</date-field>
      </form-row>
      <impound-lot-operator :path=path fg_class="col-sm-12">Impound Lot Operator</impound-lot-operator>
  </form-card>
</template>
<script>
  import CardsCommon from "@/components/forms/CardsCommon";
  import ImpoundLotOperator from "@/components/questions/ImpoundLotOperator";
  export default {
  name: "ImpoundmentLotCard",
    components: { ImpoundLotOperator },
    mixins: [ CardsCommon ]
  }
</script>