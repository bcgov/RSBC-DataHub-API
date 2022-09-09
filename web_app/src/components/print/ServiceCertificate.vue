<template>
  <div v-if="isDocumentServed(getPath)">
    <div id="print-instructions" class="card text-dark mb-2">
      <div class="card-header text-left">
        <div class="font-weight-bold">Print this page</div>
        <div class="small text-muted">If you need it for your records</div>
        <div class="text-right">
          <div class="btn btn-primary btn-sm"  @click="goHome">Close and return to Home</div>
      </div>
      </div>

    </div>
    <service-certificate-wording
      :form_full_name="getOfficialFormName(getPath)"
      :served_date="getPrintedDate(getPath)"
      :form_id="formattedNoticeNumber(getPath)"
      :driver_name="concatenateDriverName(getPath)"
      :officer_name="getAttributeValue(getPath, 'officer_name')"
      :badge_number="getAttributeValue(getPath, 'badge_number')"
      :agency="getAttributeValue(getPath, 'agency')"
      :certified_date="getCertifiedDate(getPath)">
    </service-certificate-wording>
  </div>
</template>

<script>

import {mapGetters} from "vuex";
import ServiceCertificateWording from "@/components/print/ServiceCertificateWording";

export default {
    name: "ServiceCertificate",
    props: {
      form_type: {
        type: String
      },
      id: {
        type: String,
      },
    },
    computed: {
      ...mapGetters(['getFormData',
        "getCertifiedDate",
        "getOfficialFormName",
        "getAttributeValue",
        "getPrintedDate",
        "isDocumentServed",
        "concatenateDriverName",
        "formattedNoticeNumber"]),

      getPath() {
        return `forms/${this.form_type}/${this.id}/data`
      }
    },
    components: {
      ServiceCertificateWording
    },
    methods: {
      goHome() {
        this.$router.replace({name: 'Home'})
      }
    }
}
</script>


<style scoped>

  .row {
    margin: 0 0 0 0;
    padding: 0 0 0 0;
  }

  .cell {
    color: black;
    text-align: left;
    border: 1px solid lightgrey;
  }

  .cos-table {
    padding-top: 1em;
  }

  .data {
    font-weight: bold;
    text-transform: uppercase;
  }

  @media print {
    #roadsafety-header {
     display: none;
    }
    #debug-component {
     display: none;
    }
    #not-authenticated-banner {
     display: none;
    }

    #print-instructions {
      display: none;
    }

    #certificate-of-service {
      margin-top: 25mm;
      border: none;
      page-break-before:always;
    }

    @page {
      margin: 0;

    }
  }

</style>
