<template>
    <div v-if="dataReady">        
        <div class="row lineheight0-25" style="font-size:11pt; margin:0.75rem 0 0 0;   line-height:1rem;"><b>3) After the Prohibition Served</b></div>
        <div style="text-align:justify; font-size:8.5pt; line-height:0.85rem; margin:0 1rem 0 1.5rem; ">
            Did the driver request a breath test or prescribed physical coordination test?           
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
                            :check="false"
                            checkFontSize="16pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="25">No</td>
                    <td class="" style="" colspan="29">{{formData.reasonNoTest}} </td>                                               
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
                    <td class="" style="" colspan="35">Yes, Alco-Sensor FST</td>
                    
                    <td class="" style="" colspan="24">ASD Expiry Date</td>
                    <td class="answer" style="border-bottom:1px solid black;" colspan="33">{{formData.asdExpiryDate}}</td>
                                            
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
                    <td class="" style="" colspan="46">Yes, Approved Instrument (specify)</td>
                    <td class="answer" style="border-bottom:1px solid black;" colspan="46">{{formData.approvedInstrumentType}}</td>                                            
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
                    <td class="" style="" colspan="92">Yes, Prescribed Physical Coordination Test<span style="margin-left: 0.8rem;" class="answer">{{formData.prescribedPhysicalTestType}}</span></td>
                </tr>
<!-- <test administrated> -->
                <tr style="height:0.5rem;  line-height:1rem;">
                    <td class="" style="" colspan="3"></td>                 
                    <td class="" style="" colspan="5">
                        <check-box
                            shiftBox="20px,-2px"
                            shiftmark="0px,-1px"                                   
                            checkColor="#2134AB"
                            boxSize="1.25em" 
                            :check="false"
                            checkFontSize="16pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="92">No, test was administered in forming reasonable grounds</td>
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
import { twentyFourHourFormJsonInfoType } from '@/types/Forms/MV2634';

@Component({
    components:{       
        CheckBox           
    }
})
export default class FormOfficerReport3 extends Vue {

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