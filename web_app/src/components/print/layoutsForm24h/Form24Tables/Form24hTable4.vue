<template>
    <div v-if="dataReady">

        <div class="row margin-top-n0-25" style="margin:0.5rem 0 0 0; line-height:0.25rem;">
            <div class="text-center" style="font-size:9pt; width:100%;"><b>VEHICLE INFORMATION</b></div>            
        </div>

        <div class="row margin-top-n0-40" style="font-size:6pt; margin:0.35rem 0 0 0;">
            <table class="border border-dark text-left" style="width:100%; line-height:0.5rem;">
                <tr style="height:0.01rem; line-height:0.01rem; border-right:1px solid #151515;">
                    <td class="bg-dark" style="width:1%;"/>
                    <td class="bg-dark" style="width:1%;"/>
                    <td class="" style="width:1%;"/>
                    <td v-for="inx in Array(100)" :key="inx" class="border-0 border-dark" style="width:1%;" />                                                                                                     
                </tr>
<!-- <ROW1> -->
                <tr style="height:0.25rem; line-height:0.5rem; border-top:0px solid;">
                    <td class="bg-dark text-white"  style="" colspan="2"><b>O</b></td>
                    <td class="" style="" colspan="1"> </td>
                    <td class="" style="" colspan="50">SURNAME (print)</td> 
                    <td class="" style="" colspan="50">GIVEN</td>                                                           
                </tr>
                <tr style="height:0.85rem; line-height:0.65rem;">
                    <td class="bg-dark text-white"  style="" colspan="2"><b>W</b></td>
                    <td class="" style="" colspan="1" />
                    <td class="answer"    style="" colspan="50">{{formData.ownerLastName}}</td> 
                    <td class="answer" style="" colspan="50">{{formData.ownerFirstName}}</td>                                                           
                </tr>
<!-- <ROW2> -->
                <tr style="height:0.25rem; line-height:0.5rem; border-top:1px solid;">
                    <td class="bg-dark text-white"  style="" colspan="2"><b>N</b></td>
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="35">ADDRESS</td>
                    <td class="" style="" colspan="29">CITY</td>
                    <td class=""  style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="15">PROV/STATE</td>
                    <td class=""  style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="19">POSTAL CODE</td>                                                          
                </tr>
                <tr style="height:0.85rem; line-height:0.65rem;">
                    <td class="bg-dark text-white"  style="line-height:0.5rem;" colspan="2"><b>E R</b></td>
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="35">{{formData.ownerAddress}}</td> 
                    <td class="answer" style="" colspan="29">{{formData.ownerCity}}</td>
                    <td class=""  style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="15">{{formData.ownerProvince}}</td>
                    <td class=""  style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="19">{{formData.ownerPostalCode}}</td>                                               
                </tr>
<!-- <ROW3> -->                
                <tr style="height:0.25rem;  line-height:0.5rem; border-top:1px solid;">
                    <td class="bg-dark text-white"  style="" colspan="2"><b></b></td>
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="18">LICENCE NUMBER</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="11">PROV/STATE</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="7">L/YEAR</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="18">VAL TAG NUMBER</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="24">REGISTRATION NUMBER</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="17">VEHICLE TYPE</td>                                                          
                </tr>
                <tr style="height:0.85rem; line-height:0.65rem;">
                    <td class="bg-dark text-white"  style="line-height:0.5rem;" colspan="2"><b>V E</b></td>
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="18">{{formData.plate}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="11">{{formData.plateProvince}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="7">{{formData.plateYear}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="18">{{formData.valTagNumber}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="24">{{formData.registrationNumber}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="17">{{formData.vehicleType}}</td>                                          
                </tr>

                
<!-- <ROW4> -->
                <tr style="height:0.25rem;  line-height:0.5rem; border-top:1px solid;">
                    <td class="bg-dark text-white"  style="" colspan="2"><b>H</b></td>                   
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="18">VEHICLE MAKE</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="14">MODEL</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="7">YEAR</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="17">COLOUR</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="16">PUJ CODE</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="23">NSC NUMBER</td>                                                          
                </tr>
                <tr style="height:0.85rem; line-height:0.65rem;">
                    <td class="bg-dark text-white"  style="" colspan="2"><b>I</b></td>
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="18">{{formData.vehicleMake}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="14">{{formData.vehicleModel}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="7">{{formData.vehicleYear}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="17">{{formData.vehicleColor}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="16">{{formData.pujCode}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="23">{{formData.nscNumber}}</td>                                          
                </tr>
<!-- <ROW5> -->
                <tr style="height:0.25rem; line-height:0.5rem; border-top:1px solid;">
                    <td class="bg-dark text-white"  style="" colspan="2"><b>C</b></td>
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="59">VEHICLE IDENTIFICATION (SERIAL) NUMBER</td>
                    <td class=""  style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="40">OWNER CONTACT NUMBER</td>                                                        
                </tr>
                <tr style="height:0.85rem; line-height:0.65rem;">
                    <td class="bg-dark text-white"  style="line-height:0.5rem;" colspan="2"><b>L E</b></td>
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="59">{{formData.vinNumber}}</td> 
                    <td class=""  style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="40">{{formData.ownerPhoneNumber}}</td>                                       
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
export default class Form24hTable4 extends Vue {

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
            ownerFirstName: '',
            ownerLastName: '',            
            ownerAddress: '',
            ownerCity: '',
            ownerProvince: '',
            ownerPostalCode: '',
            ownerPhoneNumber: '',
            vehicleYear: '',
            vehicleMake:'',
            vehicleModel: '',
            vehicleType: '',
            vehicleColor: '',
            plateProvince: '',
            plate: '',
            plateYear: '',
            valTagNumber: '',
            registrationNumber: '',
            pujCode: '',
            nscNumber: '',
            vinNumber: ''                      
        }

        if (form24.ownerOrganization){
            this.formData.ownerLastName = form24.ownerOrganizationName?form24.ownerOrganizationName.toUpperCase():'';           

        } else {
            this.formData.ownerFirstName = form24.ownerFirstName?form24.ownerFirstName.toUpperCase():'';
            this.formData.ownerLastName = form24.ownerLastName?form24.ownerLastName.toUpperCase():'';
        }

        this.formData.ownerAddress = form24.ownerAddress?form24.ownerAddress.toUpperCase():'';
        this.formData.ownerCity = form24.ownerCity?form24.ownerCity.toUpperCase():'';
        this.formData.ownerProvince = form24.ownerProvince?.objectCd?form24.ownerProvince.objectCd.toUpperCase():'';
        this.formData.ownerPostalCode = form24.ownerPostalCode?form24.ownerPostalCode.toUpperCase():'';
        this.formData.ownerPhoneNumber = form24.ownerPhoneNumber?form24.ownerPhoneNumber.toUpperCase():'';
       
        const colorList = form24.vehicleColor?form24.vehicleColor.map( o => o.display_name):[];
    
        this.formData.vehicleYear = form24.vehicleYear?form24.vehicleYear.toUpperCase():'';
        this.formData.vehicleMake = form24.vehicleMake?.mk?form24.vehicleMake.mk.toUpperCase():'';
        this.formData.vehicleModel = form24.vehicleMake?.md?form24.vehicleMake.md.toUpperCase():'';
        this.formData.vehicleType = form24.vehicleType?.code?form24.vehicleType.code.toUpperCase():'';
        this.formData.vehicleColor = colorList.length>0?colorList.toString():'';
        this.formData.plateProvince = form24.plateProvince?.objectCd?form24.plateProvince.objectCd.toUpperCase():'';
        this.formData.plate = form24.plateNumber?form24.plateNumber.toUpperCase():'';
        this.formData.plateYear = form24.plateYear?form24.plateYear:'';
        this.formData.pujCode = form24.puj_code?.objectCd?form24.puj_code.objectCd.toUpperCase():'';
        this.formData.valTagNumber = form24.plateValTag?form24.plateValTag.toUpperCase():'';
        this.formData.registrationNumber = form24.registrationNumber?form24.registrationNumber.toUpperCase():'';        
            
        this.formData.nscNumber = form24.nscNumber?form24.nscNumber.toUpperCase():'';
        this.formData.vinNumber = form24.vin_number?form24.vin_number.toUpperCase():''; 
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