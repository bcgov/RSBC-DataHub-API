<template>
    <div v-if="dataReady">

        <div class="row margin-top-n0-25" style="margin:0.65rem 0 0 0; line-height:0.25rem;">
            <div class="text-center" style="font-size:9pt; width:100%;"><b>RETURN OF DRIVER'S LICENCE</b></div>            
        </div>

        <div class="row margin-top-n0-40" style="font-size:5.9pt; margin:0.45rem 0 0 0;">

            <table class="border border-dark text-left" style="width:100%; line-height:0.5rem;">

                <tr style="height:0.01rem; line-height:0.01rem; border-right:1px solid #151515;">                                                         
                    <td v-for="inx in Array(100)" :key="inx" class="border-0 border-dark" style="width:1%;" />                                                                                   
                </tr>              
<!-- <ROW1> -->
                <tr style="height:0.25rem; line-height:0.75rem;"> 
                    <td class="" style="" colspan="1" />                   
                    <td class="" style="border-right:1px solid;" colspan="49">DATE AND TIME OF RETURN</td>
                    <td class="" style="" colspan="1" rowspan="2" />
                    <td class="" style="" colspan="4" rowspan="2" >
                        <check-box
                            shiftBox="18px,-1px"
                            shiftmark="-1px,-1px"                                   
                            checkColor="#2134AB"
                            boxSize="1.5em" 
                            :check="formData.returnDlInPerson"
                            checkFontSize="12pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="20" rowspan="2" >PERSONALLY</td>
                    <td class="" style="" colspan="1" rowspan="2" />
                    <td class="" style="" colspan="4" rowspan="2" >
                        <check-box
                            shiftBox="18px,-1px"
                            shiftmark="-1px,-1px"                                   
                            checkColor="#2134AB"
                            boxSize="1.5em" 
                            :check="formData.returnDlByMail"
                            checkFontSize="12pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="20" rowspan="2" >MAIL</td>                    
                </tr>

                <tr style="height:0.95rem; line-height:0.65rem;">
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="border-right:1px solid #151515;" colspan="49">{{formData.returnDlDateTime}}</td>
                </tr>

<!-- <ROW2> -->
                <tr style="height:0.25rem; line-height:0.75rem; border-top:1px solid;">
                    <td class="" style="" colspan="1" />
                    <td class="" style="border-right:1px solid;" colspan="49">RETURNING OFFICER</td>
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="49">RECEIPT OF LICENCE ACKNOWLEDGED</td>
                </tr>
                <tr style="height:0.95rem; line-height:0.65rem;">
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="border-right:1px solid #151515;" colspan="49">{{formData.returnDlOfficer}}</td>
                    <td class="" style="" colspan="1" />                    
                    <td class="answer" style="" colspan="49">{{formData.returnDlAcknowledge}}</td>                    
                </tr>

            </table>
        </div>
    </div>           
</template>     
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { namespace } from "vuex-class";

import "@/store/modules/forms/mv2906";
const mv2906State = namespace("MV2906");

import CheckBox from "../../pdfUtil/CheckBox.vue";
import { twelveHourFormJsonInfoType } from '@/types/Forms/MV2906';

@Component({
    components:{       
        CheckBox           
    }
})
export default class Form12hTable5 extends Vue {

    @mv2906State.State
    public mv2906Info: twelveHourFormJsonInfoType;   

    dataReady = false;
    formData;

    mounted(){
        this.dataReady = false;
        this.extractInfo();
        this.dataReady = true;
    }

    public extractInfo(){

        this.formData = {
            returnDlInPerson: false,
            returnDlByMail: false,
            returnDlDateTime:'',
            returnDlOfficer: '',
            returnDlAcknowledge: ''            
        }
       
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

.margin-top-n0-40{
    margin-top: -0.4rem !important;
}

.margin-top-n0-25{
    margin-top: -0.25rem !important;
}

</style>