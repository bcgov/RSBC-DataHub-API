<template>
  <div v-if="show"><slot></slot></div>
</template>

<script>
export default {
  name: "FadeText",
  props: {
    display_seconds: {
      type: Number,
      default: 5000
    }
  },
  data() {
    return {
      show: true,
    }
  },
  mounted() {
    setTimeout(() => {this.show = false;}, this.display_seconds)
  }
}
</script>