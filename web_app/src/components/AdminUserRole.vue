<template>
    <tr>
        <td class="small">{{ user.username }}</td>
        <td><h2 class="badge badge-secondary">{{ user.role_name }}</h2></td>
        <td class="text-muted small">{{ user.submitted_dt }}</td>
        <td>
          <button class="btn-secondary btn btn-sm" v-if="! isApproved" @click="triggerApproveUserRole">
            Approve <b-spinner v-if="approveSpinner" small></b-spinner>
          </button>

        </td>
      <td>
        <button class="btn-secondary btn btn-sm" v-if="isApproved" @click="triggerDeleteUserRole">
            Delete <b-spinner v-if="deleteSpinner" small></b-spinner>
          </button>
      </td>
    </tr>
</template>

<script>

import {mapActions, mapGetters} from "vuex";

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
    }
  },
  methods: {
    ...mapActions(['adminApproveUserRole', 'adminDeleteUserRole']),
    triggerApproveUserRole() {
      this.approveSpinner = true;
      this.adminApproveUserRole(this.user.username)
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
        username: this.user.username,
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