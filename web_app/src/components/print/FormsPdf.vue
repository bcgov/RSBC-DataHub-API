<template>
    <div v-if="dataReady">
        <b-card id="print-btn" class="bg-light"> 
            <b-button  @click="print()">Print</b-button>
        </b-card>

        <div v-if="form24">
            <form24h-layout  v-for="(value, inx) in ['DRIVER COPY','POLICE COPY','SEND TO ICBC']" v-bind:key="inx" :copyType="value"  />      
        </div>
        <div v-if="form12">
            <form12h-layout  v-for="(value, inx) in ['DRIVER COPY','POLICE COPY','SEND TO ICBC']"  v-bind:key="inx" :copyType="value"  />
        </div>
        <div v-if="formVI">
            <form-vi-layout  v-for="(value, inx) in ['DRIVER COPY', 'DRIVER INFO', 'ILO COPY', 'POLICE/SUPERINTENDENT COPY', 'SUPERINTENDENT/POLICE COPY']"  v-bind:key="inx" :copyType="value"  />
        </div>

    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import Form24hLayout from "./layoutsForm24h/Form24hLayout.vue"
import Form12hLayout from "./layoutsForm12h/Form12hLayout.vue"
import FormViLayout from "./layoutsFormVI/FormViLayout.vue"

import {tellApiFormIsPrinted} from "@/utils/forms"
import moment from "moment-timezone";

import { namespace } from "vuex-class";
import "@/store/modules/common";
const commonState = namespace("Common");

import "@/store/modules/forms/mv2906";
const mv2906State = namespace("MV2906");

import "@/store/modules/forms/mv2634";
const mv2634State = namespace("MV2634");

import { currentlyEditingFormObjectInfoType } from '@/types/Common';
import { twelveHourFormJsonInfoType } from '@/types/Forms/MV2906';
import { twentyFourHourFormJsonInfoType } from '@/types/Forms/MV2634';


@Component({
    components:{       
        Form24hLayout,
        Form12hLayout,
        FormViLayout
    }
})
export default class FormsPdf extends Vue {

    @commonState.State
    public currently_editing_form_object: currentlyEditingFormObjectInfoType;

    @commonState.Action
    public UpdateCurrentlyEditingFormObject!: (newCurrentlyEditingFormObject: currentlyEditingFormObjectInfoType) => void	

    //TODO -may remove
    @mv2906State.Action
    public UpdateMV2906Info!: (newMV2906Info: twelveHourFormJsonInfoType) => void

    @mv2634State.Action
    public UpdateMV2634Info!: (newMV2634Info: twentyFourHourFormJsonInfoType) => void;
    
    dataReady=false;
    form12=false;
    form24=false;
    formVI=false;

    timeoutHandle

    mounted(){
        this.dataReady=false; 
        this.init()
    }

    public init(){  //TODO - may remove in future 
             
        if(!this.currently_editing_form_object.form_type){
            
            const form_id = this.$route.params['id']
            const form_type = this.$route.params['form_type']
            const formData = this.$store.state.forms[form_type][form_id]

            console.log(formData)

            if(formData){                
                clearTimeout(this.timeoutHandle);
                this.UpdateCurrentlyEditingFormObject({
                    form_type:form_type,
                    form_id: form_id  
                })
                
                if(form_type=='12Hour')            
                    this.UpdateMV2906Info(formData)
                else if(form_type=='24Hour')            
                    this.UpdateMV2634Info(formData)

                this.determinePDFtype()
            }else{
                console.log('RETRY')
                this.timeoutHandle = window.setTimeout(this.init,500)
            }
        }else{
            this.determinePDFtype()
        }
    }

    public determinePDFtype(){
        const formType = this.currently_editing_form_object.form_type
        this.form12=(formType=="12Hour");
        this.form24=(formType=="24Hour");
        this.formVI=(formType=="VI");
        this.dataReady=true;
    }


    public submitToICBC(){
        const editingForm = this.currently_editing_form_object
        const current_timestamp = moment().format()
        const payload = {
            form_type: editingForm.form_type, 
            form_id:editingForm.form_id,
            timestamp:current_timestamp,
        }        
      
        this.$store.commit("setFormAsPrinted",payload) 

        const el= document.getElementsByName("print");
        if(el.length>0){
            const html= el.length==1? el[0].innerHTML : (el[0].innerHTML+el[1].innerHTML)
            const pdfhtml = Vue.filter('printPdf')(html, payload.form_type)
            this.$store.commit("addHtmlToForm",{payload:payload, html:pdfhtml})
            // console.log(pdfhtml)
        }

        tellApiFormIsPrinted(payload)
          .then( (response) => {
              console.log("response from tellApiFormIsPrinted()", response)
          })
          .catch( (error) => {
              console.log("no response from tellApiFormIsPrinted()", error)
          })
        // this.display_spinner = false;

    }

    print(){
        this.submitToICBC()
        window.print()
    }
}
</script>


<style type="text/css">

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

    #print-btn{
        display: none;
    }

    #app{
        margin:0;
        padding:0;
    }

    #router-container{
        margin:0;
        padding:0;
    }

}

</style>

