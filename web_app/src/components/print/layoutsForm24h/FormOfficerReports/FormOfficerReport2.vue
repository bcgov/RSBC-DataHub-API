<template>
    <div v-if="dataReady">        
        <div class="row lineheight0-25" style="font-size:11pt; margin:0.75rem 0 0 0;   line-height:1rem;"><b>2) Reasonable Grounds</b></div>
        <div style="text-align:justify; font-size:8.5pt; line-height:0.85rem; margin:0 1rem 0 1.5rem; ">
            Was a prescribed Approved Screening Device (ASD), Approved Instrument
            or prescribed physical coordination test used to form reasonable grounds
            to believe that the driver’s ability to drive a motor vehicle was affected by
            alcohol or a drug?           
        </div>
       
        
        <div class="row margin-top-0" style="font-size:9pt; margin:0.4rem 0 0 0;">
            <table class="border-0 border-dark text-left" style="width:100%; line-height:0.5rem;">
                
                <tr style="height:0.01rem; line-height:0.01rem;">
                    <td v-for="inx in Array(100)" :key="inx" class="border-0 border-dark" style="width:1%;" />                                                                                
                </tr>

<!-- <YES-NO> -->
                <tr style="height:0.5rem;  line-height:1rem;">
                    <td class="" style="" colspan="3"></td>                 
                    <td class="" style="" colspan="5">
                        <check-box
                            shiftBox="20px,-2px"
                            shiftmark="0px,-1px"                                   
                            checkColor="#2134AB"
                            boxSize="1.25em" 
                            :check="formData.testPrescribed"
                            checkFontSize="16pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="7">Yes</td>
                    <td class="" style="" colspan="5">
                        <check-box
                            shiftBox="20px,-2px"
                            shiftmark="0px,-1px"                                   
                            checkColor="#2134AB"
                            boxSize="1.25em" 
                            :check="!formData.testPrescribed"
                            checkFontSize="16pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="25">No</td>
                    <td class="answer" style="" colspan="29"> {{formData.reasonNoTest}}</td>                                               
                </tr>

                <tr style="height:1.5rem;  line-height:1.5rem;">
                     <td class="" style="" colspan="4"></td>
                    <td class="" style="font-size:8.5pt;" colspan="96">
                        If yes, which test was administered?
                    </td>
                </tr>

<!-- <ALCO> -->
                <tr style="height:0.5rem;  line-height:1rem;">
                    <td class="" style="" colspan="3"></td>                 
                    <td class="" style="" colspan="5">
                        <check-box
                            shiftBox="20px,-2px"
                            shiftmark="0px,-1px"                                   
                            checkColor="#2134AB"
                            boxSize="1.25em" 
                            :check="formData.fstTest"
                            checkFontSize="16pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="30">Alco-Sensor FST</td>
                    
                    <td class="" style="" colspan="23">ASD Expiry Date</td>
                    <td class="answer" style="border-bottom:1px solid black;" colspan="39">{{formData.asdExpiryDate}}</td>
                                            
                </tr>
<!-- <APPROVED INSTRUMENT> -->
                <tr style="height:0.5rem;  line-height:1rem;">
                    <td class="" style="" colspan="3"></td>                 
                    <td class="" style="" colspan="5">
                        <check-box
                            shiftBox="20px,-2px"
                            shiftmark="0px,-1px"                                   
                            checkColor="#2134AB"
                            boxSize="1.25em" 
                            :check="formData.approvedInstrumentTest"
                            checkFontSize="16pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="40">Approved Instrument (specify)</td>
                    <td class="answer" style="border-bottom:1px solid black;" colspan="52">{{formData.approvedInstrumentType}}</td>                                            
                </tr>
<!-- <PRESCRIBED> -->
                <tr style="height:0.5rem;  line-height:1rem;">
                    <td class="" style="" colspan="3"></td>                 
                    <td class="" style="" colspan="5">
                        <check-box
                            shiftBox="20px,-2px"
                            shiftmark="0px,-1px"                                   
                            checkColor="#2134AB"
                            boxSize="1.25em" 
                            :check="formData.prescribedPhysicalTest"
                            checkFontSize="16pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="92">Prescribed Physical Coordination Test<span style="margin-left: 0.8rem;" class="answer">{{formData.prescribedPhysicalTestType}}</span></td>
                </tr>

<!-- <Time of test> -->                
                <tr style="height:0.5rem;  line-height:0.8rem;"><td></td></tr>
                <tr style="height:0.85rem;  line-height:0.8rem;">
                    <td class="" style="" colspan="4"></td>                                     
                    <td class="" style="" colspan="16">Time of Test</td>
                    <td class="answer" style="border-bottom:1px solid black;" colspan="20">{{formData.testDateTime}}</td> 
                    <td class="" style="" colspan="60"></td>                                          
                </tr>
                <tr style="height:0.25rem;  line-height:0.8rem;"></tr>
  <!-- <Result: Alcohol> -->                 
                <tr style="height:0.5rem;  line-height:1.2rem;">
                    <td class="" style="" colspan="4"></td>                                     
                    <th class="" style="text-decoration:underline" colspan="26">Result: Alcohol</th>
                </tr>              
                <tr style="height:0.5rem;  line-height:1rem; border-top:0px solid;">
                    <td class="" style="" colspan="3"></td>                 
                    <td class="" style="" colspan="5">
                        <check-box
                            shiftBox="20px,-2px"
                            shiftmark="0px,-1px"                                   
                            checkColor="#2134AB"
                            boxSize="1.25em" 
                            :check="formData.alcoholUnder99"
                            checkFontSize="16pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="20">51–99 mg%</td>
                    <td class="" style="" colspan="5">
                        <check-box
                            shiftBox="20px,-2px"
                            shiftmark="0px,-1px"                                   
                            checkColor="#2134AB"
                            boxSize="1.25em" 
                            :check="formData.alcoholOver99"
                            checkFontSize="16pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="20">Over 99 mg%</td>
                    <td class="" style="" colspan="5">
                        <check-box
                            shiftBox="20px,-2px"
                            shiftmark="0px,-1px"                                   
                            checkColor="#2134AB"
                            boxSize="1.25em" 
                            :check="formData.alcoholBac"
                            checkFontSize="16pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="7">BAC</td>
                    <td class="answer" style="border-bottom:1px solid black;" colspan="35">{{formData.alcoholBacResult}}</td>
                </tr>

<!-- <Result: Drug> -->                 
                <tr style="height:0.5rem;  line-height:1.2rem;">
                    <td class="" style="" colspan="4"></td>                                     
                    <th class="" style="text-decoration:underline" colspan="26">Result: Drug</th>
                </tr>              
                <tr style="height:0.5rem;  line-height:1rem; border-top:0px solid;">
                    <td class="" style="" colspan="3"></td>                 
                    <td class="" style="" colspan="5">
                        <check-box
                            shiftBox="20px,-2px"
                            shiftmark="0px,-1px"                                   
                            checkColor="#2134AB"
                            boxSize="1.25em" 
                            :check="formData.drugTestAffected"
                            checkFontSize="16pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="92">Ability to drive affected by a drug 
                        <span class="answer" style="margin-right: 1rem;">{{formData.drugResults}}</span>
                    </td>
                </tr>

                
            </table>
        </div>
    </div>           
</template>     
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { namespace } from "vuex-class";

import "@/store/modules/forms/mv2634";
const mv2634State = namespace("MV2634");

import CheckBox from "../../pdfUtil/CheckBox.vue";
import { twentyFourHourFormDataInfoType, twentyFourHourFormJsonInfoType } from '@/types/Forms/MV2634';

@Component({
    components:{       
        CheckBox           
    }
})
export default class FormOfficerReport2 extends Vue {

    @mv2634State.State
    public mv2634Info: twentyFourHourFormJsonInfoType;   

    dataReady = false;

    formData;

    mounted(){
        this.dataReady = false;
        this.extractInfo();
        this.dataReady = true;
    }

    public extractInfo(){

        const form24 = this.mv2634Info.data

        this.formData = {
            testPrescribed: false,
            reasonNoTest: '',
            fstTest: false,           
            asdExpiryDate: '',
            alcoholOver99: false,
            alcoholUnder99: false,
            approvedInstrumentTest: false,
            approvedInstrumentType: '',
            alcoholBac: false,
            prescribedPhysicalTest: false,
            prescribedPhysicalTestType: '',
            alcoholBacResult: '',
            drugsProhibition: false,            
            testDateTime: '',            
            drugTestAffected: false,
            drugResults: ''                                 
        }

        if (form24.prescribedTest){

            this.formData.testPrescribed = true; 
            this.formData.reasonNoTest = '';    

            if (form24.prohibitionType && form24.prohibitionType == 'Alcohol'){

                this.formData.drugTestAffected = false;   
                this.formData.drugsProhibition = false; 
                this.formData.drugResults = '';

                this.determineTestDateTime(form24);               

                const alcoholTest = form24.alcoholTest?form24.alcoholTest:''; 

                if (alcoholTest == 'Alco-Sensor FST (ASD)'){

                    this.formData.fstTest = true;
                    this.formData.approvedInstrumentTest = false;
                    this.formData.approvedInstrumentType = '';
                    this.formData.prescribedPhysicalTest = false;
                    this.formData.prescribedPhysicalTestType = '';
                    this.formData.alcoholBac = false;
                    this.formData.alcoholBacResult = '';
                    this.formData.asdExpiryDate = form24.asd?.expiryDate?Vue.filter('format-date-dash')(form24.asd.expiryDate):'';
                    this.formData.alcoholOver99 = form24.asd?.result?(form24.asd.result == 'over'):false;
                    this.formData.alcoholUnder99 = form24.asd?.result?(form24.asd.result == 'under'):false;

                } else if (alcoholTest == 'Approved Instrument'){

                    this.formData.fstTest = false;
                    this.formData.approvedInstrumentTest = true;
                    this.formData.approvedInstrumentType = 'INTOX EC/IR II';
                    this.formData.alcoholBac = true;
                    this.formData.alcoholBacResult = form24.BacResult?form24.BacResult + ' MG%':'';
                    this.formData.prescribedPhysicalTest = false;
                    this.formData.prescribedPhysicalTestType = '';
                    this.formData.asdExpiryDate = '';
                    this.formData.alcoholOver99 = false;
                    this.formData.alcoholUnder99 = false;

                } else if (alcoholTest == 'Prescribed Physical Coordination Test (SFST)'){

                    this.formData.fstTest = false;
                    this.formData.approvedInstrumentTest = false;
                    this.formData.approvedInstrumentType = ''
                    this.formData.alcoholBac = false;
                    this.formData.alcoholBacResult = '';
                    this.formData.prescribedPhysicalTest = true;
                    this.formData.prescribedPhysicalTestType = 'SFST';
                    this.formData.asdExpiryDate = '';
                    this.formData.alcoholOver99 = false;
                    this.formData.alcoholUnder99 = false;

                } else {                    
                    this.formData.fstTest = false;
                    this.formData.asdExpiryDate = '';
                    this.formData.alcoholOver99 = false;
                    this.formData.alcoholUnder99 = false;
                    this.formData.approvedInstrumentTest = false;
                    this.formData.approvedInstrumentType = '';
                    this.formData.prescribedPhysicalTest = false;
                    this.formData.prescribedPhysicalTestType = '';
                    this.formData.alcoholBac = false;
                    this.formData.alcoholBacResult = '';
                }            
                

            } else if (form24.prohibitionType && form24.prohibitionType == 'Drugs') {

                this.formData.fstTest = false;     
                this.formData.asdExpiryDate = '';                
                this.formData.alcoholOver99 = false;
                this.formData.alcoholUnder99 = false;                
                this.formData.alcoholBac = false;                
                this.formData.alcoholBacResult = '';

                this.determineTestDateTime(form24);

                const drugTest = form24.drugsTest?form24.drugsTest:'';
               
                if (drugTest == 'Approved Drug Screening Equipment'){

                    this.formData.prescribedPhysicalTest = false;
                    this.formData.prescribedPhysicalTestType = '';                    

                    this.formData.approvedInstrumentTest = true;
                    this.formData.approvedInstrumentType = 'ADSE';
                    const drugResults = form24.approvedDrugScreeningEquipment?.length>0?form24.approvedDrugScreeningEquipment:[];
                    if (drugResults.length == 2){
                        this.formData.drugResults = 'THC AND COCAINE';
                    } else {
                        this.formData.drugResults = drugResults.toString().toUpperCase();
                    }
                    this.formData.drugTestAffected = true;                    
                } else if (drugTest == 'Prescribed Physical Coordination Test (SFST)'){
                    
                    this.formData.prescribedPhysicalTest = true;
                    this.formData.prescribedPhysicalTestType = 'SFST';
                    this.formData.approvedInstrumentTest = false;
                    this.formData.approvedInstrumentType = '';
                    this.formData.drugResults = '';                   
                    this.formData.drugTestAffected = true;

                } else if (drugTest == 'Prescribed Physical Coordination Test (DRE)'){
                    
                    this.formData.prescribedPhysicalTest = true;
                    this.formData.prescribedPhysicalTestType = 'DRE';
                    this.formData.approvedInstrumentTest = false;
                    this.formData.approvedInstrumentType = '';
                    this.formData.drugResults = '';                   
                    this.formData.drugTestAffected = true;

                } else {

                    this.formData.approvedInstrumentTest = false;
                    this.formData.approvedInstrumentType = ''; 
                    this.formData.prescribedPhysicalTest = false;
                    this.formData.prescribedPhysicalTestType = '';
                    this.formData.drugResults = '';                   
                    this.formData.drugTestAffected = false; 
                } 

            } else {
                this.resetTestFields();                
                this.formData.reasonNoTest = form24.prescribedNoTestReason?form24.prescribedNoTestReason.toUpperCase():'';
            }
                  

        } else {
            this.resetTestFields();
            this.formData.reasonNoTest = form24.prescribedNoTestReason?form24.prescribedNoTestReason.toUpperCase():'';  
            if (form24.prohibitionType){
                this.formData.drugTestAffected = form24.prohibitionType == 'Drugs';
            }     

        }

        
    }

    public determineTestDateTime(form24: twentyFourHourFormDataInfoType){
        if (form24.prescribedTestDate && form24.prescribedTestTime){
            const testTime = form24.prescribedTestTime.substr(0,2)+ ':' + form24.prescribedTestTime.substr(2,2);        
            this.formData.testDateTime = Vue.filter('format-date-dash')(form24.prescribedTestDate) + ' ' + testTime;

        } else {
            this.formData.testDateTime = '';
        }
    }                
    
    public resetTestFields(){

        this.formData.testPrescribed = false;
        this.formData.fstTest = false;     
        this.formData.asdExpiryDate = '';
        this.formData.testDateTime = '';
        this.formData.alcoholOver99 = false;
        this.formData.alcoholUnder99 = false;
        this.formData.approvedInstrumentTest = false;
        this.formData.approvedInstrumentType = '';
        this.formData.alcoholBac = false;
        this.formData.prescribedPhysicalTest = false;
        this.formData.prescribedPhysicalTestType = '';
        this.formData.alcoholBacResult = '';
        this.formData.drugsProhibition = false;
        this.formData.drugTestAffected = false; 
        this.formData.drugResults = '';

    }

    
}

</script>

<style scoped>

.answer {
    color: rgb(3, 19, 165);
    font-size: 7pt;
    font-weight: 600;
}

.lineheight0-25{
    line-height:0.25rem !important;
}
.lineheight0-50{
    line-height:0.5rem !important;
}
.lineheight0-75{
    line-height:0.75rem !important;
}

.margin-top-0{
    margin-top: 0rem !important;
}

</style>