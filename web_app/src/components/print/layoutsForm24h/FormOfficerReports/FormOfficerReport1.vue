<template>
    <div v-if="dataReady">
        <div class="lineheight0-25 text-center" style="font-size:11pt; margin:1.75rem 0 0 0;   line-height:1rem;"><b>Officer’s Report</b> (Continued)</div>
        <div class="row lineheight0-25" style="font-size:11pt; margin:0rem 0 0 0;   line-height:1rem;"><b>1) Driver</b></div>
        <div style="text-align:justify; font-size:8.5pt; line-height:0.85rem; margin:0 1rem 0 1.5rem; ">
            The driver identified on the reverse was operating a motor vehicle or had
            care or control of a motor vehicle for the purposes of section 215(1) of the
            Motor Vehicle Act based upon (provide evidence):
        </div>
       
        
        <div class="row margin-top-0" style="font-size:9pt; margin:0.4rem 0 0 0;">
            <table class="border-0 border-dark text-left" style="width:100%; line-height:0.5rem;">
                
                <tr style="height:0.01rem; line-height:0.01rem;">
                    <td v-for="inx in Array(100)" :key="inx" class="border-0 border-dark" style="width:1%;" />                                                                                
                </tr>

<!-- <ROW1> -->
                <tr style="height:0.5rem;  line-height:1rem; border-top:0px solid;">
                    <td class="" style="" colspan="3"></td>                 
                    <td class="" style="" colspan="5">
                        <check-box
                            shiftBox="20px,-2px"
                            shiftmark="0px,-1px"                                   
                            checkColor="#2134AB"
                            boxSize="1.25em" 
                            :check="formData.reasonableGrounds.includes('Witnessed by officer')"
                            checkFontSize="16pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="30">Witnessed by officer</td>
                    <td class="" style="" colspan="5">
                        <check-box
                            shiftBox="20px,-2px"
                            shiftmark="0px,-1px"                                   
                            checkColor="#2134AB"
                            boxSize="1.25em" 
                            :check="formData.reasonableGrounds.includes('Admission by driver')"
                            checkFontSize="16pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="30">Admission by driver</td>
                    <td class="" style="" colspan="1"> </td>                                               
                </tr>

<!-- <ROW2> -->
                <tr style="height:0.5rem;  line-height:1rem; border-top:0px solid;">
                    <td class="" style="" colspan="3"></td>                 
                    <td class="" style="" colspan="5">
                        <check-box
                            shiftBox="20px,-2px"
                            shiftmark="0px,-1px"                                   
                            checkColor="#2134AB"
                            boxSize="1.25em" 
                            :check="formData.reasonableGrounds.includes('Independent witness')"
                            checkFontSize="16pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="30">Independent witness</td>
                    <td class="" style="" colspan="5">
                        <check-box
                            shiftBox="20px,-2px"
                            shiftmark="0px,-1px"                                   
                            checkColor="#2134AB"
                            boxSize="1.25em" 
                            :check="formData.reasonableGrounds.includes('Other')"
                            checkFontSize="16pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="25">Other</td>
                    <td class="" style="" colspan="6"> </td>                                               
                </tr>
                <tr style="height:0.5rem;  line-height:1rem;">
                    <td class="" style="" colspan="4"></td>                    
                    <td class="answer" style="" colspan="94">{{formData.other}}</td>
                </tr>
                <tr style="height:0.5rem;  line-height:0.5rem;">
                    <td class="" style="" colspan="4"></td>
                    <td class="answer" style="" colspan="94"><div v-if="formData.videoSurveillance">VIDEO SURVEILLANCE</div></td>                    
                </tr>
                <!-- <tr style="height:2rem; line-height:1rem;" ></tr> -->
                <!-- <tr style="height:0.5rem; line-height:1rem;">
                    <td class="" style="" colspan="4"></td>
                    <td class="" style="" colspan="30">Additional Information:</td>
                    <td class="" style="border-bottom:1px solid black;" colspan="66"></td>
                </tr>
                <tr style="height:1rem;  line-height:1rem;">
                    <td class="" style="" colspan="4"></td>                    
                    <td class="" style="border-bottom:1px solid black;" colspan="96"></td>
                </tr>
                <tr style="height:1rem;  line-height:1rem;">
                    <td class="" style="" colspan="4"></td>                    
                    <td class="" style="border-bottom:1px solid black;" colspan="96"></td>
                </tr>
                <tr style="height:1rem;  line-height:1rem;">
                    <td class="" style="" colspan="4"></td>                    
                    <td class="" style="border-bottom:1px solid black;" colspan="96"></td>
                </tr> -->
                
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
export default class FormOfficerReport1 extends Vue {

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
            reasonableGrounds: [],
            other: '',            
            videoSurveillance: false                      
        }

        this.formData.reasonableGrounds = form24.reasonableGrounds?form24.reasonableGrounds:[];
        if (this.formData.reasonableGrounds.includes('Other')){
            this.formData.other = form24.reasonableGroundsOther?form24.reasonableGroundsOther:'';
        } else {
            this.formData.other = '';
        }
        this.formData.videoSurveillance = this.formData.reasonableGrounds.includes('Video surveillance');        
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