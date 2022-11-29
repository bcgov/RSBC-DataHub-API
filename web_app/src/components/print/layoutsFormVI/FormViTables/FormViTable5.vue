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
                    <td class="" style="" colspan="49" />
                    <td class="" style="" colspan="20">DATE (YYYY/MM/DD)</td>
                    <td class="" style="" colspan="31" />                                                                  
                </tr>
                <tr class="spacer-low" style="color:#FFF; height:0.15rem; line-height:0.15rem;"><td colspan="100"></td></tr>
                <tr style="height:1.9rem;  line-height:1rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="4" />
                    <td class="font-size-8" style="font-size:7pt;" colspan="45">The undersigned peace officer has reasonable grounds to believe that on</td>                     
                    <td class="answer2" style="border:1px solid #656565;" colspan="20">2020/02/02</td> 
                    <td class="" style="" colspan="1" />
                    <td class="font-size-8" style="font-size:7pt;" colspan="1">,</td>
                    <td class="" style="" colspan="29" />                                                                           
                </tr>
                <tr style="height:1.9rem; line-height:1rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="4" />
                    <td class="font-size-8" style="font-size:7pt;" colspan="1">at</td> 
                    <td class="" style="" colspan="1" />
                    <td class="answer2" style="border:1px solid #656565;" colspan="9">1000</td> 
                    <td class="" style="" colspan="1" />
                    <td class="font-size-8" style="font-size:7pt;" colspan="7">hours, on</td>
                    <td class="" style="" colspan="29">
                        <underline-form 
                            class="pdf-none"
                            hint="STREET/HIGHWAY" 
                            text="Horby" 
                            textSize="10pt" 
                            textWeight="600" 
                            textwidth="15rem" 
                            textColor="#2134AB"  />
                        <underline-form 
                            class="print-none"
                            hint="STREET/HIGHWAY" 
                            text="Horby" 
                            textSize="10pt" 
                            textWeight="600" 
                            textwidth="12.5rem" 
                            textColor="#2134AB"  />    
                    </td>                                       
                    <td class="font-size-8" style="font-size:7pt;" colspan="7">at or near</td>
                    <td class="" style="border-top:1px solid white;" colspan="27">
                        <underline-form
                            class="pdf-none" 
                            hint="CITY/TOWN" 
                            text="PRINCE GEORGE" 
                            textSize="10pt" 
                            textWeight="600" 
                            textwidth="13rem" 
                            textColor="#2134AB" />
                        <underline-form 
                            class="print-none"
                            hint="CITY/TOWN" 
                            text="PRINCE GEORGE" 
                            textSize="10pt" 
                            textWeight="600" 
                            textwidth="11.5rem" 
                            textColor="#2134AB" />
                    </td>                   
                    <td class="font-size-8" style="font-size:7pt; border-top:1px solid white;" colspan="14">British Columbia,</td>                                                                           
                </tr>
                <tr style="height:1.2rem;  line-height:1.3rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="4" />
                    <td class="font-size-8" style="font-size:7pt;" colspan="95">the driver was operating a motor vehicle and for one or more of the reasons specified below the vehicle is impounded for the period set out below:</td> 
                    <td class="" style="" colspan="1" />
                </tr>
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
export default class FormViTable5 extends Vue {

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
    transform:rotate(-90deg) translate(-42px,-8px) !important;
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