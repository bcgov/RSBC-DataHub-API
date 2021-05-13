<template>
<div v-if="visible" class="form-group" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
    <label class="small" :for="id"><slot></slot>
      <span v-if="required" class="text-danger"> *</span>
      <span class="text-muted" v-if="isValidDate"> ({{ timeAgoString }})</span>
    </label>
    <div class="col-xs-10">
      <div class="input-group mb-3">
        <input type="text"
           class="form-control form-control-sm" :disabled="disabled"
               placeholder="YYYY-MM-DD"
           :id="id"
           :value="dateSegment"
           @input="updateDateSegment">
        <input type="text"
           class="form-control form-control-sm" :disabled="disabled"
            placeholder="HH:MM"
            :value="timeSegment"
            @input="updateTimeSegment">
        <div class="input-group-append">
          <button @click="setCurrentDateTime" class="btn btn-sm btn-secondary" type="button">Now</button>
        </div>
      </div>
      <div class="small text-danger">{{ errors[0] }}</div>
    </div>
  </validation-provider>
</div>
</template>

<script>

import FieldCommon from "@/components/questions/FieldCommon";
import moment from 'moment';
import {mapGetters, mapMutations} from "vuex";

export default {
  name: "DateTime",
  mixins: [FieldCommon],

  data() {
    return {
      timeAgoString: null,
      setIntervalID: null
    }
  },

  created () {
    this.timeAgo()
    this.setIntervalID = setInterval(this.timeAgo.bind(this) , 1000)
  },

  destroyed() {
    clearInterval(this.setIntervalID)
  },

  methods: {
    ...mapMutations(["updateFormField"]),
    setCurrentDateTime() {
      this.setDateTime(this.getCurrentTime());
    },
    setDateTime(isoDateTimeString) {
      const payload = {target: {id: this.id, value: isoDateTimeString }}
      console.log('inside DateTime.vue setCurrentDateTime()', payload)
      this.$store.commit("updateFormField", payload)
    },
    timeAgo() {
      if(this.isValidDate) {
        this.timeAgoString = moment(this.getAttributeValue(this.id)).fromNow()
      }
    },
    getCurrentTime() {
      return moment().format("YYYY-MM-DD HH:mm");
    },
    updateTimeSegment(e) {
      const timeString = e.target.value;
      this.setDateTime(this.dateSegment + ' ' + timeString);
    },
    updateDateSegment(e) {
      const dateString = e.target.value;
      this.setDateTime(dateString + ' ' + this.timeSegment);
    }
  },

  computed: {
    ...mapGetters(["getAttributeValue"]),
    isValidDate() {
      return moment(this.getAttributeValue(this.id)).isValid()
    },
    dateSegment() {
      return this.getAttributeValue(this.id).split(' ')[0];
    },
    timeSegment() {
      return this.getAttributeValue(this.id).split(' ')[1];
    }
  }

}
</script>
