<template>
    <div v-if="dataReady">

        <div class="row margin-top-n0-25" style="margin:0.5rem 0 0 0; line-height:0.25rem;">
            <div class="text-center" style="font-size:9pt; width:100%;"><b>DISPOSITION OF VEHICLE</b></div>            
        </div>

        <div class="row margin-top-n0-40" style="font-size:6pt; margin:0.35rem 0 0 0;">
            <table class="border border-dark text-left" style="width:100%; line-height:0.5rem;">
                <tr style="height:0.01rem; line-height:0.01rem; border-right:1px solid #151515;">                   
                    <td v-for="inx in Array(100)" :key="inx" class="border-0 border-dark" style="width:1%;" />                                                                                                     
                </tr>

<!-- <ROW1> -->
                <tr style="height:0.25rem;  line-height:0.75rem; border-top:0px solid;">                                      
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="8">YEAR</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="14">MAKE</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="19">MODEL</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>                    
                    <td class="" style="" colspan="19">COLOUR</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="14">PROV/STATE</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="20">VEHICLE LIC. NO.</td>                                                          
                </tr>
                <tr style="height:0.95rem; line-height:0.65rem;">                    
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="8">{{formData.vehicleYear}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="14">{{formData.vehicleMake}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="19">{{formData.vehicleModel}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="19">{{formData.vehicleColor}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="14">{{formData.plateProvince}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="20">{{formData.plate}}</td>                                          
                </tr>


<!-- <ROW2> -->
                <tr style="height:0.25rem; line-height:0.75rem; border-top:1px solid;">                    
                    <td class="" style="" colspan="1"> </td>
                    <td class="" style="" colspan="99">LOCATION OF KEYS</td> 
                                                                            
                </tr>
                <tr style="height:0.95rem; line-height:0.65rem;">                    
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="99">{{formData.locationOfKeys}}</td>                                                                                
                </tr>

<!-- <ROW3> -->
                <tr style="height:0.25rem; line-height:0.75rem; border-top:1px solid;">                    
                    <td class="" style="" colspan="1"> </td>
                    <td class="" style="" colspan="99">LOCATION OF VEHICLE</td> 
                                                                            
                </tr>
                <tr style="height:0.95rem; line-height:0.65rem;">                    
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="99">{{formData.locationOfVehicle}}</td>                                                                                
                </tr>

<!-- <ROW4> -->
                <tr style="height:0.25rem; line-height:0.75rem; border-top:1px solid;">                    
                    <td class="" style="" colspan="1"> </td>
                    <td class="" style="" colspan="99">VEHICLE RELEASED TO (PLEASE PRINT)</td> 
                                                                            
                </tr>
                <tr style="height:0.95rem; line-height:0.65rem;">                    
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="99">{{formData.vehicleReleasedTo}}</td>                                                                                
                </tr>

<!-- <ROW2> -->
                <tr style="height:0.25rem; line-height:0.75rem; border-top:1px solid;">                    
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="58">SIGNATURE OF PERSON RECEIVING VEHICLE</td>
                    <td class=""  style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="40">DATE AND TIME RELEASED</td>
                                                     
                </tr>
                <tr style="height:0.95rem; line-height:0.65rem;">                    
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="58"></td>
                    <td class=""  style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="26">{{formData.dateReleased}}</td>
                    <td class=""  style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="13">{{formData.timeReleased}}</td>                                               
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
export default class Form12hTable4 extends Vue {

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

        const form12 = this.mv2906Info.data

        this.formData = {
            vehicleYear: '',
            vehicleMake:'',
            vehicleModel: '',
            vehicleColor: '',
            plateProvince: '',
            plate: '',
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
        
        if (form12.vehicleImpounded){
            const lineAddress = form12.impoundLot?.lot_address?form12.impoundLot.lot_address.toUpperCase()+', ':'';
            const city = form12.impoundLot?.city?form12.impoundLot.city.toUpperCase()+ ', ':'';
            const phone = form12.impoundLot?.phone?form12.impoundLot.phone:'';
            vehicleLocationInfo = lineAddress + city + phone;
            vehicleReleasedTo = form12.impoundLot?.name?form12.impoundLot.name.toUpperCase():'';
            locationOfKeys = form12.locationOfKeys?form12.locationOfKeys.toUpperCase():'';
            dateReleased = '';
            timeReleased = '';
        } else {
            if (form12.notImpoundingReason == 'Left at roadside'){
                vehicleLocationInfo = 'LEFT AT ROADSIDE'
                vehicleReleasedTo = '';
                locationOfKeys = '';
                dateReleased = '';
                timeReleased = '';
            } else {
                vehicleLocationInfo = ''
                vehicleReleasedTo = form12.vehicleReleasedTo?form12.vehicleReleasedTo.toUpperCase():'';
                locationOfKeys = '';
                dateReleased = Vue.filter('format-date-dash')(form12.releasedDate);
                timeReleased = form12.releasedTime.substr(0,2)+ ':' + form12.releasedTime.substr(2,2);
            }
            
        }

        const colorList = form12.vehicleColor?form12.vehicleColor.map( o => o.code):[];
    
        this.formData.vehicleYear = form12.vehicleYear?form12.vehicleYear.toUpperCase():'';
        this.formData.vehicleMake = form12.vehicleMake?.mk?form12.vehicleMake.mk.toUpperCase():'';
        this.formData.vehicleModel = form12.vehicleMake?.md?form12.vehicleMake.md.toUpperCase():'';
        this.formData.vehicleColor = colorList.length>0?colorList.toString():'';
        this.formData.plateProvince = form12.plateProvince?.objectCd?form12.plateProvince.objectCd.toUpperCase():'';
        this.formData.plate = form12.plateNumber?form12.plateNumber.toUpperCase():'';
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