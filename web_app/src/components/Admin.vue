<template>
  <div v-if="isUserAnAdmin" class="card w-100 mt-3 mb-3">
      <div class="card-header text-white text-left font-weight-bold small pl-3 pt-1 pb-1 bg-primary">
        User Management
      </div>
      <div class="card-body text-left pb-1">
        <table class="table table-striped">
          <tbody>
            <tr>
              <th>SURNAME</th>
              <th>Given</th>
              <th>Prime ID</th>
              <th>Agency</th>
              <th>Keycloak GUID</th>
              <th>Username</th>
              <th>Role</th>
              <th>Date Applied</th>
              <th colspan="2">Action</th>
            </tr>
            <admin-user-role v-for="(user, index) in getAllUsers" :key="index" :user="user"></admin-user-role>
          </tbody>
        </table>
      </div>
     <add-user-role></add-user-role>
  </div>
</template>
<script>
  import AddUserRole from "@/components/AddUserRole";
  import AdminUserRole from "@/components/AdminUserRole";
  import {mapActions, mapGetters} from "vuex";
  export default {
    name: "Admin",
    computed: {
      ...mapGetters([
        'isUserAnAdmin',
        'getAllUsers'
      ]),
    },
    methods: {
      ...mapActions([
        'fetchStaticLookupTables'
      ])
    },
    created() {
      this.fetchStaticLookupTables({
        "admin": true,
        "resource": "users",
        "static": false
      })
    },
    components: {
      AddUserRole,
      AdminUserRole
    }
  }
</script>