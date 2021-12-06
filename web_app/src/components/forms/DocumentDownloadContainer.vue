<template>
  <form-card title="Download Documents">
    <div class="d-flex justify-content-between">
      <document-download v-for="(document, kid) in documentObjects" :key="kid" :document=document :kid=kid>

      </document-download>
    </div>
  </form-card>
</template>

<script>
import CardsCommon from "@/components/forms/CardsCommon";
import DocumentDownload from "@/components/forms/DocumentDownload";
import {mapGetters} from "vuex";

export default {
  name: "DocumentDownloadContainer",
  mixins: [CardsCommon],
  computed: {
    ...mapGetters(["documentObjects"]),
  },
  components: {
    DocumentDownload
  }
}
</script>
