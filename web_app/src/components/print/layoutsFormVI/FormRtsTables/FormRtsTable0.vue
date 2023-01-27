<template>
    <div v-if="dataReady">       
        
        <div class="row outer_table_class" style="font-size:8pt; margin:0rem 0 0 0;">
            <table class="border-0 border-dark" style="width:100%; line-height:0.75rem;">                
                <tr>
                    <td style="width:25%;" >
                        <div style="width:11rem;">
                            <img :src="src"/>
                        </div>
                    </td> 
                    <td  style="width:15%;" />
                    <td  class="" style="width:20%;" >
                        <table>
                            <tr>
                                <td>                        
                                    <div class="mt-3" style="color: rgb(3, 19, 165);font-family: barcode; font-size:30pt;" >{{serialNo}}</div>
                                </td>
                            </tr>
                            <tr style="width:100%;" >
                                <td >
                                    <div class="text-center mt-1" style="font-size:14pt;" ><b>VI NO.</b> <span style="color: rgb(3, 19, 165);">22-1000710</span></div>
                                </td>
                            </tr>
                        </table>
                    </td>
                    <td  style="width:15%;" />                    
                    <td  style="width:25%; line-height:0.65rem;">
                        <table class="float-right">
                            <tr> 
                                <th class="text-right">REPORT TO SUPERINTENDENT</th>                                                           
                            </tr>
                            <tr> 
                                <td class="text-right">Vehicle Impoundment</td>
                            </tr>
                            <tr> 
                                <td class="text-right">Section 254 MVA</td>
                            </tr>
                            <tr> 
                                <td />
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
            <table class="border-0 border-dark" style="width:100%; margin-top:0.5rem; line-height:0.75rem;">
                <tr>
                    <td class="text-left">
                        <b>DATE OF REPORT</b> (YYYY/MM/DD):
                        <underline-form 
                            class="text-center"
                            hint="" 
                            text="2020/02/02" 
                            textSize="10pt" 
                            textWeight="600" 
                            textwidth="6rem" 
                            textColor="#2134AB" />
                    </td>
                </tr>
            </table>
        </div>
    </div>           
</template>     
<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import {srcFile} from '@/images/logo'

import CheckBox from "../../pdfUtil/CheckBox.vue";
import UnderlineForm from "../../pdfUtil/UnderlineForm.vue"

@Component({
    components:{       
        CheckBox,
        UnderlineForm           
    }
})
export default class FormRtsTable0 extends Vue {

    // @Prop({required:true})
    // result!: form20DataInfoType;

    dataReady = false;
    src =""
    serialNo="*1000710*"

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

.outer_table_class{
    margin: 1rem 0 0 0 !important;
   
}

</style>