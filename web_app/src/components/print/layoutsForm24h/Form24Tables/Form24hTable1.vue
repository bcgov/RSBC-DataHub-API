<template>
    <div v-if="dataReady">
        <div class="row lineheight0-0 margin-top-1" style="font-size:10pt; margin:0rem 0 0 0;   line-height:1rem;"><b>NOTICE OF 24-HOUR PROHIBITION</b></div>
        <div class="row lineheight0-15" style="font-size:10pt; margin:0rem 0 0 0;   line-height:1rem;"><b>AND REPORT TO ICBC</b></div>
        <div class="row lineheight0-15 margin-top-0" style="margin:0.5rem 0 0 0; line-height:1rem;">
            <div class="answer text-left" style="font-size:10pt; width:67%;">{{formData.formId}}</div>
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
                <tr style="height:0.25rem;  line-height:0.5rem; border-top:0px solid;">
                    <td class="bg-dark text-white"  style="line-height:0.5rem;" colspan="1" rowspan="2"><b>T O</b></td>
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="49">SURNAME (print)</td> 
                    <td class="" style="" colspan="49">GIVEN</td>                                                           
                </tr>
                <tr style="height:0.85rem;line-height:0.65rem;">
                    <td class="" style="" colspan="1" />
                    <td class="answer"    style="" colspan="49">{{formData.surName}}</td> 
                    <td class="answer" style="" colspan="49">{{formData.givenName}}</td>                                                           
                </tr>
<!-- <ROW2> -->
                <tr style="height:0.25rem;  line-height:0.5rem; border-top:1px solid;">
                    <td class="bg-dark text-white m-0 p-0 "  style="" colspan="1"><b>D </b></td>
                    <td class="" style="" colspan="1" />
                    <td class=""  style="" colspan="48">DRIVER'S LICENCE NO.</td>
                    <td class=""  style="border-left:1px solid;" colspan="1"></td>
                    <td class=""  style="" colspan="20">PROV/STATE</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="" style="" colspan="28">DOB (yyyymmdd)</td>                                                          
                </tr>
                <tr style="height:0.8rem; line-height:0.65rem;">
                    <td class="bg-dark text-white m-0 p-0 "  style="line-height:0.5rem;" colspan="1"><b>R I</b></td>
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="48">{{formData.dlNumber}}</td>
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="20">{{formData.jurisdiction}}</td> 
                    <td class="" style="border-left:1px solid;" colspan="1"></td>
                    <td class="answer" style="" colspan="28">{{formData.dob}}</td>                                                
                </tr>
<!-- <ROW3> -->
                <tr style="height:0.25rem; line-height:0.5rem; border-top:1px solid;">
                    <td class="bg-dark text-white m-0 p-0 "  style="" colspan="1"><b>V </b></td>
                    <td class="" style="" colspan="1" />
                    <td class="" style="" colspan="38">ADDRESS</td>
                    <td class="" style="" colspan="23">CITY</td> 
                    <td class="" style="" colspan="18">PROV/STATE</td>
                    <td class="" style="" colspan="19">POSTAL CODE</td>                                                          
                </tr>
                <tr style="height:0.8rem; line-height:0.65rem;">
                    <td class="bg-dark text-white m-0 p-0 "  style="line-height:0.5rem;" colspan="1"><b>E R</b></td>
                    <td class="" style="" colspan="1" />
                    <td class="answer" style="" colspan="38">{{formData.address}}</td> 
                    <td class="answer" style="" colspan="23">{{formData.city}}</td> 
                    <td class="answer" style="" colspan="18">{{formData.province}}</td>
                    <td class="answer" style="" colspan="19">{{formData.postalCode}}</td>                                               
                </tr>
<!-- <ROW4> -->
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
                    <td class="" style="" colspan="18">215(2) <b>ALCOHOL</b></td> 
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
                    <td class="" style="" colspan="25">215(3) <b>DRUGS</b></td>
                    <td class="" style="" colspan="27" />                                                        
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
export default class Form24hTable1 extends Vue {

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

        const form24 = this.mv2634Info.data;

        this.formData = {
            formId: '',
            surName:'',
            givenName: '',
            jurisdiction: '',
            dlNumber: '',
            province: '',
            dob: '',
            address: '',
            city: '',
            postalCode: '',
            alcohol: false,
            drugs: false
        }

        this.formData.formId = this.mv2634Info.form_id?this.mv2634Info.form_id.toUpperCase():'';
        this.formData.surName = form24.lastName?form24.lastName.toUpperCase():'';
        this.formData.givenName = form24.givenName?form24.givenName.toUpperCase():'';
        this.formData.jurisdiction = form24.driversLicenceJurisdiction.objectCd?form24.driversLicenceJurisdiction.objectCd.toUpperCase():'';
        this.formData.dlNumber = form24.driversNumber?form24.driversNumber.toUpperCase():'';
        this.formData.province = form24.driverProvince.objectCd?form24.driverProvince.objectCd.toUpperCase():'';
        this.formData.dob = form24.dob?form24.dob:'';
        this.formData.address = form24.address?form24.address.toUpperCase():'';
        this.formData.city = form24.driverCity?form24.driverCity.toUpperCase():'';
        this.formData.postalCode = form24.driverPostalCode?form24.driverPostalCode.toUpperCase():'';
        
        this.formData.alcohol = form24.prohibitionType && form24.prohibitionType == 'Alcohol';  
        this.formData.drugs = form24.prohibitionType && form24.prohibitionType == 'Drugs';    
           
    }

    
}

</script>

<style scoped>

.answer {
    color: rgb(3, 19, 165);
    font-size: 7pt;
    font-weight: 600;
}

.lineheight0-0{
    line-height:0.05rem !important;
}

.lineheight0-15{
    line-height:0.15rem !important;
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

.margin-top-1{
    margin-top: 1rem !important;
}

</style>