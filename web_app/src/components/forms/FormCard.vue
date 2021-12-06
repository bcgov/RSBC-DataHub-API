<template>
<div class="card-body text-dark text-left">
  <div class="card">
    <div v-if="title" class="card-header lightgray text-dark font-weight-bold pt-2 pb-2">
      <div class="container p-0 m-0">
        <div class="row p-0 mt-0 mb-0">
          <div class="col-12 pt-1">{{ title }}</div>
        </div>
      </div>
    </div>
    <div class="card-body lightgray">
      <slot></slot>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: "FormCard",
  props: {
    title: String
  }
}
</script>