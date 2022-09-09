<template>
  <div>
    <div id="certificate-of-service" class="text-dark font-weight-bold text-uppercase text-left">
      Certificate of Service
    </div>
    <div class="text-dark text-left pt-2">
      I, the enforcement officer identified below, certify that on <span class="value">{{ served_date }}</span>
      served a printout, in the <span class="value">{{ form_full_name }}</span> under the
      <span class="font-italic">Motor Vehicle Act</span> or the <span class="font-italic">
      Motor Vehicle Act Regulations</span>, of notice number <span class="value">{{ form_id }}</span> on
      <span class="value">{{ driver_name }}</span> by personal delivery.
    </div>
    <div class="cos-table">
      <div class="row">
        <div class="col-6 cell">
          <div class="title">Enforcement Officer's Name</div>
          <div class="data value">{{ officer_name }}</div>
        </div>
        <div class="col-6 cell">
          <div class="title">Officer's Number</div>
          <div class="data value">{{ badge_number }}</div>
        </div>
      </div>
      <div class="row">
        <div class="col-12 cell">
          <div class="title">Organization / Detachment / Location of Officer</div>
          <div class="data value">{{ agency }}</div>
        </div>
      </div>
      <div class="row">
        <div class="col-12 cell">
          <div class="title">Date Certified (YYYY-MM-DD)</div>
          <div class="data value">{{ certified_date }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
    name: "ServiceCertificate",
    props: {
      driver_name: {
        type: String,
        default: '[error]'
      },
      form_id: {
        type: String,
        default: '[error]'
      },
      officer_name: {
        type: String,
        default: '[error]'
      },
      badge_number: {
        type: String,
        default: '[error]'
      },
      agency: {
        type: String,
        default: '[error]'
      },
      served_date: {
        type: String,
        default: '[error]'
      },
      form_full_name: {
        type: String,
        default: '[error]'
      },
      certified_date: {
        type: String,
        default: '[error]'
      },
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

  .value {
    color: darkblue;
  }

</style>
