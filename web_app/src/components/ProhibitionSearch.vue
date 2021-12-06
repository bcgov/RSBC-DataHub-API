<template>
  <div class="card w-100 mt-3 bg-light border-light">
      <div class="card-body text-dark pt-1">
        <p class="small text-left pt-1 pb-1 mb-0 mt-0">Search for a recent prohibition</p>
        <form>
          <div class="d-flex form-row align-items-start">
            <wait-for-icbc-field :show_label=false id="plate_year" fg_class="col-sm-8">Prohibition Search</wait-for-icbc-field>
            <button type="submit" disabled class="btn btn-primary btn-sm">Search</button>
          </div>
        </form>
      </div>
  </div>
</template>

<script>

import WaitForIcbcField from "@/components/questions/WaitForICBCField";

export default {
  name: "ProhibitionSearch",
  components:{
    WaitForIcbcField
  }
}
</script>

<style scoped>
  .card {
    background-color: lightgray;
  }
</style>