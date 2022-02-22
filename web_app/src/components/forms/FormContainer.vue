<template>
    <div class="card w-100 mt-3 mb-3 border-primary">
      <div class="card-header text-white bg-secondary pt-2 pb-0">
        <h4>{{ title }}</h4>
      </div>
      <div class="card-header mt-0 mb-0 pt-2 pb-0 text-dark">
        <p class="text-right pb-0 mb-2">
          <span class="prohibition_number">{{ getCurrentlyEditedFormId }} </span>
        </p>
      </div>
      <slot></slot>
    </div>
</template>

<script>

import { mapGetters } from 'vuex'

export default {
  name: "FormContainer",
  props: {
    title: String
  },
  computed: {
    ...mapGetters(['getCurrentlyEditedFormId'])
  }
}
</script>