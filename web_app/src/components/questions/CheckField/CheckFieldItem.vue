<template>
  <div>
    <input class="form-check-input"
         :id="id"
         type="checkbox"
         v-model="attribute"
         :name="id">
    <label class="form-check-label" :for="id">{{ label }}</label>
  </div>

</template>

<script>
import {mapMutations, mapGetters} from "vuex";
import FieldCommon from "@/components/questions/FieldCommon";

export default {
  name: "CheckFieldItem",
  mixins: [FieldCommon],
  props: {
    label: {
      type: String,
      default: ''
    }
  },
  methods: {
    ...mapMutations(["updateFormField", "deleteFormField"])
  },
  computed: {
    ...mapGetters(["checkBoxStatus", "hasFormBeenPrinted", "doesAttributeExist", "getAttributeValue"]),
    attribute: {
      get() {
        return this.getAttributeValue(this.path, this.id)
      },
      set(event, other) {
        console.log("event setter", event, other)
        const payload = {
          target: {
            path: this.path,
            id: this.id,
            value: {}
          }
        }
        console.log("updateCheckBox()", payload)
        if (event) {
          this.updateFormField(payload)
        } else {
          // item exists; remove it
          if (this.doesAttributeExist(this.path, this.id)) {
            this.deleteFormField(payload)
          }
        }
      }
    }
  }
}
</script>

<style scoped>

</style>