<template>
    <div class="card-body text-left form-group">
      <label class="small" for="username">Add an admin user</label>
      <div class="input-group mb-3">

       <select class="form-control" id="username" v-model="newUser">
          <option v-for="(user, id) in getAllUsers"
                  :value="user"
                  :key="id">
            {{ user.username }}
          </option>
       </select>
        <div class="input-group-append">
          <div class="btn-secondary btn btn-sm pt-2"  @click="triggerAddUserRole">
            Add <b-spinner v-if="showSpinner" small></b-spinner>
          </div>
        </div>
      </div>
    </div>
</template>

<script>

import {mapActions, mapGetters} from "vuex";

export default {
  name: "AddUserRole",
  data() {
    return {
      showSpinner: false,
      newUser: {}
    }
  },
  computed: {
    ...mapGetters(['isUserAnAdmin', 'getAllUsers']),
  },
  methods: {
    ...mapActions(['adminAddUserRole']),
    triggerAddUserRole() {
      this.showSpinner = true;
      this.adminAddUserRole(this.newUser)
        .then( () => {
          this.showSpinner = false;
          this.newUser = {}
        })
        .catch( () => {
          this.showSpinner = false;
          this.newUser = {}
        })

    }
  }
}
</script>

<style scoped>

</style>