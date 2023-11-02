<template>
  <div class="card bg-light border-secondary mb-3">
      <div class="card-body text-dark">
        <span class="font-weight-bold">Welcome!</span>
        Please log in to get started.
        <router-link to="/login" class="font-weight-bold">
          <div class="btn btn-primary">Login</div>
        </router-link>
      </div>
  </div>
</template>
<script>
export default {
  name: "WelcomeLoginCard"
}
</script>
<style scoped>
</style>