<template>
    <div v-if="dataReady">

        <div class="row outer_table_class" style="font-size:6pt; margin:0.25rem 0 0 0; padding:0rem;">

            <table class="text-left" style="border:2px solid #151515; width:100%; line-height:0.5rem;">
                
                <tr style="height:0.01rem; line-height:0.01rem;">                    
                    <td v-for="inx in Array(100)" :key="inx" class="border-0" style="width:1% !important;" />                                                                                   
                </tr>
<!-- <ROW1> -->                
                <tr style="height:0.5rem;  line-height:0.75rem; border-top:0px solid;">
                    <td class="" style="" colspan="4" />
                    <td class="" style="border-left:1px solid #656565;" colspan="1" />
                    <td class="" style="" colspan="35">PEACE OFFICER’S NAME (PRINT)</td> 
                    <td class="" style="border-left:1px solid #656565;" colspan="1" />
                    <td class="" style="" colspan="29">PEACE OFFICER’S SIGNATURE</td>
                    <td class="" style="border-left:1px solid #656565;" colspan="1" />
                    <td class="" style="" colspan="29">PIN/BADGE NUMBER</td>
                                                         
                </tr>                
                <tr style="height:1.5rem;  line-height:1rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="4" />
                    <td class="" style="border-bottom:1px solid #656565;border-left:1px solid #656565;" colspan="1" />
                    <td class="answer2" style="border-bottom:1px solid #656565;" colspan="35">ADMIN</td> 
                    <td class="" style="border-bottom:1px solid #656565;border-left:1px solid #656565;" colspan="1" />
                    <td class="answer2" style="border-bottom:1px solid #656565;" colspan="29">SIGN</td>
                    <td class="" style="border-bottom:1px solid #656565;border-left:1px solid #656565;" colspan="1" />
                    <td class="answer2" style="border-bottom:1px solid #656565;" colspan="29">0000</td>                                                                               
                </tr>
<!-- <ROW2> -->                
                <tr style="height:0.5rem;  line-height:0.65rem; border-top:0px solid;">
                    <td class="" style="" colspan="4" />
                    <td class="" style="border-left:1px solid #656565;" colspan="1" />
                    <td class="" style="" colspan="60">ENFORCEMENT AGENCY NAME (PRINT)</td> 
                    <td class="" style="border-left:1px solid #656565;" colspan="1" />
                    <td class="" style="" colspan="34">AGENCY FILE NUMBER</td>
                </tr>                
                <tr style="height:1.5rem;  line-height:1rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="4" />
                    <td class="" style="border-bottom:1px solid #656565;border-left:1px solid #656565;" colspan="1" />
                    <td class="answer2" style="border-bottom:1px solid #656565;" colspan="60">ROAD SAFTY </td> 
                    <td class="" style="border-bottom:1px solid #656565;border-left:1px solid #656565;" colspan="1" />
                    <td class="answer2" style="border-bottom:1px solid #656565;" colspan="34">879653</td>                                                                              
                </tr>               

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
export default class FormViTable8 extends Vue {

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


.side-name{
    transform:rotate(-90deg) translate(-42px,-5px) !important;
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