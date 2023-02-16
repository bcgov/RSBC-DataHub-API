<template>
  <div v-if="visible" class="form-group" :class="fg_class">
    <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
      <label v-if="show_label" :for="id"><slot></slot>
        <span v-if="required" class="text-danger"> *</span>
      </label>
      <div class="input-group mb-3">
        <input type=text class="form-control" :class="fe_class" :disabled="disabled || hasFormBeenPrinted" :id="id" placeholder="" v-model="attribute">
        <div class="input-group-append">
          <button type="button" @click="triggerPlateLookup" class="btn-sm btn-secondary font-weight-bold" :disabled="hasFormBeenPrinted || ! isDisplayIcbcPlateLookup" id="icbc-prefill">
            ICBC Prefill
            <b-spinner v-if="display_spinner" label="Loading..." small></b-spinner>
          </button>
        </div>
      </div>
      <div class="small text-danger">
        {{ errors[0] }}
        <fade-text v-if="fetch_error" :show-seconds=3000>{{ fetch_error }}</fade-text>
      </div>
    </validation-provider>
  </div>
</template>
<script>
  import FadeText from "@/components/FadeText";
  import FieldCommon from "@/components/questions/FieldCommon";
  import { mapActions, mapGetters,  mapMutations} from "vuex";
  export default {

    name: "PlateNumber",
    components: {
      FadeText
    },
    computed: {
      ...mapGetters([
          "getAttributeValue",
          "getCurrentlyEditedFormId",
          "hasFormBeenPrinted",
          "isDisplayIcbcPlateLookup"
      ]),
      icbcPayload() {
        return {
          "plateNumber": this.getAttributeValue(this.path, this.id)
        }
      },
    },
    data() {
      return {
        display_spinner: false,
        fetch_error: ''
      }
    },
    methods: {
    ...mapActions(["lookupPlateFromICBC"]),
    ...mapMutations(["updateFormField"]),
      triggerPlateLookup() {
        this.fetch_error = '';
        this.display_spinner = true;
        this.lookupPlateFromICBC([this.icbcPayload, this.path])
        .then( () => {
          this.display_spinner = false
        })
        .catch( error => {
          this.display_spinner = false
          this.fetch_error = error.description;
        })
      }
    },
    mixins: [ FieldCommon ]
  }
</script>