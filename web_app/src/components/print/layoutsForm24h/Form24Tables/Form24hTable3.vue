<template>
    <div v-if="dataReady">

        <div class="row officer_class" style="font-size:6pt; margin:0.25rem 0 0 0;">

            <table class="border border-dark text-left" style="width:100%; line-height:0.5rem;">

                <tr style="height:0.01rem; line-height:0.01rem; border-right:1px solid #151515;">
                    <td class="" style="width:1%;" colspan="1" />                 
                    <td v-for="inx in Array(100)" :key="inx" class="border-0 border-dark" style="width:1%;" />                                                                                   
                </tr>              
<!-- <ROW1> -->
                <tr style="height:0.25rem; line-height:0.5rem;">
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="98">LOCATION OF PEACE OFFICER'S REQUEST FOR SURRENDER OF DRIVER'S LICENCE</td>
                    <td class="" style="" colspan="2" />
                </tr>
                <tr style="height:0.85rem; line-height:0.65rem;">
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="98">{{formData.offenceAddress}}</td>
                    <td class="" style="" colspan="2" />
                </tr>
<!-- <ROW2> -->
                <tr style="height:0.25rem; line-height:0.5rem; border-top:1px solid;">
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="70">SIGNATURE OF PEACE OFFICER SERVING PROHIBITION NOTICE</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="29">BADGE NUMBER</td>
                </tr>
                <tr style="height:0.85rem; line-height:0.65rem;">
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="70">{{formData.officerName}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="29">{{formData.badgeNumber}}</td>
                </tr>
<!-- <ROW2> -->
                <tr style="height:0.25rem; line-height:0.5rem; border-top:1px solid;">
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="60">POLICE AGANCY OR RCMP UNIT</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="39">AGANCY FILE NUMBER</td>
                </tr>
                <tr style="height:0.85rem; line-height:0.65rem;">
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="60">{{formData.agencyName}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="39">{{formData.agencyFileNumber}}</td>
                </tr>

            </table>
        </div>
    </div>           
</template>     
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { namespace } from "vuex-class";

import "@/store/modules/forms/mv2634";
const mv2634State = namespace("MV2634");

import CheckBox from "../../pdfUtil/CheckBox.vue";
import { twentyFourHourFormJsonInfoType } from '@/types/Forms/MV2634';


@Component({
    components:{       
        CheckBox           
    }
})
export default class Form24hTable3 extends Vue {

    @mv2634State.State
    public mv2634Info: twentyFourHourFormJsonInfoType;   

    dataReady = false;

    formData;

    mounted(){
        this.dataReady = false;
        this.extractInfo();
        this.dataReady = true;
    }

    public extractInfo(){

        const form24 = this.mv2634Info.data

        this.formData = {
            offenceAddress: '',
            officerName:'',
            badgeNumber: '',
            agencyName: '',
            agencyFileNumber: ''            
        }

        const lineAddress = form24.offenceAddress?form24.offenceAddress.toUpperCase()+', ':'';
        const city = form24.offenceCity?.objectDsc?form24.offenceCity.objectDsc.toUpperCase():'';

        this.formData.offenceAddress = lineAddress + city;
        this.formData.officerName = form24.officer_name?form24.officer_name.toUpperCase():'';
        this.formData.badgeNumber = form24.badge_number?form24.badge_number:'';
        this.formData.agencyName = form24.agency?form24.agency.toUpperCase():'';
        this.formData.agencyFileNumber = form24.agencyFileNumber?form24.agencyFileNumber.toUpperCase():'';
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

.officer_class{
    margin: 0 0 !important;
}

</style>