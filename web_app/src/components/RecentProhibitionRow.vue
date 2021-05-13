<template>
  <tr v-if="prohibition">
    <td>
      {{ prohibition.data.last_name }},
      {{ prohibition.data.first_name }}
      ({{ prohibition.data.drivers_number }})
    </td>
    <td>{{ prohibition.short_name }}</td>
    <td>{{ getServedStatus(prohibition_index) }}</td>
    <td><span class="text-muted text-secondary small">{{ prohibition.data.prohibition_number }}</span></td>
    <td>
      <h6>
        <b-icon-trash v-if="isFormEditable(prohibition_index)" variant="danger" @click="deleteSpecificForm(prohibition_index)"></b-icon-trash>&nbsp;
        <b-icon-pen v-if="isFormEditable(prohibition_index)" variant="primary" @click="editExistingForm(prohibition_index)"></b-icon-pen>


        <span v-if=" ! isFormEditable(prohibition_index)" class="text-muted text-secondary">
          <b-icon-clock variant="primary" @click="deleteSpecificForm(prohibition_index)"></b-icon-clock>
          <span class="small"> Sending ...</span>
        </span>
      </h6>
    </td>
  </tr>
</template>

<script>

import { mapMutations, mapGetters, mapActions } from 'vuex';

export default {
  name: "RecentProhibitionRow",
  props: {
    prohibition_index: null,
    prohibition: {}
  },
  computed: {
    ...mapGetters(["isFormEditable", "getServedStatus"])
  },
  methods: {
    ...mapMutations(["editExistingForm"]),
    ...mapActions(["deleteSpecificForm"])
  }
}
</script>
