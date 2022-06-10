<template>
  <b-col>
    <div :class="selectedColourClass">
      <div class="btn "
           @click="toggleStyle()">
        {{ vehicle_style.name }}
      </div>
    </div>
  </b-col>

</template>

<script>
export default {
  name: "StyleCard",
  props: {
    selected: null,
    vehicle_style: {
      code: '',
      name: '',
    },
  },
  computed: {
    isSelected() {
      if (this.selected) {
        return this.selected.code === this.vehicle_style.code;
      }
      return false;
    },
    selectedColourClass() {
      if (this.isSelected) {
        return 'btn-warning selected'
      }
      return 'btn-light'
    }
  },
  methods: {
    toggleStyle() {
      this.$emit("toggle-style", this.vehicle_style)
    }
  }
}
</script>

<style scoped>

.selected {
  padding: 2px 2px 2px 2px;
  border: 5px solid red;
}

</style>