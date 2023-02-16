<template>
  <div>
    <div class="d-flex">
      <div>
        <router-link to="/" class="text-white font-weight-bold">
          <div class="btn btn-info m-0">Return to Main Menu</div>
        </router-link>
      </div>
    </div>
    <div class="card w-100 mt-3 mb-3 border-primary">
      <div class="card-header text-white bg-secondary pt-2 pb-0">
        <h4>{{ title }}</h4>
      </div>
      <div class="card-header mt-0 mb-0 pt-2 pb-0 text-dark">
        <p class="text-right pb-0 mb-2">
          <span class="prohibition_number">{{ getDashedFormNumber }}<check-digit :form_object="form_object"></check-digit></span>
        </p>
      </div>
      <slot></slot>
    </div>
  </div>
</template>
<script>
  import CheckDigit from "@/components/forms/CheckDigit";
  import { mapGetters } from 'vuex'
  export default {
    name: "FormContainer",
    components: { CheckDigit },
    computed: {
      ...mapGetters([
        'getCurrentlyEditedFormId',
        'getFormIdCheckDigit'
      ]),
      getDashedFormNumber() {
        let dashedFormNumber = "";
        for (let x = 0; x < this.getCurrentlyEditedFormId.length; x++) {
          (x == 2) ? dashedFormNumber += "-" + this.getCurrentlyEditedFormId[x] : dashedFormNumber += this.getCurrentlyEditedFormId[x];
        }
        return dashedFormNumber;
      }
    },
    props: {
      form_object: Object,
      title: String
    }
  }
</script>
<style scoped>
  #check-digit {
    background: lightgrey;
    padding: 0 2px 0 2px;
  }
</style>