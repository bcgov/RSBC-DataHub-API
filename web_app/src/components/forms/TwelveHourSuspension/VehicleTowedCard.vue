<template>

    <div>
      <form-row>
        <radio-field id="location_of_keys"
                     :path="path"
                      fg_class="col-sm-6" rules="required"
                     :options='[["vehicle", "With vehicle"], ["driver", "With driver"]]'>Location of Keys?</radio-field>
      </form-row>
      <impound-lot-operator
          :path="path"  fg_class="col-sm-12" rules="required">Tow Operator</impound-lot-operator>
    </div>

</template>

<script>

import CardsCommon from "@/components/forms/CardsCommon";


export default {
name: "VehicleImpoundmentCard",
mixins: [CardsCommon]
}
</script>

<style scoped>

</style>