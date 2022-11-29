<template>
    <b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light">
        <b-card-header class="text-left h3" header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
            <b>Vehicle information</b>      
        </b-card-header>
        
        <b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">
            <b-alert
				:show="errorDismissCountDown"
				style="margin:0 0 2rem auto;"
				dismissible
				@dismissed="errorDismissCountDown=0"
				@dismiss-count-down="errorDismissCountDown=$event;"
				variant="danger"
                > {{error}}
            </b-alert>
            <b-row class="text-left">
                <b-col cols="3" >
                    <label class="m-0 p-0"> Jurisdiction  <span class="text-danger">*</span> </label>
                    <input-search-form
                        :data="vehicleInfo"
                        dataField="plateProvince"
                        :optionList="jurisdictions"
                        optionLabelField="objectDsc"
                        :error="vehicleState.plateProvince==false?'Please select one!':''"
                        :disabled="formPrinted"
                        placeholder="Search for a Jurisdiction"
                        @update="update"
                    />                          
                </b-col>
                <b-col class="pr-2" cols="4">
                    <label class="ml-1 m-0 p-0"> Plate Number <span class="text-danger">*</span></label>
                    <b-form-input
                        size="lg"
                        v-model="vehicleInfo.plateNumber"
                        :disabled="formPrinted"
                        :state="vehicleState.plateNumber"
                        @change="update"
                        placeholder="Plate">
                    </b-form-input>                                
                </b-col>
                <b-col class="p-0 pt-1" cols="1">
                    <b-button 
                        size="lg"
                        class="bg-primary text-white"
                        style="margin-top:1.7rem;"
                        :disabled="formPrinted || !displayIcbcPlateLookup"                        
                        @click="triggerPlateLookup">
                        <spinner 
                            color="#FFF" 
                            v-if="searchingLookup" 
                            style="margin:0; padding: 0; transform:translate(-12px,-22px);"/>
                        <span style="font-size: 13pt;">ICBC Prefill</span>
                    </b-button>  
                </b-col>
            </b-row>
            <b-row class="text-left">
                <b-col  cols="2" >
                    <label class="ml-1 m-0 p-0"> Vehicle Year </label>
                    <input-search-form
                        :data="vehicleInfo"
                        dataField="vehicleYear" 
                        :optionList="vehicleYears"
                        optionLabelField=""
                        :error="vehicleState.vehicleYear==false?'Please select one!':''"
                        :disabled="formPrinted"
                        placeholder="Select a vehicle year"
                        @update="update"
                    />                                          
                </b-col>
                <b-col cols="6">
                    <label class="ml-1 m-0 p-0"> Vehicle Make and Model </label>
                    <input-search-form
                        :data="vehicleInfo"
                        dataField="vehicleMake" 
                        :optionList="vehicles"
                        optionLabelField="search"
                        :error="vehicleState.vehicleMake==false?'Please select one!':''"
                        :disabled="formPrinted"
                        placeholder="Search for a vehicle make and model"
                        @update="update"
                    />                
                     
                </b-col>
                
                <b-col  cols="3">                    
                    <vehicle-color-form
                        label="Vehicle Colour(s)"
                        :data="vehicleInfo"
                        dataField="vehicleColor" 
                        :optionList="vehicleColours"
                        optionLabelField="display_name"
                        optionTrackField="code"
                        :error="vehicleState.vehicleColor==false?'Please select one!':''"
                        :disabled="formPrinted"
                        placeholder="Search for a car colour"
                        @update="update"
                    /> 
                                                     
                </b-col>
            </b-row>
            <b-row class="text-left">				

                <b-col cols="3">
                    <label class="ml-1 m-0 p-0"> NSC Prov / State </label>
                    <input-search-form
                        :data="vehicleInfo"
                        dataField="puj_code" 
                        :optionList="jurisdictions"
                        optionLabelField="objectDsc"
                        :error="vehicleState.puj_code==false?'Please select one!':''"
                        :disabled="formPrinted"
                        placeholder="Search for a Province or State"
                        @update="update"
                    />					
                </b-col>
                <b-col cols="7">
                    <label class="ml-1 m-0 p-0"> NSC Number</label>
                    <b-form-input
                        size="lg"
                        :class="vehicleInfo.nscNumber.length > 14?'is-invalid':''"
                        v-model="vehicleInfo.nscNumber"						
                        :disabled="formPrinted"
                        :state="vehicleState.nscNumber"
                        @change="update">
                    </b-form-input>
                    <div 
                        v-if="vehicleInfo.nscNumber.length > 14" 
                        style="font-size:10pt;" 
                        class="text-danger text-left m-0 mt-n p-0">
                        The NSC number cannot exceed 14 characters.
                    </div>					                             
                </b-col>
            </b-row>			
        </b-card>

    </b-card>
</template>


<script lang="ts">

import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace } from "vuex-class";

import "@/store/modules/common";
const commonState = namespace("Common");

import "@/store/modules/forms/mv2906";
const mv2906State = namespace("MV2906");

import { jurisdictionInfoType, provinceInfoType, vehicleColourInfoType, vehicleInfoType, vehicleStyleInfoType } from '@/types/Common';
import { twelveHourFormStatesInfoType, twelveHourFormDataInfoType, twelveHourFormJsonInfoType } from '@/types/Forms/MV2906';
import Spinner from "@/components/utils/Spinner.vue";
import { lookupPlateFromICBC } from '@/utils/icbc';
import {getArrayOfVehicleYears} from "@/utils/vehicle";

import InputSearchForm from '@/components/utils/InputSearchForm.vue'
import VehicleColorForm from '@/components/utils/VehicleColorForm.vue'

@Component({
    components: {           
        Spinner,
        InputSearchForm,
        VehicleColorForm 
    }        
}) 
export default class VehicleInformationCard extends Vue {   

    @commonState.State
    public jurisdictions: jurisdictionInfoType[];

    @commonState.State
    public provinces: provinceInfoType[];

    @commonState.State
    public vehicles: vehicleInfoType[];

    @commonState.State
    public vehicle_styles: vehicleStyleInfoType[];

    @commonState.State
    public vehicleColours: vehicleColourInfoType[];	

    @mv2906State.State
    public mv2906Info: twelveHourFormJsonInfoType;

    @Prop({required: true})
    vehicleInfo!: twelveHourFormDataInfoType;
    
    @Prop({required: true})
    vehicleState!: twelveHourFormStatesInfoType;

    dataReady = false;  
    
    error = '';
    path = '';
    showScannerMessage = false;
    scannerOpened = false;
    scannerMessage = '';
    searchingLookup = false;
    searchingDl = false;
    formPrinted = false;
    vehicleYears = [];
    displayIcbcPlateLookup=true
    errorDismissCountDown=0

    mounted() { 
        this.dataReady = false;        
        this.formPrinted = Boolean(this.mv2906Info.printed_timestamp);
        this.extractFields();
        this.checkIcbcPlateLookupAllowed()
        this.dataReady = true;
    }

    public extractFields(){		
        this.path = 'forms/' + this.mv2906Info.form_type + '/' + this.mv2906Info.form_id + '/data';
        this.vehicleYears = getArrayOfVehicleYears();
    }

    public triggerPlateLookup(){		
        this.error = ''
        this.searchingLookup = true;
        lookupPlateFromICBC([this.mv2906Info.data.plateNumber, this.path ])
            .then(() => {
                const data = this.$store.state.forms['12Hour'][this.mv2906Info.form_id] //TODO: get this 'data' from ICBC
                this.updateFormFields(data);
                this.searchingLookup = false;
            })
            .catch( error => {
                console.log("error", error)
                this.searchingLookup = false;
                this.error = error.description;
                this.errorDismissCountDown=3
            })
    }

    public updateFormFields(data: any){
        this.vehicleInfo.vehicleYear = data['vehicleModelYear'];		
        this.vehicleInfo.vehicleColor = [{code: data['vehicleColour'], display_name: data['vehicleColour'], colour_class: data['vehicleColour']}];
        //TODO: fix color info fields
        this.vehicleInfo.vehicleMake = {
            "md": data['vehicleMake'], 
            "mk": data['vehicleModel'], 
            "search": data['vehicleMake'] + " - " + data['vehicleModel']};
    }

    public update(){  
        this.checkIcbcPlateLookupAllowed()
        this.recheckStates()
    }

    public recheckStates(){
        this.$emit('recheckStates')
    }

    public checkIcbcPlateLookupAllowed(){
        this.displayIcbcPlateLookup = this.vehicleInfo.plateProvince.objectCd == "BC" && this.$store.state.isUserAuthorized;
    }

 
}
</script>

<style scoped lang="scss">

    label{
        font-size: 16pt;
    }

    input.is-invalid {
        background: #ebc417;
    }
    select.is-invalid {
        background: #ebc417;
        option {
            background: #FFF;
        }
    }

</style>
