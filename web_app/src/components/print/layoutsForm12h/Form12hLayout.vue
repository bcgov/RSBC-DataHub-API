<template>
    <b-card v-if="dataReady" :name="pageId"  bg-variant="white" class="pdf-container bg-white svg-wrapper" no-body>
        <div style="font-size:1pt;color:#FFF;"><b>i</b></div>
        <div class="row mx-0">
            <div class="col  ml-0">                
                <form12h-table1 />
                <form12h-table2 />
                <form12h-table3 />
                <form12h-table4 />
                <form12h-table5 />
                <form12h-table6 :copyType="copyType"/>
            </div>

            <div class="col ml-0">                
                <form12-notice />               
            </div>
        </div>

    </b-card>
</template>     
<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';


import CheckBox from "../pdfUtil/CheckBox.vue";
import Form12hTable1 from "./Form12Tables/Form12hTable1.vue";
import Form12hTable2 from "./Form12Tables/Form12hTable2.vue";
import Form12hTable3 from "./Form12Tables/Form12hTable3.vue";
import Form12hTable4 from "./Form12Tables/Form12hTable4.vue";
import Form12hTable5 from "./Form12Tables/Form12hTable5.vue";
import Form12hTable6 from "./Form12Tables/Form12hTable6.vue";
import Form12Notice from "./Form12Notice.vue"

@Component({
    components:{       
        CheckBox,
        Form12hTable1,
        Form12hTable2,
        Form12hTable3,
        Form12hTable4,
        Form12hTable5,
        Form12hTable6,
        Form12Notice,        
    }
})
export default class Form12hLayout extends Vue {
    
    @Prop({required:true})
    copyType!: string;

    dataReady = false;
    pageId=''

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

    #roadsafety-header {
        display: none;
    }
    #debug-component {
        display: none;
    }
    #not-authenticated-banner {
        display: none;
    }

    /* .svg-wrapper {
        page-break-before:always;
        transform: rotate(-90deg) scale(1.3) translate(-200px);
    } */

    .svg-wrapper {
        /* font-family: BCSans; */
        page-break-before:always !important;
        transform-origin: 580px 520px;
        transform: rotate(-90deg) scale(1.15);
        border:0px solid black;
    }
}

</style>