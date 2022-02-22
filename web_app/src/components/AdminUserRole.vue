<template>
    <tr>
      <td class="small">{{ user.first_name }}</td>
      <td class="small">{{ user.last_name }}</td>
      <td class="small">{{ user.badge_number }}</td>
      <td class="small">{{ user.agency }}</td>
      <td class="small">{{ user.username }}</td>
      <td><h2 class="badge badge-secondary">{{ user.role_name }}</h2></td>
      <td class="text-muted small">{{ submittedDate }} Pacific Time</td>
      <td>
        <button class="btn-success btn btn-sm" v-if="! isApproved" @click="triggerApproveUserRole">
          Approve <b-spinner v-if="approveSpinner" small></b-spinner>
        </button>
      </td>
      <td>
        <button class="btn-danger btn btn-sm" v-if="isApproved" @click="triggerDeleteUserRole">
            Delete <b-spinner v-if="deleteSpinner" small></b-spinner>
          </button>
      </td>
    </tr>
</template>

<script>

import {mapActions, mapGetters} from "vuex";
import moment from 'moment-timezone'

export default {
  name: "AdminUserRole",
  data() {
    return {
      approveSpinner: false,
      deleteSpinner: false
    }
  },
  props: {
      user: {
        first_name: '',
        last_name: '',
        badge_number: '',
        user_guid: '',
        username: {},
        role_name: {},
        approved_dt: {},
        submitted_dt: {}
      }
  },
  computed: {
    ...mapGetters(['isUserAnAdmin', 'getAllUsers']),
    isApproved() {
      return this.user.approved_dt
    },
    submittedDate() {
      return moment(this.user.submitted_dt).tz("UTC").format("YYYY-MM-DD HH:mm")
    }
  },
  methods: {
    ...mapActions(['adminApproveUserRole', 'adminDeleteUserRole']),
    triggerApproveUserRole() {
      this.approveSpinner = true;
      this.adminApproveUserRole(this.user)
        .then( () => {
          this.approveSpinner = false;
        })
        .catch( () => {
          this.approveSpinner = false;
        })
    },
    triggerDeleteUserRole() {
      this.deleteSpinner = true;
      const payload = {
        user_guid: this.user.user_guid,
        role_name: this.user.role_name
      }
      this.adminDeleteUserRole(payload)
        .then( () => {
          this.deleteSpinner = false;
        })
        .catch( () => {
          this.deleteSpinner = false;
        })
    },
  }
}
</script>

<style scoped>

</style>