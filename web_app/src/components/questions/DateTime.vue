<template>
<div v-if="visible" class="form-group border" :class="fg_class">
  <validation-provider :rules="rules" :name="id" v-slot="{ errors, required }">
    <div class="col-xs-10">
      <div class="form-row">
        <div class="form-group col-md-6">
          <label :for="id"><slot></slot>
            <span class="small text-muted"> YYYYMMDD</span>
            <span v-if="required" class="text-danger"> *</span>
            <span class="badge badge-success ml-3" v-if="displayTimeAgoString"> {{ timeAgoString }}</span>
            <span v-if="displayDateNotValid" class="text-danger"> (date not valid)</span>
          </label>
          <input type="text"
             class="form-control"
             :class="errors.length > 0 ? 'border-danger bg-warning' : ''"
             :disabled="disabled"
             placeholder="YYYYMMDD"
             :id="id"
             :value="dateSegment"
             @input="updateDateSegment">
        </div>
        <div class="form-group col-md-6">
          <label for="time">
            <span class="small text-muted"> HHMM in Pacific Time</span>
            <span v-if="displayTimeNotValid" class="text-danger"> (time not valid)</span>
          </label>
          <input type="text"
             id="time"
             class="form-control"
             :class="errors.length > 0 ? 'border-danger bg-warning' : ''"
             :disabled="disabled"
              placeholder="HHMM"
              :value="timeSegment"
              @input="updateTimeSegment">
        </div>

      </div>
      <div class="small text-danger ml-1">{{ errors[0] }}</div>
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
    setDateTime(isoDateTimeString) {
      const payload = {target: {id: this.id, value: isoDateTimeString }}
      this.$store.commit("updateFormField", payload)
    },
    timeAgo() {
      if(this.isValidDate) {
        this.timeAgoString = moment(this.getAttributeValue(this.id)).fromNow()
      }
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
    isFutureDate() {
      return moment().diff(this.getAttributeValue(this.id), "millisecond") < 0
    },
    dateSegment() {
      return this.getAttributeValue(this.id).split(' ')[0];
    },
    timeSegment() {
      let timeArray = this.getAttributeValue(this.id).split(' ');
      if (timeArray.length > 1) {
        return timeArray[1]
      } else {
        return ''
      }
    },
    displayDateNotValid() {
      let dateTimeArray = this.getAttributeValue(this.id).split(' ');
      if (this.getAttributeValue(this.id).length === 0) {
        return false;
      } else {
        return ! (dateTimeArray[0].length === 8)
      }
    },
    displayTimeNotValid() {
      let dateTimeArray = this.getAttributeValue(this.id).split(' ');
      if (this.getAttributeValue(this.id).length === 0) {
        return false;
      } else {
        return ! (dateTimeArray[1].length === 4)
      }
    },
    displayTimeAgoString() {
      return this.isValidDate && ! this.displayDateNotValid && ! this.displayTimeNotValid;
    }
  }

}
</script>
