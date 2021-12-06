<template>
  <div class="card w-100 mt-3 mb-3" v-if="isUserAnAdmin">
      <div class="card-header text-white text-left font-weight-bold small pl-3 pt-1 pb-1 bg-primary">
        User Roles
      </div>
      <div class="card-body text-left pb-1">
        <table class="table table-striped">
          <tbody>
            <admin-user-role v-for="(user, index) in getAllUsers" :key="index" :user="user"></admin-user-role>

          </tbody>
        </table>
      </div>
     <add-user-role></add-user-role>
  </div>
</template>

<script>

import {mapActions, mapGetters} from "vuex";
import AdminUserRole from "@/components/AdminUserRole";
import AddUserRole from "@/components/AddUserRole";

export default {
  name: "Admin",
  computed: {
    ...mapGetters(['isUserAnAdmin', 'getAllUsers']),
  },
  methods: {
    ...mapActions(['fetchStaticLookupTables'])
  },
  created() {
    this.fetchStaticLookupTables("users")
  },
  components: {
    AddUserRole,
    AdminUserRole
  }
}
</script>

<style scoped>

</style>