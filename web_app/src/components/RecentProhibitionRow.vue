<template>
  <tr v-if="prohibition">
    <td>
      {{ prohibition.data.last_name }},
      {{ prohibition.data.first_name }}
      ({{ prohibition.data.drivers_number }})<br />
      <span class="text-muted text-secondary">{{ prohibition_number }}</span>
    </td>
    <td>{{ prohibition.short_name }}</td>
    <td>Not Served</td>
    <td>Not Submitted</td>
    <td>
      <h6>
        <b-icon-trash variant="danger" @click="deleteEditedForm(prohibition_number)"></b-icon-trash>&nbsp;
        <b-icon-pen variant="primary" @click="editExistingForm(prohibition_number)"></b-icon-pen>
      </h6>
    </td>
  </tr>
</template>

<script>

import { mapMutations } from 'vuex';

export default {
  name: "RecentProhibitionRow",
  props: {
    prohibition_number: null,
    prohibition: {}
  },
  methods: {
    ...mapMutations(["deleteEditedForm", "editExistingForm"]),
  }
}
</script>
