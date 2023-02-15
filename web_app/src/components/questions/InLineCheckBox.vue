<template>
  <div v-if="visible" class="form-group" :class="fg_class">
    <div class="form-check">
      <input class="form-check-input" :disabled="disabled || hasFormBeenPrinted" :id="id" :name="id" type="checkbox" v-model="attribute" :value="option">
      <label class="form-check-label" :for="id"><slot></slot></label>
    </div>
  </div>
</template>
<script>
  import FieldCommon from "@/components/questions/FieldCommon";
  import { mapGetters,  mapMutations} from 'vuex';
  export default {
    name: "InLineCheckBox",
    computed: {
      ...mapGetters([
        "checkBoxStatus",
        "hasFormBeenPrinted"
      ]),
      attribute: {
        get() {
          return this.doesAttributeExist(this.path, this.id + '_true');
        },
        set(value) {
          [true, false].forEach((option) => {
            const payload = {
              target: {
                  id: this.id + "_" + option.toString(),
                  path: this.path,
                  value: {}
                }
            }
            if (value === option) {
              this.updateFormField(payload);
            } else {
              this.deleteFormField(payload);
            }
          })
        }
      },
    },
    methods: {
      ...mapMutations([
        "deleteFormField",
        "updateCheckBox",
        "updateFormField"
      ])
    },
    mixins: [ FieldCommon ],
    props: {
      option: null,
      type: String()
    }
  }
</script>