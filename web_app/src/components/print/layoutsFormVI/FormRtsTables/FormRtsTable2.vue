<template>
    <div v-if="dataReady">

        <div class="row outer_table_class" style="font-size:6pt; margin:0.25rem 0 0 0; padding:0rem;">

            <table class="text-left" style="border:2px solid #151515; width:100%; line-height:0.5rem;">
                
                <tr style="height:0.01rem; line-height:0.01rem;">                    
                    <td v-for="inx in Array(100)" :key="inx" class="border-0" style="width:1% !important;" />                                                                                   
                </tr>

<!-- <Side Title> -->
                <tr class="spacer-high" style="color:#FFF; height:0.15rem;  line-height:0.15rem;"><td colspan="100">.</td></tr>
                <tr style="height:0.5rem;  line-height:1.0rem; border-top:0px solid;">
                    <th class="side-name" style="font-size:8pt; transform:rotate(-90deg) translate(-65px,-5px);" colspan="6">LINKAGE</th>                                                                                                                    
                    <th class="" style="font-size:8pt; transform:translate(-9px,0px);" colspan="89">The officer determined the following: (relationship between the driver, owner, and the vehicle)</th>
                    <td class="" style="" colspan="5" />
                </tr>

<!-- <ROW-1> -->
                <tr style="color:#FFF; height:0.15rem; line-height:0.15rem;"><td colspan="100">.</td></tr>
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
                    <td class="font-size-8" style="" colspan="16">Location of vehicle’s key(s).</td>  
                    <td class="answer2" style="border:1px solid #656565;" colspan="48">WITH THE DRIVER</td>
                    <td class="" style="" colspan="1"/>
                    <th class="font-size-8" style="" colspan="29">(or explain in incident details – refer to row 23/24)</th>                    
                </tr>               
                <tr style="color:#FFF; height:0.1rem; line-height:0.1rem;"><td colspan="100">.</td></tr> 

<!-- <ROW-2> -->
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
                    <td class="font-size-7" style="" colspan="94">The driver is a principal operator <b>(PDN)</b>.</td>
                </tr>
                <tr style="color:#FFF; height:0.1rem; line-height:0.1rem;"><td colspan="100">.</td></tr>

<!-- <ROW-3> -->
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
                    <td class="font-size-7" style="" colspan="94">The owner was in the vehicle.</td>
                </tr>
                <tr style="color:#FFF; height:0.1rem; line-height:0.1rem;"><td colspan="100">.</td></tr>

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
                    <td class="font-size-7" style="" colspan="94">The owner was aware the driver was in possession of the vehicle <b>(explain in incident details – refer to row 23/24).</b></td>
                </tr>
                <tr style="color:#FFF; height:0.1rem; line-height:0.1rem;"><td colspan="100">.</td></tr>

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
                    <td class="font-size-7" style="" colspan="94">Vehicle subject to a transfer notice <b>(explain in incident details – refer to row 23/24).</b></td>
                </tr>
                <tr style="color:#FFF; height:0.1rem; line-height:0.1rem;"><td colspan="100">.</td></tr>

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
                    <td class="font-size-7" style="" colspan="94">Other <b>(explain in incident details – refer to row 23/24).</b></td>
                </tr>
                <tr style="color:#FFF; height:0.25rem; line-height:0.25rem;"><td colspan="100">.</td></tr>

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
export default class FormRtsTable2 extends Vue {

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

.font-size-8{
    font-size: 8pt !important;
}

.font-size-7{
    font-size: 7pt !important;
}
.font-size-7-2{
    font-size: 7.2pt !important;
}

.side-name{
    transform:rotate(-90deg) translate(-70px,-5px) !important;
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