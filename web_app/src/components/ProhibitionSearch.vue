<template>
  <div class="card w-100 mt-3 bg-light border-light">
      <div class="card-body text-dark pt-1">
        <p class="small text-left pt-1 pb-1 mb-0 mt-0">Search for a recent prohibition</p>
        <form>
          <div class="form-row align-items-center">
            <div class="col-sm-8 my-1">
              <label class="sr-only small" for="prohibitionSearch">Prohibition Number</label>
              <input type="text" class="form-control form-control-sm" id="prohibitionSearch" placeholder="Driver's last name or BCDL">
            </div>
            <div class="col-auto my-1">
              <button type="submit" disabled class="btn btn-primary btn-sm">Search</button>
            </div>
          </div>
        </form>
      </div>
  </div>
</template>

<script>
export default {
name: "ProhibitionSearch"
}
</script>

<style scoped>
  .card {
    background-color: lightgray;
  }
</style>