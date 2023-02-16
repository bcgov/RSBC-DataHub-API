<template>
    <div class="card-body text-left form-group">
      <label class="small" for="username">Grant administrator role to an existing user</label>
      <div class="input-group mb-3">
       <select class="form-control" id="username" v-model="newUser">
          <option v-for="(user, id) in getAllUsers" :key="id" :value="user">
            {{ user.username }}
          </option>
       </select>
       &nbsp;
        <div class="input-group-append">
          <div class="btn-secondary btn btn-sm pt-2" @click="triggerAddUserRole">
            Add as Administrator
            <b-spinner v-if="showSpinner" small></b-spinner>
          </div>
        </div>
      </div>
    </div>
</template>
<script>
  import { mapActions, mapGetters } from "vuex";
  export default {
    name: "AddUserRole",
    computed: {
      ...mapGetters([
        'getAllUsers',
        'isUserAnAdmin'
      ]),
    },
    data() {
      return {
        newUser: {},
        showSpinner: false
      }
    },
    methods: {
      ...mapActions([
        'adminAddUserRole'
      ]),
      triggerAddUserRole() {
        this.showSpinner = true;
        this.adminAddUserRole(this.newUser)
        .then( () => {
          this.showSpinner = false;
          this.newUser = {};
        })
        .catch( () => {
          this.showSpinner = false;
          this.newUser = {};
        })
      }
    }
  }
</script>