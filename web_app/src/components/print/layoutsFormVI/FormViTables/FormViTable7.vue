<template>
    <div v-if="dataReady">

        <div class="row outer_table_class" style="font-size:6pt; margin:0.25rem 0 0 0; padding:0rem;">

            <table class="text-left" style="border:2px solid #151515; width:100%; line-height:0.5rem;">
                
                <tr style="height:0.01rem; line-height:0.01rem;">                    
                    <td v-for="inx in Array(100)" :key="inx" class="" style="width:1% !important;" />                                                                                   
                </tr>
<!-- <ROW1> -->
                <tr class="spacer-high" style="color:#FFF; height:0.25rem;  line-height:0.25rem;"><td colspan="100">.</td></tr>
                <tr style="height:0.5rem;  line-height:0.5rem; border-top:0px solid;">
                    <td class="side-name" style="font-size:8pt; transform:rotate(-90deg) translate(-32px,-18px)" colspan="8"><b>IMP LOT</b></td>
                    <td class="" style="" colspan="20" />
                    <td class="" style="" colspan="28">DATE (YYYY/MM/DD)</td>
                    <td class="" style="" colspan="20">IMPOUND LOT</td>
                    <td class="" style="" colspan="24" />                                                                  
                </tr>
                <tr class="spacer-low" style="color:#FFF; height:0.15rem; line-height:0.15rem;"><td colspan="100"></td></tr>
                <tr style="height:1.9rem;  line-height:1rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="4" />
                    <td class="font-size-8" style="font-size:7pt;" colspan="24">The motor vehicle was impounded on</td>                     
                    <td class="answer2" style="border:1px solid #656565;" colspan="15">2020/02/02</td> 
                    <td class="" style="" colspan="1" />
                    <td class="font-size-8" style="font-size:7pt;" colspan="12">, and is stored at</td>
                    <td class="answer2" style="border:1px solid #656565;" colspan="43">IMPOUND LOT # 4556</td>
                    <td class="" style="" colspan="1" />                                                                           
                </tr>
                <tr class="spacer-low" style="color:#FFF; height:0.25rem; line-height:0.25rem;"><td colspan="100">.</td></tr>
                <tr style="height:0.5rem;  line-height:0.5rem; border-top:0px solid;">                    
                    <td class="" style="" colspan="4" />
                    <td class="" style="" colspan="36">STREET ADDRESS</td>
                    <td class="" style="" colspan="30">CITY</td>
                    <td class="" style="" colspan="30" />                                                                  
                </tr>
                <tr class="spacer-low" style="color:#FFF; height:0.15rem; line-height:0.15rem;"><td colspan="100"></td></tr>
                <tr style="height:1.9rem;  line-height:1rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="4" />                    
                    <td class="answer2" style="border:1px solid #656565;" colspan="35">TERMINAL AVE</td> 
                    <td class="" style="" colspan="1" />                    
                    <td class="answer2" style="border:1px solid #656565;" colspan="25">VANCOUVER</td>
                    <td class="" style="" colspan="1" />
                    <td class="font-size-8" style="font-size:7pt;" colspan="13">, British Columbia</td>
                    <td class="answer2" style="border:1px solid #656565;" colspan="20">800-900-1000</td> 
                    <td class="" style="" colspan="1" />                                                                           
                </tr>
                
                
               
                <tr style="color:#FFF; height:0.5rem; line-height:0.25rem;"><td colspan="100">.</td></tr>

            </table>
        </div>
    </div>           
</template>     
<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';


import CheckBox from "../../pdfUtil/CheckBox.vue";
import UnderlineForm from "../../pdfUtil/UnderlineForm.vue"

@Component({
    components:{       
        CheckBox,
        UnderlineForm          
    }
})
export default class FormViTable7 extends Vue {

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
    color: rgb(3, 19, 165) !important;
    font-size: 10pt !important;
    font-weight: 600 !important;
    padding-left:0.25rem;
}



.print-none{
    display: none !important;
}

.font-size-8{
    font-size: 10pt !important;
}

.side-name{
    transform:rotate(-90deg) translate(-33px,-17px) !important;
}

.padding-left-0-25{
    padding-left:0.28rem ;
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