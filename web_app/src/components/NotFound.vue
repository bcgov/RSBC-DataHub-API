<template>
  <div class="card bg-light border-secondary mb-3">
      <div class="card-body text-dark">
        <div class="font-weight-bold">Page Not Found</div>
        Try going back
        <router-link to="/" class="font-weight-bold">
          <span class="text-primary">Home</span>
        </router-link>
      </div>
  </div>
</template>

<script>
export default {
name: "NotFound"
}
</script>