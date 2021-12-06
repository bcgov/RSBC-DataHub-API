<template>
<div class="row m-0 p-0 text-muted">
    <div class="col-sm-3"><slot></slot></div>
    <div class="col-sm-7">{{ displayAttributeValue }}</div>
  </div>
</template>

<script>
import {mapGetters} from "vuex";

export default {
name: "ReadOnlyElement",
  props: {
    id: String
  },
  computed: {
    ...mapGetters(["getAttributeValue"]),
    displayAttributeValue() {
      const value = this.getAttributeValue(this.id);
      if (typeof value === "object") {
          if (value.length === 0) {
            return "No"
          }
          return value.join(", ")
      }
      return value
    }
  }
}
</script>
