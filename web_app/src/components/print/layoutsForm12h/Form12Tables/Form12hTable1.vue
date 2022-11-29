<template>
    <div v-if="dataReady">
        <div class="row lineheight0-25" style="font-size:11pt; margin:0rem 0 0 0;   line-height:1rem;"><b>NOTICE OF 12-HOUR </b></div>
        <div class="row lineheight0-25" style="font-size:11pt; margin:0rem 0 0 0;   line-height:1rem;"><b>LICENCE SUSPENSION</b></div>
        <div class="row lineheight0-25 margin-top-0" style="margin:0.5rem 0 0 0; line-height:1rem;">
            <div class="answer text-left" style="font-size:11pt; width:67%;">{{formData.formId}}</div>
            <div style="font-size:6pt; width:33%;transform:translate(0,6px);">MICROFILM NO.</div>
        </div>
        
        <div class="row margin-top-0" style="font-size:6pt; margin:0.4rem 0 0 0;">
            <table class="border border-dark text-left" style="width:100%; line-height:0.5rem;">
                
                <tr style="height:0.01rem; line-height:0.01rem;">
                    <td class="bg-dark" style="width:1%;"/>
                    <td class="" style="width:1%;"/>
                    <td v-for="inx in Array(98)" :key="inx" class="border-0 border-dark" style="width:1%;" />                                                                                
                </tr>

<!-- <ROW1> -->
                <tr style="height:0.25rem;  line-height:0.75rem; border-top:0px solid;">
                    <td class="bg-dark text-white"  style="line-height:0.5rem;" colspan="1" rowspan="2"><b>T O</b></td>
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="49">SURNAME (print)</td> 
                    <td class="" style="" colspan="49">GIVEN</td>                                                           
                </tr>
                <tr style="height:0.95rem;line-height:0.65rem;">
                    <td class="" style="" colspan="1" />
                    <td class="answer"    style="" colspan="49">{{formData.surName}}</td> 
                    <td class="answer" style="" colspan="49">{{formData.givenName}}</td>                                                           
                </tr>
<!-- <ROW2> -->
                <tr style="height:0.25rem;  line-height:0.75rem; border-top:1px solid;">
                    <td class="bg-dark text-white m-0 p-0 "  style="" colspan="1"><b>D </b></td>
                    <td class="" style="" colspan="1" />
                    <td class=""  style="" colspan="48">DRIVER'S LICENCE NO.</td>
                    <td class=""  style="border-left:1px solid;" colspan="1"></td>
                    <td class=""  style="" colspan="20">PROVINCE</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="28">DOB (yyyymmdd)</td>                                                          
                </tr>
                <tr style="height:0.95rem; line-height:0.65rem;">
                    <td class="bg-dark text-white m-0 p-0 "  style="line-height:0.5rem;" colspan="1"><b>R I</b></td>
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="48">{{formData.dlNumber}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer text-center" style="font-size:12pt;" colspan="20">{{formData.province}}</td> 
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="28">{{formData.dob}}</td>                                                
                </tr>
<!-- <ROW3> -->
                <tr style="height:0.25rem; line-height:0.75rem; border-top:1px solid;">
                    <td class="bg-dark text-white m-0 p-0 "  style="" colspan="1"><b>V </b></td>
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="43">ADDRESS (STREET)</td>
                    <td class="" style="" colspan="35">CITY/MUNICIPALITY</td>                     
                    <td class="" style="" colspan="20">POSTAL CODE</td>                                                          
                </tr>
                <tr style="height:0.95rem; line-height:0.65rem;">
                    <td class="bg-dark text-white m-0 p-0 "  style="line-height:0.5rem;" colspan="1"><b>E R</b></td>
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="43">{{formData.address}}</td> 
                    <td class="answer" style="" colspan="35">{{formData.city}}</td> 
                    <td class="answer" style="" colspan="20">{{formData.postalCode}}</td>                                               
                </tr>

<!-- <ROW4> -->
                <tr style="height:0.25rem;  line-height:0.75rem; border-top:1px solid;">                    
                    <td class="" style="" colspan="1" />
                    <td class=""  style="" colspan="48">PHONE NUMBER</td>
                    <td class=""  style="border-left:1px solid;" colspan="1"></td>
                    <td class=""  style="" colspan="12">PUJ CODE</td>
                    <td class="" style="" colspan="1"></td>
                    <td class="" style="" colspan="37">NSC NUMBER</td>                                                          
                </tr>
                <tr style="height:0.95rem; line-height:0.65rem;">                    
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="48">{{formData.phoneNumber}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="11">{{formData.pujCode}}</td> 
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="38">{{formData.nscNumber}}</td>                                                
                </tr>

<!-- <ROW5> -->
                <tr style="height:1.2rem; line-height:0.5rem; border-top:1px solid;">
                    <td class="" style="" colspan="2" />
                    <td class="" style="" colspan="10">REASON:</td>
                    <td class="" style="" colspan="5"> 
                        <check-box
                            shiftBox="20px,-2px"
                            shiftmark="-2px,0px"                                   
                            checkColor="#2134AB"
                            boxSize="1.5em"
                            :check="formData.alcohol"
                            checkFontSize="16pt"                                     
                            text="" /> 
                    </td>
                    <td class="" style="" colspan="18">90.3(2) <b>ALCOHOL</b></td> 
                    <td class="" style="" colspan="7"><b style="text-decoration: underline;">OR</b></td>
                    <td class="" style="" colspan="6">
                        <check-box
                            shiftBox="20px,-2px"
                            shiftmark="-2px,0px"                                   
                            checkColor="#2134AB"
                            boxSize="1.5em" 
                            :check="formData.drugs"
                            checkFontSize="16pt"
                            text="" />
                    </td>
                    <td class="" style="" colspan="25">90.3(2.1) <b>DRUGS</b></td>
                    <td class="" style="" colspan="27" />                                                        
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
export default class Form12hTable1 extends Vue {

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
            formId: '',
            surName:'',
            givenName: '',
            dlNumber: '',
            province: '',
            dob: '',
            address: '',
            city: '',
            postalCode: '',
            phoneNumber: '',
            pujCode: '',
            nscNumber: '',
            alcohol: false,
            drugs: false
        }

        this.formData.formId = this.mv2906Info.form_id? this.mv2906Info.form_id.toUpperCase():'';
        this.formData.surName = form12.lastName? form12.lastName.toUpperCase():'';
        this.formData.givenName = form12.givenName? form12.givenName.toUpperCase():'';
        this.formData.dlNumber = form12.driversNumber? form12.driversNumber.toUpperCase():'';
        this.formData.province = form12.driversLicenceJurisdiction?.objectCd? form12.driversLicenceJurisdiction.objectCd.toUpperCase():'';
        this.formData.dob = form12.dob? form12.dob:'';
        this.formData.address = form12.address? form12.address.toUpperCase():'';
        
        let city = form12.driverCity? form12.driverCity.toUpperCase():'';
        city = form12.driverProvince?.objectCd? (city+', '+form12.driverProvince?.objectCd.toUpperCase()): city;
        this.formData.city = city

        this.formData.postalCode = form12.driverPostalCode?form12.driverPostalCode.toUpperCase():'';
        this.formData.phoneNumber = form12.driverPhoneNumber?form12.driverPhoneNumber:'';
        this.formData.pujCode = form12.puj_code?.objectCd?form12.puj_code.objectCd.toUpperCase():'';
        this.formData.nscNumber = form12.nscNumber?form12.nscNumber.toUpperCase():'';
        this.formData.alcohol = form12.prohibitionType && form12.prohibitionType == 'Alcohol';  
        this.formData.drugs = form12.prohibitionType && form12.prohibitionType == 'Drugs';    
           
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

.margin-top-0{
    margin-top: 0rem !important;
}

</style>