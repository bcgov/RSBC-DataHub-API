<template>
    <div v-if="dataReady">

        <div class="row margin-top-n0-40" style="font-size:6pt; margin:0.25rem 0 0 0;">

            <table class="border border-dark text-left" style="width:100%; line-height:0.5rem;">

                <tr style="height:0.01rem; line-height:0.01rem; border-right:1px solid #151515;">                                    
                    <td v-for="inx in Array(51)" :key="inx" class="border-0 border-dark" style="width:1%;" />
                    <td class="" colspan="1" style="border-left:1px solid; width:1%;"/> 
                    <td v-for="inx in Array(50)" :key="inx" class="border-0 border-dark" style="width:1%;" />                                                                                   
                </tr>              
<!-- <ROW1> -->
                <tr style="height:0.25rem; line-height:0.5rem;">
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="50">LOCATION OF KEY</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="50">LOCATION OF VEHICLE</td>
                </tr>
                <tr style="height:0.85rem; line-height:0.65rem;">
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="50">{{formData.locationOfKeys}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="50">{{formData.locationOfVehicle}}</td>
                </tr>
<!-- <ROW2> -->
                <tr style="height:0.25rem; line-height:0.5rem; border-top:1px solid;">
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="27">VEHICLE RELEASED TO</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="43">SIGNATURE OF PERSON RECEIVING VEHICLE</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="29">DATE AND TIME RELEASED</td>
                </tr>
                <tr style="height:0.85rem; line-height:0.65rem;">
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="27">{{formData.vehicleReleasedTo}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="43"></td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="29">{{formData.dateReleased}} {{formData.timeReleased}}</td>
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
export default class Form24hTable6 extends Vue {

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
            vehicleImpounded: false,                     
            locationOfKeys: '',
            locationOfVehicle: '',
            vehicleReleasedTo: '',
            dateReleased: '',
            timeReleased: ''            
        }

        let vehicleLocationInfo = '';
        let vehicleReleasedTo = '';
        let locationOfKeys = '';
        let dateReleased = '';
        let timeReleased = '';
        
        if (form24.vehicleImpounded){
            vehicleLocationInfo = 'IMPOUNDED';            
            locationOfKeys = form24.locationOfKeys?form24.locationOfKeys.toUpperCase():'';
            vehicleReleasedTo = '';
            dateReleased = '';
            timeReleased = '';
        } else {
            if (form24.notImpoundingReason == 'Left at roadside'){
                vehicleLocationInfo = 'LEFT AT ROADSIDE'
                vehicleReleasedTo = '';
                locationOfKeys = '';
                dateReleased = '';
                timeReleased = '';
            } else if (form24.notImpoundingReason == 'Released to other driver'){
                vehicleLocationInfo = ''
                vehicleReleasedTo = form24.vehicleReleasedTo?form24.vehicleReleasedTo.toUpperCase():'';
                locationOfKeys = '';
                dateReleased = Vue.filter('format-date-dash')(form24.releasedDate);
                timeReleased = form24.releasedTime.substr(0,2)+ ':' + form24.releasedTime.substr(2,2);
            }
            
        }

        this.formData.vehicleImpounded = form24.vehicleImpounded;
        this.formData.locationOfKeys = locationOfKeys?locationOfKeys:'';
        this.formData.locationOfVehicle = vehicleLocationInfo?vehicleLocationInfo:'';
        this.formData.vehicleReleasedTo = vehicleReleasedTo?vehicleReleasedTo:'';
        this.formData.dateReleased = dateReleased?dateReleased:'';
        this.formData.timeReleased = timeReleased?timeReleased:''; 
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