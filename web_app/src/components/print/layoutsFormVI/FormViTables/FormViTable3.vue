<template>
    <div v-if="dataReady">

        <div class="row outer_table_class" style="font-size:6pt; margin:0.25rem 0 0 0; padding:0rem;">

            <table class="text-left" style="border:2px solid #151515; width:100%; line-height:0.5rem;">
                
                <tr style="height:0.01rem; line-height:0.01rem;">                    
                    <td v-for="inx in Array(100)" :key="inx" class="border-0" style="width:1% !important;" />                                                                                   
                </tr>
<!-- <ROW1> -->
                <tr class="spacer-high" style="color:#FFF; height:0.25rem;  line-height:0.25rem;"><td colspan="100">.</td></tr>
                <tr style="height:0.5rem;  line-height:0.5rem; border-top:0px solid;">
                    <td class="side-name" style="font-size:8pt; transform:rotate(-90deg) translate(-42px,-5px)" colspan="5"><b>OWNER</b></td>                    
                    <td class="" style="transform:translate(-8px,0px)" colspan="50">ADDRESS (STREET)</td>                    
                    <td class="" style="" colspan="22">CITY/TOWN</td>
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="9">PROV/STATE</td>
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="11">POSTAL/ZIP CODE</td>
                    <td class="" style="" colspan="1" />                                                          
                </tr>
                <tr class="spacer-low" style="color:#FFF; height:0.15rem; line-height:0.15rem;"><td colspan="100"></td></tr>
                <tr style="height:1.9rem;  line-height:1rem; border-top:0px solid;">                  
                    <td class="" style="" colspan="4" />
                    <td class="answer2" style="border:1px solid #656565;" colspan="73">
                        <div class="row m-0 p-0">
                            <div style="width:68%" >800 HORNBY ST.</div>
                            <div style="width:32%" >VANCOUVER</div>
                        </div>
                    </td> 
                    <td class="" style="" colspan="1" />
                    <td class="answer2" style="border:1px solid #656565;" colspan="9">BC</td>
                    <td class="" style="" colspan="1" />
                    <td class="answer2" style="border:1px solid #656565;" colspan="11">V1R 1R1</td>
                    <td class="" style="" colspan="1" />                                                           
                </tr>
                <tr style="color:#FFF; height:0.15rem; line-height:0.25rem;"><td colspan="100">.</td></tr>
                <tr style="height:0.5rem;  line-height:0.5rem; border-top:0px solid;">                    
                    <td class="" style="" colspan="4" />
                    <td class="" style="" colspan="30">CONTACT PHONE</td> 
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="64">EMAIL ADDRESS</td>
                    <td class="" style="" colspan="1" />                                                                             
                </tr>
                <tr class="spacer-low" style="color:#FFF; height:0.15rem; line-height:0.15rem;"><td colspan="100"></td></tr>
                <tr style="height:1.9rem;  line-height:1rem; border-top:0px solid;">                    
                    <td class="" style="" colspan="4" />
                    <td class="answer2" style="border:1px solid #656565;" colspan="30">800-700-6000</td>
                    <td class="" style="" colspan="1" />
                    <td class="answer2" style="border:1px solid #656565;" colspan="64">A@B.COM</td>
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

@Component({
    components:{       
        CheckBox           
    }
})
export default class FormViTable3 extends Vue {

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
    transform:rotate(-90deg) translate(-40px,-5px) !important;
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