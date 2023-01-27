<template>
    <div v-if="dataReady">       
        
        <div class="row" style="font-size:8pt; margin:0rem 0 0 0;">
            <table class="border-0 border-dark" style="width:100%; line-height:0.75rem;">                
                <tr style="height:0.01rem; line-height:0.01rem;">                    
                    <td v-for="inx in Array(100)" :key="inx" class="" style="width:1% !important;" />                                                                                   
                </tr>
                
                <tr style="height:0.15rem;  line-height:0.15rem; border-top:0px solid;">
                    <th class="answer2 text-center" colspan="85">
                       
                    </th>   
                    <td colspan="15" rowspan="2">                        
                        <div class="mt-3" style="font-family: barcode; font-size:27pt;" >{{serialNo}}</div>
                    </td>                           
                </tr>
                <tr style="height:0.5rem;  line-height:0.5rem; border-top:0px solid;">
                    <th class="answer2 text-center" colspan="85"> {{copyType}} </th>
                </tr>
                <tr style="height:0.5rem;  line-height:0.5rem; border-top:0px solid;">
                    <th class="text-left" colspan="90" /> 
                    <th class="text-left" style="font-size:5pt;" colspan="10">MV2722 (2015/02)</th>
                </tr>
            </table>
        </div>
    </div>           
</template>     
<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import {srcFile} from '@/images/logo'

import CheckBox from "../../pdfUtil/CheckBox.vue";

@Component({
    components:{       
        CheckBox           
    }
})
export default class FormRtsTable6 extends Vue {

    @Prop({required:true})
    copyType!: string;

    dataReady = false;
    src =""
    serialNo="*2721*"

    mounted(){
        this.dataReady = false; 
        this.src = srcFile;
        // this.extractInfo();
        this.dataReady = true;
    }

    public p(){
        const s = new XMLSerializer().serializeToString(document.getElementById("my-svg"))
        console.log(s)
        const decoded = unescape(encodeURIComponent(s));
        const base64 = btoa(decoded);
        const imgSource = `data:image/svg+xml;base64,${base64}`;
        console.log(imgSource)
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

.font-barcode {
    font-family: "barcode",serif;
    font-weight: normal;
    font-size: 2em;
    min-width: 100%;
    margin-top:0.2rem;
}

.answer {
    color: rgb(3, 19, 165);
    font-size: 7pt;
    font-weight: 600;
}

.answer2 {
    color: rgb(3, 19, 165) !important;
    font-size: 10pt !important;
    font-weight: 600 !important;
    padding-left:0.25rem;
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