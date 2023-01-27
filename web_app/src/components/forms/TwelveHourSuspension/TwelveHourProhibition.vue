<template>
    <b-card header-tag="header" bg-variant="light" border-variant="primary" class="mx-auto p-0">
        <b-card-header class="h2" header-bg-variant="secondary" header-border-variant="dark" header-text-variant="white">            
            Notice of 12 Hour Licence Suspension
        </b-card-header>
        <b-card no-body v-if="dataReady" border-variant="light" bg-variant="light" class="my-0 mx-auto p-0" :key="'m12-'+updatedInfo">
            <b-row class="pt-2 pb-0 text-danger border-light">            
                <div class="ml-auto mr-2 h4">{{id}}</div>      
            </b-row>
            
            <drivers-information-card :driverInfo="twelveHourData" :driverState="fieldStates" @recheckStates="recheckStates()" />
            <vehicle-information-card class="mt-5" :vehicleInfo="twelveHourData" :vehicleState="fieldStates" @recheckStates="recheckStates()"/>
            <vehicle-disposition-card class="mt-5" :vdInfo="twelveHourData" :vdState="fieldStates" @recheckStates="recheckStates()"/>
            <prohibition-information-card class="mt-5" :prohibitionInfo="twelveHourData" :prohibitionState="fieldStates" @recheckStates="recheckStates()"/>
            <officer-details-card class="mt-5" :officerInfo="twelveHourData" :officerState="fieldStates" @recheckStates="recheckStates()"/>

        </b-card>
       
        <b-card class="mt-5">
            <b-button @click="navigateToPrintPage" variant="primary"><b style="font-size:15pt">Print All Copies</b> </b-button>
        </b-card>
        
    </b-card>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator';

import DriversInformationCard from "@/components/forms/TwelveHourSuspension/DriversInformationCard.vue";
import OfficerDetailsCard from "@/components/forms/TwelveHourSuspension/OfficerDetailsCard.vue";
import VehicleInformationCard from "@/components/forms/TwelveHourSuspension/VehicleInformationCard.vue";
import PrintDocuments from "../PrintDocuments.vue";
import ProhibitionInformationCard from "@/components/forms/TwelveHourSuspension/ProhibitionInformationCard.vue";
import VehicleDispositionCard from "@/components/forms/TwelveHourSuspension/VehicleDispositionCard.vue";

import { twelveHourFormDataInfoType, twelveHourFormJsonInfoType, twelveHourFormStatesInfoType } from '@/types/Forms/MV2906';
import { cityInfoType, currentlyEditingFormObjectInfoType, formsInfoType, impoundLotOperatorsInfoType } from '@/types/Common';

import { namespace } from "vuex-class";
import "@/store/modules/common";
const commonState = namespace("Common");

import "@/store/modules/forms/mv2906";
const mv2906State = namespace("MV2906");

@Component({
	components:{        
        PrintDocuments,
		ProhibitionInformationCard,
		DriversInformationCard,
		OfficerDetailsCard,
		VehicleInformationCard,
		VehicleDispositionCard
    }
})
export default class TwelveHourProhibition extends Vue {  

	@mv2906State.State
    public mv2906Info: twelveHourFormJsonInfoType;
	
	@commonState.State
    public formsInfo: formsInfoType;

    @commonState.State
    public currently_editing_form_object: currentlyEditingFormObjectInfoType;

	@commonState.Action
    public UpdateCurrentlyEditingFormObject!: (newCurrentlyEditingFormObject: currentlyEditingFormObjectInfoType) => void	

	@mv2906State.Action
    public UpdateMV2906Info!: (newMV2906Info: twelveHourFormJsonInfoType) => void
	
	name = '12Hour'; 
	updatedInfo = 0;
    dataReady = false;
    fieldStates = {} as twelveHourFormStatesInfoType;

	id = '';
	movedToPrintPage = false;
	twelveHourFormData = {} as twelveHourFormJsonInfoType;
    twelveHourData = {} as twelveHourFormDataInfoType;

	variants = ["icbc", "driver", "police"];

	mounted() {		
		this.id = this.currently_editing_form_object.form_id;
		// const payload = {form_type: this.name, form_id: this.id}
		this.clearStates()
		// this.UpdateCurrentlyEditingFormObject(payload);
        const formData = this.$store.state.forms[this.name][this.id]
        //console.log(formData)
        this.UpdateMV2906Info(formData)

		this.extractCurrentlyEditedFormData();        		
		
	}

	public extractCurrentlyEditedFormData() {

        //console.log(this.mv2906Info)

        if(this.mv2906Info?.data?.driversLicenceJurisdiction?.objectCd){
            //console.log('updateData')
            this.twelveHourFormData = this.mv2906Info            
        }else{
            //console.log('init')
            this.prepopulateDefaultValues()            
            this.recheckStates()
        }  
        this.twelveHourData = this.twelveHourFormData.data      
		this.dataReady = true;
	}

    public prepopulateDefaultValues(){
        const twelveHourData = {} as twelveHourFormDataInfoType

        twelveHourData.driversNumber="";
        twelveHourData.givenName='';
        twelveHourData.lastName='';
        twelveHourData.dob='';
        twelveHourData.driversLicenceJurisdiction= {"objectCd":"BC","objectDsc":"BRITISH COLUMBIA"};
        twelveHourData.address='';
        twelveHourData.driverPhoneNumber='';
        twelveHourData.driverCity='';
        twelveHourData.driverProvince= {"objectCd":"","objectDsc":""};
        twelveHourData.driverPostalCode='';
        twelveHourData.plateProvince= {"objectCd":"BC","objectDsc":"BRITISH COLUMBIA"};
        twelveHourData.plateNumber='';
        
        twelveHourData.puj_code= {"objectCd":"","objectDsc":""};
        twelveHourData.nscNumber='';
                
        twelveHourData.vehicleYear='';
        twelveHourData.vehicleMake={md:'', mk:'', search:''};
        twelveHourData.vehicleColor=[];
        
        twelveHourData.prohibitionType='';
           
        twelveHourData.vehicleImpounded=null; 
        twelveHourData.impoundLot= {} as impoundLotOperatorsInfoType;
        twelveHourData.locationOfKeys='';
        twelveHourData.notImpoundingReason='';
        twelveHourData.releasedDate='';
        twelveHourData.releasedTime='';
        twelveHourData.vehicleReleasedTo='';

        twelveHourData.offenceAddress='';
        twelveHourData.offenceCity = {} as cityInfoType; 
        twelveHourData.agencyFileNumber='';
        twelveHourData.prohibitionStartDate='';
        twelveHourData.prohibitionStartTime='';


        twelveHourData.agency='';
        twelveHourData.badge_number='';
        twelveHourData.officer_name='';
        
        twelveHourData.submitted=false;
        
        this.twelveHourFormData = this.mv2906Info
        this.twelveHourFormData.data = twelveHourData
        
    }

	public clearStates(){
        const twelveHourFormStates = {} as twelveHourFormStatesInfoType;        
        twelveHourFormStates.driversNumber=null
        twelveHourFormStates.givenName=null
        twelveHourFormStates.lastName=null
        twelveHourFormStates.dob=null   
        twelveHourFormStates.address=null
        twelveHourFormStates.driverPhoneNumber=null
        twelveHourFormStates.driverCity=null
        twelveHourFormStates.driverProvince=null
        twelveHourFormStates.driverPostalCode=null
        twelveHourFormStates.agency=null
        twelveHourFormStates.badgeNumber=null
        twelveHourFormStates.driversLicenceJurisdiction=null
        twelveHourFormStates.officerName=null
        twelveHourFormStates.plateProvince=null    
        twelveHourFormStates.plateNumber=null         
        twelveHourFormStates.puj_code=null 
        twelveHourFormStates.nscNumber=null 
        twelveHourFormStates.registrationNumber=null 
        twelveHourFormStates.vehicleYear=null
        twelveHourFormStates.vehicleMake=null 
        twelveHourFormStates.vehicleColor=null   
        twelveHourFormStates.vehicleImpounded=null    
        twelveHourFormStates.locationOfKeys=null 
        twelveHourFormStates.impoundLotName=null 
        twelveHourFormStates.impoundLotAddress=null 
        twelveHourFormStates.impoundLotCity=null 
        twelveHourFormStates.impoundLotPhone=null 
        twelveHourFormStates.notImpoundingReason=null    
        twelveHourFormStates.vehicleReleasedTo=null    
        twelveHourFormStates.releasedDate=null 
        twelveHourFormStates.releasedTime=null 
        twelveHourFormStates.prohibitionType=null 
        twelveHourFormStates.offenceAddress=null 
        twelveHourFormStates.offenceCity=null 
        twelveHourFormStates.agencyFileNumber=null 
        twelveHourFormStates.prohibitionStartDate=null 
        twelveHourFormStates.prohibitionStartTime=null      
        twelveHourFormStates.submitted=null    

        this.fieldStates = twelveHourFormStates;
        this.dataReady = true
    }

	public recheckStates(){
        this.UpdateMV2906Info(this.twelveHourFormData)
        this.$store.commit("updateFormInRoot",this.twelveHourFormData)
        console.log('check')
        const specialFields = ['dob']
        for(const field of Object.keys(this.fieldStates)){
            if(this.fieldStates[field]==false && !specialFields.includes(field)){
                this.checkStates(false)
                return 
            }
        }  
    }

	public checkStates(finalCheck){
        const data = this.twelveHourFormData.data
        
        //__Driver's Information
        this.fieldStates.driversNumber = data.driversNumber? null:false;
        this.fieldStates.lastName = data.lastName? null:false;
        if(!data.dob) this.fieldStates.dob = false;
        this.fieldStates.address = data.address? null:false;
        this.fieldStates.driverCity = data.driverCity? null:false;
        this.fieldStates.driverProvince = data.driverProvince?.objectCd? null:false;

        if(data.driverPhoneNumber) 
            this.fieldStates.driverPhoneNumber = Vue.filter('verifyPhone')( data.driverPhoneNumber)? null:false;
        else 
            this.fieldStates.driverPhoneNumber = null;
        
        if(data.driverPostalCode)
            this.fieldStates.driverPostalCode = Vue.filter('verifyPostCode')(data.driverPostalCode, data.driverProvince?.objectCd)? null:false;      
        else 
            this.fieldStates.driverPostalCode = null;

        //__Vehicle Information
        this.fieldStates.plateProvince = data.plateProvince?.objectCd? null:false;
        this.fieldStates.plateNumber = data.plateNumber? null:false;


        //__Vehicle Disposition
        this.fieldStates.vehicleImpounded = data.vehicleImpounded==null? false : null;
        //Impounded
        this.fieldStates.locationOfKeys = data.vehicleImpounded==true && !data.locationOfKeys? false: null;         
        this.fieldStates.impoundLotName = data.vehicleImpounded==true && !data.impoundLot?.name ? false: null;
        this.fieldStates.impoundLotAddress = data.vehicleImpounded==true && !data.impoundLot?.lot_address ? false : null;
        this.fieldStates.impoundLotCity = data.vehicleImpounded==true && !data.impoundLot?.city ? false : null;
        this.fieldStates.impoundLotPhone = data.vehicleImpounded==true && !data.impoundLot?.phone ? false : null;
        //NotImpounded

        this.fieldStates.notImpoundingReason = data.vehicleImpounded==false && !data.notImpoundingReason ? false: null;
        
        this.fieldStates.vehicleReleasedTo = data.vehicleImpounded==false && data.notImpoundingReason=='Released to other driver' && !data.vehicleReleasedTo ? false: null;
                        
        if(data.vehicleImpounded==true || data.notImpoundingReason!='Released to other driver')
            this.fieldStates.releasedDate = null;
        else if(!data.releasedDate)
            this.fieldStates.releasedDate = false;
        
        if(data.vehicleImpounded==true || data.notImpoundingReason!='Released to other driver')
            this.fieldStates.releasedTime = null;
        else if(!data.releasedTime)
            this.fieldStates.releasedTime = false;
        
        //__Prohibition
        this.fieldStates.prohibitionType = data.prohibitionType==''? false: null;
        this.fieldStates.offenceAddress = data.offenceAddress? null : false;
        this.fieldStates.offenceCity = data.offenceCity?.objectCd? null : false;
        this.fieldStates.agencyFileNumber = data.agencyFileNumber? null : false;

        if(!data.prohibitionStartDate) this.fieldStates.prohibitionStartDate = false;
        if(!data.prohibitionStartTime) this.fieldStates.prohibitionStartTime = false;


        //__Officer
        this.fieldStates.agency = data.agency? null : false;


        for(const field of Object.keys(this.fieldStates)){
            if(this.fieldStates[field]==false){
                if(finalCheck) Vue.filter('findInvalidFields')()
                return false
            }                
        }       
        this.$store.commit("updateFormInRoot",this.twelveHourFormData)
        return true;            
    }

    public navigateToPrintPage(){
        if(this.checkStates(true)){
            const form_id = this.currently_editing_form_object.form_id
            const form_type = this.currently_editing_form_object.form_type
            this.$router.push({   
                name: 'print',
                params: { id: form_id, form_type: form_type}
            })
        }
    }

}
</script>

<style scoped>
  .lightgray {
    background-color: lightgray;
  }
  .prohibition_number {
    color: red;
  }
</style>