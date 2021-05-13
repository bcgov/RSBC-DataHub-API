<template>
    <div class="card w-100 mt-3 mb-3">
      <div class="card-header text-white text-left font-weight-bold small pl-3 pt-1 pb-1 bg-primary">
        Recent Prohibitions
      </div>
      <div class="card-body text-left pb-1">
        <table class="table table-striped">
          <tbody>
            <recent-prohibition-row v-for="(prohibition, index) in getAllEditedProhibitions"
                                    :key="index"
                                    :prohibition="prohibition"
                                    :prohibition_number="prohibition.data.prohibition_number"
                                    :prohibition_index="index">
            </recent-prohibition-row>
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
    ...mapGetters(["getAllEditedProhibitions", "getSpecificForm"]),
  },
  components: {
    RecentProhibitionRow
  }
}
</script>

<style scoped>

</style>