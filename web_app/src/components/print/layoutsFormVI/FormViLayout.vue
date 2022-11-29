<template>
    <b-card v-if="dataReady" :name="pageId"  bg-variant="info" class="pdf-container bg-white svg-wrapper" no-body>
        <div style="font-size:1pt;color:#FFF;"><b>i</b></div>

            <div v-if="copyType=='SUPERINTENDENT/POLICE COPY'" class="mx-0">
                <div class="col ml-0"> 
                    <form-rts-table0 />
                    <form-rts-table1 />
                    <form-rts-table2 />
                    <form-rts-table3 />
                    <form-rts-table4 />
                    <form-rts-table5 />
                    <form-rts-table6 :copyType="copyType"/>
                </div>
            </div>

            <div  v-else-if="copyType=='DRIVER INFO'" class=" mx-0">
                <div class="col  ml-0"> 
                    <form-vi-notice />
                </div>
            </div>

            <div v-else class="mx-0">
                <div class="col ml-0"> 
                    <form-vi-table0 />              
                    <form-vi-table1 />
                    <form-vi-table2 />
                    <form-vi-table3 />
                    <form-vi-table4 />
                    <form-vi-table5 />
                    <form-vi-table6 />
                    <form-vi-table7 />
                    <form-vi-table8 />
                    <form-vi-table9 :copyType="copyType"/>
                </div>
            </div>

           
            
           
           

    </b-card>
</template>     
<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';


import CheckBox from "../pdfUtil/CheckBox.vue";
import FormViTable0 from "./FormViTables/FormViTable0.vue";
import FormViTable1 from "./FormViTables/FormViTable1.vue";
import FormViTable2 from "./FormViTables/FormViTable2.vue";
import FormViTable3 from "./FormViTables/FormViTable3.vue";
import FormViTable4 from "./FormViTables/FormViTable4.vue";
import FormViTable5 from "./FormViTables/FormViTable5.vue";
import FormViTable6 from "./FormViTables/FormViTable6.vue";
import FormViTable7 from "./FormViTables/FormViTable7.vue";
import FormViTable8 from "./FormViTables/FormViTable8.vue";
import FormViTable9 from "./FormViTables/FormViTable9.vue";

import FormViNotice from "./FormViNotice.vue";

import FormRtsTable0 from "./FormRtsTables/FormRtsTable0.vue"
import FormRtsTable1 from "./FormRtsTables/FormRtsTable1.vue"
import FormRtsTable2 from "./FormRtsTables/FormRtsTable2.vue"
import FormRtsTable3 from "./FormRtsTables/FormRtsTable3.vue"
import FormRtsTable4 from "./FormRtsTables/FormRtsTable4.vue"
import FormRtsTable5 from "./FormRtsTables/FormRtsTable5.vue"
import FormRtsTable6 from "./FormRtsTables/FormRtsTable6.vue"

@Component({
    components:{       
        CheckBox,
        FormViTable0,
        FormViTable1,
        FormViTable2,
        FormViTable3,
        FormViTable4,
        FormViTable5,
        FormViTable6,
        FormViTable7,
        FormViTable8,
        FormViTable9,

        FormViNotice,

        FormRtsTable0,
        FormRtsTable1,
        FormRtsTable2,
        FormRtsTable3,
        FormRtsTable4,
        FormRtsTable5,
        FormRtsTable6,

    }
})
export default class FormViLayout extends Vue {
    
    @Prop({required:true})
    copyType!: string;

    dataReady = false;
    pageId='';

    mounted(){
        this.dataReady = false;

        if(this.copyType.includes('ICBC') || this.copyType.includes('SUPERINTENDENT')){
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
    margin-top: 1rem !important;
    margin-right: auto !important;
    margin-left: auto !important;
    width: 100% !important;
    max-width: 950px !important;
    min-width: 950px !important;
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
        size:  8.5in 11in  !important;
        margin: 0.1in 0.3in 0.1in 0.1in !important;
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
        border:0px solid black;        
    }
}

</style>