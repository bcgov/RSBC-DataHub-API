<template>
    <b-card v-if="dataReady" :name="pageId"  bg-variant="info" class="pdf-container bg-white svg-wrapper" no-body>
        <div style="font-size:1pt;color:#FFF;"><b>i</b></div>
            <div class="row mx-0">
                <div class="col  ml-0">                
                    <form24h-table1 />
                    <form24h-table2 />
                    <form24h-table3 />
                    <form24h-table4 />
                    <form24h-table5 />
                    <form24h-table6 />
                    <form24h-table7 />
                    <form24h-table8 :copyType="copyType"/>
                </div>

                <div class="col ml-0">
                    <div v-if="copyType=='DRIVER COPY'">
                        <form24-notice />
                    </div>
                    <div v-else>
                        <form-officer-report1 />
                        <form-officer-report2 />
                        <form-officer-report3 />
                    </div>
                </div>
            </div>

    </b-card>
</template>     
<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';


import CheckBox from "../pdfUtil/CheckBox.vue";
import Form24hTable1 from "./Form24Tables/Form24hTable1.vue";
import Form24hTable2 from "./Form24Tables/Form24hTable2.vue";
import Form24hTable3 from "./Form24Tables/Form24hTable3.vue";
import Form24hTable4 from "./Form24Tables/Form24hTable4.vue";
import Form24hTable5 from "./Form24Tables/Form24hTable5.vue";
import Form24hTable6 from "./Form24Tables/Form24hTable6.vue";
import Form24hTable7 from "./Form24Tables/Form24hTable7.vue";
import Form24hTable8 from "./Form24Tables/Form24hTable8.vue";

import Form24Notice from "./Form24Notice.vue"

import FormOfficerReport1 from "./FormOfficerReports/FormOfficerReport1.vue"
import FormOfficerReport2 from "./FormOfficerReports/FormOfficerReport2.vue"
import FormOfficerReport3 from "./FormOfficerReports/FormOfficerReport3.vue"

@Component({
    components:{       
        CheckBox,
        Form24hTable1,
        Form24hTable2,
        Form24hTable3, 
        Form24hTable4,
        Form24hTable5,
        Form24hTable6,
        Form24hTable7,
        Form24hTable8,
        Form24Notice,
        FormOfficerReport1,
        FormOfficerReport2,
        FormOfficerReport3,
    }
})
export default class Form24hLayout extends Vue {
    
    @Prop({required:true})
    copyType!: string;

    dataReady = false;
    pageId='';

    mounted(){
        this.dataReady = false;

        if(this.copyType.includes('ICBC')){
            this.pageId="print"
        }else{
            this.pageId=this.copyType.replace(' ','').toLowerCase()
        }

        // this.extractInfo();
        this.dataReady = true;
    }

    // public extractInfo(){
           
    // }

    
}

</script>

<style scoped type="text/css">

.answer {
    color: rgb(3, 19, 165);
    font-size: 7pt;
}

.pdf-container {
    padding: 0px !important; 
    margin-right: auto !important;
    margin-left: auto !important;
    width: 100% !important;
    max-width: 980px !important;
    min-width: 980px !important;
    font-size: 10pt !important;
    font-family: BCSans;
    color: #313132 !important;
    border: 0px solid;
}

.svg-wrapper {
    border-bottom: darkblue solid 1px;
}

@media print {

    @page {
        /* size: letter;
        margin: 0; */
        size:  8.5in 11in  !important;
        margin: 0.01in 0.01in !important;
    }

    html {
        margin: 0;
    }

    body {
        margin: 0;
    }

    #print-btn{
        display: none;
    }


    #roadsafety-header {
        display: none;
    }
    #debug-component {
        display: none;
    }
    #not-authenticated-banner {
        display: none;
    }

    .svg-wrapper {
        page-break-before:always !important;
        transform-origin: 580px 520px;
        transform: rotate(-90deg) scale(1.15);
        border:0px solid black;
    }
}

</style>