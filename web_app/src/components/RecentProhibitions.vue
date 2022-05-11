<template>
    <div class="card w-100 mt-3 mb-3">
      <div class="card-header text-white text-left font-weight-bold small pl-3 pt-1 pb-1 bg-primary">
        Recent Prohibitions
      </div>
      <div class="card-body text-left pb-1">
        <table class="table table-striped">
          <tbody>
            <recent-prohibition-row v-for="(prohibition, index) in getAllEditedFormsNotPrinted"
                                    :key="index"
                                    :prohibition="prohibition">
            </recent-prohibition-row>
            <div class="text-muted small" v-if="getAllEditedFormsNotPrinted.length === 0">
              There are no recently created prohibitions that have not been printed
            </div>
          </tbody>
        </table>
      </div>
    </div>
</template>

<script>

import RecentProhibitionRow from "@/components/RecentProhibitionRow";
import {mapGetters} from 'vuex';

export default {
  name: "RecentProhibitions",
  computed: {
    ...mapGetters(["getAllEditedFormsNotPrinted"]),
  },
  components: {
    RecentProhibitionRow
  }
}
</script>

<style scoped>

</style>