<template>
  <div v-if="isDisplayStep">
    <slot></slot>
    <div class="card-body mt-0 pt-0">
          <div class="row">
            <div class="col-6 text-left">
              <a @click="previousStep" href="#" v-if="! isPreviousButtonDisabled" class="btn btn-success">
                <b-icon-arrow-left></b-icon-arrow-left> {{ previousStepLabel }}
              </a>
            </div>
            <div class="col-6 text-right">
              <a @click="nextStep" href="#" v-if="! isNextButtonDisabled" class="btn btn-success">
                {{ nextStepLabel }} <b-icon-arrow-right></b-icon-arrow-right>
              </a>
            </div>
          </div>
    </div>
  </div>
</template>

<script>

import { mapGetters, mapMutations } from 'vuex';

export default {
  name: "FormStep",
  props: {
    step_number: Number
  },
  methods: {
    ...mapMutations(["nextStep", "previousStep"])
  },
  computed: {
    ...mapGetters(["getFormSteps", "getFormCurrentStep", "isPreviousButtonDisabled", "isNextButtonDisabled"]),
    isDisplayStep() {
      return this.getFormCurrentStep === this.step_number;
    },
    previousStepLabel() {
      return this.getFormSteps[this.step_number -2]
    },
    nextStepLabel() {
      return this.getFormSteps[this.step_number]
    }
  },
}
</script>