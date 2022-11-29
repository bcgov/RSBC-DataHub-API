<template>
    <div v-if="dataReady">

        <div class="row outer_table_class" style="font-size:6pt; margin:0.25rem 0 0 0; padding:0rem;">

            <table class="text-left" style="border:2px solid #151515; width:100%; line-height:0.5rem;">
                
                <tr style="height:0.01rem; line-height:0.01rem;">                    
                    <td v-for="inx in Array(100)" :key="inx" class="border-0" style="width:1% !important;" />                                                                                   
                </tr>
<!-- <Side Title> -->
                <tr class="spacer-high" style="color:#FFF; height:0.15rem;  line-height:0.15rem;"><td colspan="100">.</td></tr>
                <tr style="height:0.05rem;  line-height:0.05rem; border-top:0px solid;">
                    <td class="side-name" style="font-size:8pt; transform:rotate(-90deg) translate(-20px,-165px);" colspan="50"><b>CHECK ALL APPLICABLE REASONS</b></td>                                                                                                
                    <td colspan="50" />
                </tr>

<!-- <ROW-1> -->
                <tr style="height:0.5rem;  line-height:0.5rem; border-top:0px solid;">
                    <td class="" style="" colspan="4" />
                    <td class="font-size-7" style="" colspan="67"><b>3, 7, OR 30 DAY IMPOUNDMENT</b> IN ACCORDANCE WITH SECTION 215.46 AND 253 OF THE <i>MOTOR VEHICLE ACT:</i></td>
                    <td class="font-size-7-2" style="" colspan="29">(Immediate Roadside Prohibition IMPOUNDMENT)</td>                                                                  
                </tr> 
                <tr style="color:#FFF; height:0.1rem; line-height:0.1rem;"><td colspan="100">.</td></tr>
<!-- <ROW-2>  -->
                <tr style="height:1.5rem;  line-height:1rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="4" />
                    <td class="" style="" colspan="2">
                        <check-box
                            shiftBox="16px,-3px"
                            shiftmark="-1px,-4px"                                   
                            checkColor="#2134AB"
                            boxSize="1.5em" 
                            :check="true"
                            checkFontSize="15pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="18">3-DAY IMPOUNDMENT</td>
                    <td class="" style="" colspan="2">
                        <check-box
                            shiftBox="16px,-3px"
                            shiftmark="-1px,-4px"                                   
                            checkColor="#2134AB"
                            boxSize="1.5em" 
                            :check="true"
                            checkFontSize="15pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="18">7-DAY IMPOUNDMENT</td>
                    <td class="" style="" colspan="2">
                        <check-box
                            shiftBox="16px,-3px"
                            shiftmark="-1px,-4px"                                   
                            checkColor="#2134AB"
                            boxSize="1.5em" 
                            :check="true"
                            checkFontSize="15pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="18">30-DAY IMPOUNDMENT</td>                    
                    <th class="font-size-7" style="" colspan="6">IRP No.</th>
                    <td class="answer2" style="border:1px solid #656565;" colspan="29">1000523</td>
                    <td class="" style="" colspan="1" />                                                           
                </tr>
                
                <tr style="height:0.35rem; line-height:0.35rem;">
                    <td colspan="4"/>
                    <td colspan="95" style="border-bottom:1px solid #252525;"/>
                    <td colspan="1"/>
                </tr>
                <tr style="color:#FFF; height:0.15rem; line-height:0.15rem;"><td colspan="100">.</td></tr>

<!-- <ROW-3> -->
                <tr style="height:0.5rem;  line-height:0.5rem; border-top:0px solid;">
                    <td class="" style="" colspan="4" />
                    <td class="font-size-7" style="" colspan="70"><b>7 DAY IMPOUNDMENT FOR THE FOLLOWING REASON(S)</b> – SECTION 251 AND 253 OF THE <i>MOTOR VEHICLE ACT:</i></td>
                    <td class="font-size-7" style="" colspan="26">(Driving Behaviour Related IMPOUNDMENT)</td>                                                                  
                </tr> 
                <tr style="color:#FFF; height:0.5rem; line-height:0.5rem;"><td colspan="100">.</td></tr>

<!-- <ROW-4> -->
                <tr style="height:1rem;  line-height:1rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="4" />
                    <td class="" style="" colspan="2">
                        <check-box
                            shiftBox="16px,-3px"
                            shiftmark="-1px,-4px"                                   
                            checkColor="#2134AB"
                            boxSize="1.5em" 
                            :check="true"
                            checkFontSize="15pt"
                            text="" />
                    </td>
                    <td class="font-size-7" style="" colspan="94"><b>EXCESSIVE SPEED</b> - Committing an offence under section 148 of the <i>Motor Vehicle Act.</i></td>                                                                                                  
                </tr>
<!-- <ROW-5> -->
                <tr style="height:1rem;  line-height:1rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="4" />
                    <td class="" style="" colspan="2">
                        <check-box
                            shiftBox="16px,-3px"
                            shiftmark="-1px,-4px"                                   
                            checkColor="#2134AB"
                            boxSize="1.5em" 
                            :check="true"
                            checkFontSize="15pt"
                            text="" />
                    </td>
                    <td class="font-size-7" style="" colspan="94"><b>PROHIBITED</b> - Driving while prohibited under the <i>Motor Vehicle Act, Criminal Code, Youth Justice Act or Youth Criminal Justice Act</i> (Canada).</td>                                                                                                  
                </tr>
<!-- <ROW-6> -->
                <tr style="height:1rem;  line-height:1rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="4" />
                    <td class="" style="" colspan="2">
                        <check-box
                            shiftBox="16px,-3px"
                            shiftmark="-1px,-4px"                                   
                            checkColor="#2134AB"
                            boxSize="1.5em" 
                            :check="true"
                            checkFontSize="15pt"
                            text="" />
                    </td>
                    <td class="font-size-7" style="" colspan="94"><b>SUSPENDED</b> - Driving while suspended under section 89 or section 232 of the <i>Motor Vehicle Act.</i></td>                                                                                                  
                </tr>           
<!-- <ROW-7> -->
                <tr style="height:1rem;  line-height:1rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="4" />
                    <td class="" style="" colspan="2">
                        <check-box
                            shiftBox="16px,-3px"
                            shiftmark="-1px,-4px"                                   
                            checkColor="#2134AB"
                            boxSize="1.5em" 
                            :check="true"
                            checkFontSize="15pt"
                            text="" />
                    </td>
                    <td class="font-size-7" style="" colspan="94"><b>STREET RACING</b> - Driving or operating a motor vehicle in a race as defined in the <i>Motor Vehicle Act</i> and the officer intends to charge with an offence.</td>                                                                                                  
                </tr>
<!-- <ROW-8> -->
                <tr style="height:1rem;  line-height:1rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="4" />
                    <td class="" style="" colspan="2">
                        <check-box
                            shiftBox="16px,-3px"
                            shiftmark="-1px,-4px"                                   
                            checkColor="#2134AB"
                            boxSize="1.5em" 
                            :check="true"
                            checkFontSize="15pt"
                            text="" />
                    </td>
                    <td class="font-size-7" style="" colspan="94"><b>STUNT DRIVING</b> - Driving or operating a motor vehicle in a stunt as defined in the <i>Motor Vehicle Act</i> and the officer intends to charge with an offence.</td>                                                                                                  
                </tr>
<!-- <ROW-9> -->
                <tr style="height:1rem;  line-height:1rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="4" />
                    <td class="" style="" colspan="2">
                        <check-box
                            shiftBox="16px,-3px"
                            shiftmark="-1px,-4px"                                   
                            checkColor="#2134AB"
                            boxSize="1.5em" 
                            :check="true"
                            checkFontSize="15pt"
                            text="" />
                    </td>
                    <td class="font-size-7" style="" colspan="94"><b>MOTORCYCLE (seating)</b> - Committing an offence under section 194 (1) or (2) of the <i>Motor Vehicle Act.</i></td>                                                                                                  
                </tr> 
<!-- <ROW-10> -->
                <tr style="height:1rem;  line-height:1rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="4" />
                    <td class="" style="" colspan="2">
                        <check-box
                            shiftBox="16px,-3px"
                            shiftmark="-1px,-4px"                                   
                            checkColor="#2134AB"
                            boxSize="1.5em" 
                            :check="true"
                            checkFontSize="15pt"
                            text="" />
                    </td>
                    <td class="font-size-7" style="" colspan="94"><b>MOTORCYCLE (restrictions)</b> - <span class="font-size-7" style="font-size:5.5pt" >Committing an offence under section 25(15) of the <i>Motor Vehicle Act</i> relating to a restriction or condition of a motorcycle learner or novice driver’s licence.</span></td>                                                                                                  
                </tr>
<!-- <ROW-11> -->
                <tr style="height:1rem;  line-height:1rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="4" />
                    <td class="" style="" colspan="2">
                        <check-box
                            shiftBox="16px,-3px"
                            shiftmark="-1px,-4px"                                   
                            checkColor="#2134AB"
                            boxSize="1.5em" 
                            :check="true"
                            checkFontSize="15pt"
                            text="" />
                    </td>
                    <td class="font-size-7" style="" colspan="94"><b>UNLICENSED (UL)</b> - Driving without a valid driver’s licence and with a notice on the driving record indicating a previous conviction for driving while unlicensed.</td>                                                                                                  
                </tr>

                <!-- <ROW-2>  -->
                <tr style="height:1.5rem;  line-height:1rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="59" />
                    <th class="font-size-7" style="" colspan="11">UL Prohibition No.</th>
                    <td class="answer2" style="border:1px solid #656565;" colspan="29">1000523</td>
                    <td class="" style="" colspan="1" />                                                           
                </tr>
                <tr style="color:#FFF; height:0.35rem; line-height:0.25rem;"><td colspan="100">.</td></tr> 
                
            </table>
        </div>
    </div>           
</template>     
<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';


import CheckBox from "../../pdfUtil/CheckBox.vue";

@Component({
    components:{       
        CheckBox           
    }
})
export default class FormViTable6 extends Vue {

    // @Prop({required:true})
    // result!: form20DataInfoType;

    dataReady = false;


    mounted(){
        this.dataReady = false;
        // this.extractInfo();
        this.dataReady = true;
    }

    // public extractInfo(){

    //     if (this.result.withdrawingLawyerName == 'Other'){
    //         this.lawyerName = this.result.withdrawingLawyerNameOther;
    //     } else {
    //         this.lawyerName = this.result.withdrawingLawyerName;
    //     }

    //     const index = this.result.objectingParties.indexOf('Other')

    //     if (index != -1){

    //         const partiesList = this.result.objectingParties.splice(index, 1);
    //         partiesList.push(this.result.objectingPartiesOther);
    //         this.parties = partiesList.join(', ');

    //     } else {
    //         this.parties = this.result.objectingParties.join(', ');
    //     }     
           
    // }

    
}

</script>

<style scoped>

.answer2 {
    color: rgb(3, 19, 165);
    font-size: 10pt;
    font-weight: 600;
    padding-left:0.25rem;
}

.font-size-6{
    font-size: 6pt !important;
}

.font-size-7{
    font-size: 7pt !important;
}
.font-size-7-2{
    font-size: 7.2pt !important;
}

.side-name{
    transform:rotate(-90deg) translate(10px,-205px) !important;
}
@media print {
    .side-name{
        transform:rotate(-90deg) translate(10px,-205px) !important;
    }
}

.spacer-low{
    line-height:0.05rem !important;
    font-size: 1pt !important;
    height: 0.01rem !important;
}

.spacer-high{
    line-height:0.15rem !important;
    font-size: 1pt !important;
    height: 0.15rem !important;
}

.outer_table_class{
    margin: 0.5rem 0 0 0 !important;
    padding: 0 0.2rem !important;
}

</style>