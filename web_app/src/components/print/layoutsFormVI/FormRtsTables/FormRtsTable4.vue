<template>
    <div v-if="dataReady">

        <div class="row outer_table_class" style="font-size:6pt; margin:0.25rem 0 0 0; padding:0rem;">

            <table class="text-left" style="border:2px solid #151515; width:100%; line-height:0.5rem;">
                
                <tr style="height:0.01rem; line-height:0.01rem;">                    
                    <td v-for="inx in Array(100)" :key="inx" class="border-0" style="width:1% !important;" />                                                                                   
                </tr>

<!-- <ROW-1> -->
                <tr style="color:#FFF; height:0.35rem; line-height:0.35rem;"><td colspan="100">.</td></tr>
                <tr style="height:1.5rem;  line-height:1rem; border:0px solid;">
                    <td class="" style="" colspan="4" />                  
                    <td class="" style="border-left:1px solid #151515;border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="1" />
                    <td class="" style="border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="2">
                        <check-box
                            shiftBox="16px,-3px"
                            shiftmark="-1px,-4px"                                   
                            checkColor="#2134AB"
                            boxSize="1.5em" 
                            :check="true"
                            checkFontSize="15pt"
                            text="" />
                    </td> 
                    <td class="font-size-8" style="border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="25"> Incident Details explained below</td> 
                     <td class="" style="border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="2">
                        <check-box
                            shiftBox="16px,-3px"
                            shiftmark="-1px,-4px"                                   
                            checkColor="#2134AB"
                            boxSize="1.5em" 
                            :check="true"
                            checkFontSize="15pt"
                            text="" />
                    </td> 
                    <td class="font-size-8" style="border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="65"> Incident Details attached</td>               
                    <td class="" style="border-left:1px solid #151515;" colspan="1"/>
                    
                </tr>               
                 
<!-- <ROW-2> -->
                <tr style="height:1.5rem;  line-height:1rem; border:0px solid;">
                    <td class="" style="" colspan="4" />                  
                    <td class="" style="border-left:1px solid #151515;border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="1" />
                    <th class="font-size-8" style="border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="10">
                        Incident Details:
                    </th>
                    <td class="answer2" style="border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="84">
                        
                    </td>
                    <td class="" style="border-left:1px solid #151515;" colspan="1"/>
                </tr>
<!-- <ROW-3> -->
                <tr style="height:1.5rem;  line-height:1rem; border:0px solid;">
                    <td class="" style="" colspan="4" />                  
                    <td class="" style="border-left:1px solid #151515;border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="1" />
                    <td class="answer2" style="border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="94">
                    </td>
                    <td class="" style="border-left:1px solid #151515;" colspan="1"/>
                </tr>
<!-- <ROW-4> -->
                <tr style="height:1.5rem;  line-height:1rem; border:0px solid;">
                    <td class="" style="" colspan="4" />                  
                    <td class="" style="border-left:1px solid #151515;border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="1" />
                    <td class="answer2" style="border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="94">
                    </td>
                    <td class="" style="border-left:1px solid #151515;" colspan="1"/>
                </tr>
<!-- <ROW-5> -->
                <tr style="height:1.5rem;  line-height:1rem; border:0px solid;">
                    <td class="" style="" colspan="4" />                  
                    <td class="" style="border-left:1px solid #151515;border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="1" />
                    <td class="answer2" style="border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="94">
                    </td>
                    <td class="" style="border-left:1px solid #151515;" colspan="1"/>
                </tr>
<!-- <ROW-6> -->
                <tr style="height:1.5rem;  line-height:1rem; border:0px solid;">
                    <td class="" style="" colspan="4" />                  
                    <td class="" style="border-left:1px solid #151515;border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="1" />
                    <td class="answer2" style="border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="94">
                    </td>
                    <td class="" style="border-left:1px solid #151515;" colspan="1"/>
                </tr>
<!-- <ROW-7> -->
                <tr style="height:1.5rem;  line-height:1rem; border:0px solid;">
                    <td class="" style="" colspan="4" />                  
                    <td class="" style="border-left:1px solid #151515;border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="1" />
                    <td class="answer2" style="border-top:1px solid #151515;border-bottom:1px solid #151515;" colspan="94">
                    </td>
                    <td class="" style="border-left:1px solid #151515;" colspan="1"/>
                </tr>                

                <tr style="color:#FFF; height:0.35rem; line-height:0.35rem;"><td colspan="100">.</td></tr>

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
export default class FormRtsTable4 extends Vue {

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
    transform:rotate(-90deg) translate(20px,-202px) !important;
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