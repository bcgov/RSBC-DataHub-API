<template>
	<b-card header-tag="header" bg-variant="light" border-variant="primary" class="mx-auto p-0">
		<b-card-header class="h2" header-bg-variant="secondary" header-border-variant="dark" header-text-variant="white">            
			Notice of 24 Hour Licence Prohibition      
		</b-card-header>
		<b-card no-body v-if="dataReady" border-variant="light" bg-variant="light" class="my-0 mx-auto p-0" :key="'m12-'+updatedInfo">
			<b-row class="pt-2 pb-0 text-danger border-light">            
				<div class="ml-auto mr-2 h4">{{id}}</div>      
			</b-row>
			
			<drivers-information-card :driverInfo="twentyFourHourData" :driverState="fieldStates" @recheckStates="recheckStates()" />
			<vehicle-information-card class="mt-5" :vehicleInfo="twentyFourHourData" :vehicleState="fieldStates" @recheckStates="recheckStates()"/>
			<vehicle-owner-card class="mt-5" :ownerInfo="twentyFourHourData" :ownerState="fieldStates" @recheckStates="recheckStates()"/>
			<vehicle-impoundment-card class="mt-5" :viInfo="twentyFourHourData" :viState="fieldStates" @recheckStates="recheckStates()"/>
			<prohibition-information-card class="mt-5" :prohibitionInfo="twentyFourHourData" :prohibitionState="fieldStates" @recheckStates="recheckStates()"/>
			<reasonable-grounds-card class="mt-5" :rgInfo="twentyFourHourData" :rgState="fieldStates" @recheckStates="recheckStates()"/>		
			<test-administered-card
				class="mt-5"
				v-if="twentyFourHourData.prescribedTest" 
				:taInfo="twentyFourHourData" 
				:taState="fieldStates"
				@recheckStates="recheckStates()"/>
			<officer-details-card class="mt-5" :officerInfo="twentyFourHourData" :officerState="fieldStates" @recheckStates="recheckStates()"/>

		</b-card>
		<b-card class="mt-5">
            <b-button @click="navigateToPrintPage" variant="primary"><b style="font-size:15pt">Print All Copies</b> </b-button>
        </b-card>
  </b-card>

</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import PrintDocuments from "../PrintDocuments.vue";
import DriversInformationCard from "@/components/forms/TwentyFourHourProhibition/DriversInformationCard.vue";
import OfficerDetailsCard from "@/components/forms/TwentyFourHourProhibition/OfficerDetailsCard.vue";
import ProhibitionInformationCard from "@/components/forms/TwentyFourHourProhibition/ProhibitionInformationCard.vue";
import ReasonableGroundsCard from "@/components/forms/TwentyFourHourProhibition/ReasonableGroundsCard.vue";
import TestAdministeredCard from "@/components/forms/TwentyFourHourProhibition/TestAdministeredCard.vue";
import VehicleImpoundmentCard from "@/components/forms/TwentyFourHourProhibition/VehicleImpoundmentCard.vue";
import VehicleInformationCard from "@/components/forms/TwentyFourHourProhibition/VehicleInformationCard.vue";
import VehicleOwnerCard from "@/components/forms/TwentyFourHourProhibition/VehicleOwnerCard.vue";

import { namespace } from "vuex-class";
import "@/store/modules/common";
const commonState = namespace("Common");

import "@/store/modules/forms/mv2634";
import { asdInfoType, twentyFourHourFormDataInfoType, twentyFourHourFormJsonInfoType, twentyFourHourFormStatesInfoType } from "@/types/Forms/MV2634";
import { cityInfoType, currentlyEditingFormObjectInfoType, formsInfoType, impoundLotOperatorsInfoType, vehicleStyleInfoType } from "@/types/Common";
const mv2634State = namespace("MV2634");

@Component({
	components:{        
        DriversInformationCard,
		OfficerDetailsCard,
		PrintDocuments,
		ProhibitionInformationCard,
		ReasonableGroundsCard,
		TestAdministeredCard,
		VehicleImpoundmentCard,
		VehicleInformationCard,
		VehicleOwnerCard
    }
})
export default class TwentyFourHourProhibition extends Vue {  

	@mv2634State.State
    public mv2634Info: twentyFourHourFormJsonInfoType;
	
	@commonState.State
    public formsInfo: formsInfoType;

    @commonState.State
    public currently_editing_form_object: currentlyEditingFormObjectInfoType;

	@commonState.Action
    public UpdateCurrentlyEditingFormObject!: (newCurrentlyEditingFormObject: currentlyEditingFormObjectInfoType) => void	

	@mv2634State.Action
    public UpdateMV2634Info!: (newMV2634Info: twentyFourHourFormJsonInfoType) => void

	
	name = '24Hour'; 
	updatedInfo = 0;
    dataReady = false;
    fieldStates = {} as twentyFourHourFormStatesInfoType;

	id = '';
	movedToPrintPage = false;
	twentyFourHourFormData = {} as twentyFourHourFormJsonInfoType;
    twentyFourHourData = {} as twentyFourHourFormDataInfoType;

	variants = ["icbc", "driver", "ilo", "police"];


	mounted() {		
		this.id = this.currently_editing_form_object.form_id;
		this.clearStates();		
        const formData = this.$store.state.forms[this.name][this.id];        
        this.UpdateMV2634Info(formData);
		this.extractCurrentlyEditedFormData();
	}

	public extractCurrentlyEditedFormData() {

        //console.log(this.mv2634Info)

        if(this.mv2634Info?.data?.driversLicenceJurisdiction?.objectCd){
            //console.log('updateData')
            this.twentyFourHourFormData = this.mv2634Info            
        }else{
            //console.log('init')
            this.prepopulateDefaultValues()            
            this.recheckStates()
        }  
        this.twentyFourHourData = this.twentyFourHourFormData.data      
		this.dataReady = true;
	}

    public prepopulateDefaultValues(){
        const twentyFourHourData = {} as twentyFourHourFormDataInfoType

        twentyFourHourData.driversNumber="";
        twentyFourHourData.givenName='';
        twentyFourHourData.lastName='';
        twentyFourHourData.dob='';
        twentyFourHourData.driversLicenceJurisdiction= {"objectCd":"BC","objectDsc":"BRITISH COLUMBIA"};
        twentyFourHourData.address='';
        twentyFourHourData.driverCity='';
        twentyFourHourData.driverProvince= {"objectCd":"BC","objectDsc":"BRITISH COLUMBIA"};
        twentyFourHourData.driverPostalCode='';
        twentyFourHourData.plateProvince= {"objectCd":"BC","objectDsc":"BRITISH COLUMBIA"};
        twentyFourHourData.plateNumber='';
        twentyFourHourData.plateValTag='';
		twentyFourHourData.plateYear='';
		twentyFourHourData.puj_code= {"objectCd":"","objectDsc":""};
        twentyFourHourData.nscNumber='';
		twentyFourHourData.ownerFirstName='';
		twentyFourHourData.ownerLastName='';
		twentyFourHourData.ownerOrganization = null;
		twentyFourHourData.ownerOrganizationName='';

		twentyFourHourData.ownerAddress='';
		twentyFourHourData.ownerCity='';
		twentyFourHourData.ownerPhoneNumber='';
		twentyFourHourData.ownerPostalCode='';
		twentyFourHourData.ownerProvince= {"objectCd":"BC","objectDsc":"BRITISH COLUMBIA"};
        twentyFourHourData.registrationNumber='';        
        twentyFourHourData.vehicleYear='';
        twentyFourHourData.vehicleMake={md:'', mk:'', search:''};
        twentyFourHourData.vehicleColor=[];
		twentyFourHourData.vehicleType= {} as vehicleStyleInfoType;
		twentyFourHourData.vin_number='';

        
        twentyFourHourData.prohibitionType='';
           
        twentyFourHourData.vehicleImpounded=null; 
        twentyFourHourData.impoundLot= {} as impoundLotOperatorsInfoType;
        twentyFourHourData.locationOfKeys='';
        twentyFourHourData.notImpoundingReason='';
        twentyFourHourData.releasedDate='';
        twentyFourHourData.releasedTime='';
        twentyFourHourData.vehicleReleasedTo='';

        twentyFourHourData.offenceAddress='';
        twentyFourHourData.offenceCity = {} as cityInfoType; 
        twentyFourHourData.agencyFileNumber='';
        twentyFourHourData.prohibitionStartDate='';
        twentyFourHourData.prohibitionStartTime='';
        twentyFourHourData.agency='';
        twentyFourHourData.badge_number='';
        twentyFourHourData.officer_name='';
		twentyFourHourData.reasonableGrounds = [];
		twentyFourHourData.reasonableGroundsOther='';		

		twentyFourHourData.prescribedTest = null;
		twentyFourHourData.prescribedTestDate='';
		twentyFourHourData.prescribedTestTime='';
		twentyFourHourData.prescribedNoTestReason='';
		twentyFourHourData.alcoholTest='';
		twentyFourHourData.asd = {} as asdInfoType;
		twentyFourHourData.BacResult='';		
		twentyFourHourData.drugsTest='';
		twentyFourHourData.approvedDrugScreeningEquipment = [];        
        twentyFourHourData.submitted=false;
        
        this.twentyFourHourFormData = this.mv2634Info
        this.twentyFourHourFormData.data = twentyFourHourData
        
    }

	public clearStates(){
        const twentyFourHourFormStates = {} as twentyFourHourFormStatesInfoType;        
                
        twentyFourHourFormStates.ownerFirstName=null
		twentyFourHourFormStates.ownerLastName=null
		twentyFourHourFormStates.ownerOrganization=null
		twentyFourHourFormStates.ownerOrganizationName=null  
		twentyFourHourFormStates.ownerAddress=null
		twentyFourHourFormStates.ownerCity=null
		twentyFourHourFormStates.ownerPhoneNumber=null
		twentyFourHourFormStates.ownerPostalCode=null
		twentyFourHourFormStates.ownerProvince=null
		twentyFourHourFormStates.driversNumber=null
		twentyFourHourFormStates.givenName=null
		twentyFourHourFormStates.lastName=null
		twentyFourHourFormStates.dob=null
		twentyFourHourFormStates.driversLicenceJurisdiction=null
		twentyFourHourFormStates.address=null 
		twentyFourHourFormStates.driverCity=null
		twentyFourHourFormStates.driverProvince=null
		twentyFourHourFormStates.driverPostalCode=null
		twentyFourHourFormStates.plateProvince=null
		twentyFourHourFormStates.plateNumber=null
		twentyFourHourFormStates.plateValTag=null
		twentyFourHourFormStates.plateYear=null
		twentyFourHourFormStates.puj_code=null
		twentyFourHourFormStates.nscNumber=null
		twentyFourHourFormStates.registrationNumber=null
		twentyFourHourFormStates.vehicleYear=null
		twentyFourHourFormStates.vehicleMake=null
		twentyFourHourFormStates.vehicleColor=null
		twentyFourHourFormStates.vehicleType=null
		twentyFourHourFormStates.vin_number=null
		twentyFourHourFormStates.vehicleImpounded=null 
		twentyFourHourFormStates.impoundLotName=null
		twentyFourHourFormStates.impoundLotAddress=null
		twentyFourHourFormStates.impoundLotCity = null;
		twentyFourHourFormStates.impoundLotPhone = null;
		twentyFourHourFormStates.locationOfKeys=null
		twentyFourHourFormStates.notImpoundingReason=null
		twentyFourHourFormStates.releasedDate=null
		twentyFourHourFormStates.releasedTime=null
		twentyFourHourFormStates.vehicleReleasedTo=null    
		twentyFourHourFormStates.offenceAddress=null
		twentyFourHourFormStates.offenceCity=null
		twentyFourHourFormStates.agencyFileNumber=null
		twentyFourHourFormStates.prohibitionStartDate=null
		twentyFourHourFormStates.prohibitionStartTime=null
		twentyFourHourFormStates.agency=null
		twentyFourHourFormStates.badgeNumber=null
		twentyFourHourFormStates.officerName=null
		twentyFourHourFormStates.submitted=null
		twentyFourHourFormStates.reasonableGrounds=null
		twentyFourHourFormStates.reasonableGroundsOther=null  
		twentyFourHourFormStates.prescribedTest=null
		twentyFourHourFormStates.prescribedTestDate=null
		twentyFourHourFormStates.prescribedTestTime=null
		twentyFourHourFormStates.prescribedNoTestReason=null    
		twentyFourHourFormStates.prohibitionType=null    
		twentyFourHourFormStates.alcoholTest=null
		twentyFourHourFormStates.asdExpiryDate=null
		twentyFourHourFormStates.asdResult=null
		twentyFourHourFormStates.BacResult=null   
		twentyFourHourFormStates.drugsTest=null
		twentyFourHourFormStates.approvedDrugScreeningEquipment=null    

        this.fieldStates = twentyFourHourFormStates;
        this.dataReady = true
    }

	public recheckStates(){
        this.UpdateMV2634Info(this.twentyFourHourFormData)
        this.$store.commit("updateFormInRoot",this.twentyFourHourFormData)
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
        const data = this.twentyFourHourFormData.data


        //__Driver's Information
        this.fieldStates.driversNumber = data.driversNumber? null:false;
        this.fieldStates.lastName = data.lastName? null:false;
        if(!data.dob) this.fieldStates.dob = false;
        this.fieldStates.address = data.address? null:false;
        this.fieldStates.driverCity = data.driverCity? null:false;
        this.fieldStates.driverProvince = data.driverProvince?.objectCd? null:false;

		if(data.driverPostalCode)
            this.fieldStates.driverPostalCode = Vue.filter('verifyPostCode')(data.driverPostalCode, data.driverProvince?.objectCd)? null:false;      
        else 
            this.fieldStates.driverPostalCode = null;

		//__Vehicle information
		this.fieldStates.plateProvince = data.plateProvince?.objectCd? null:false;
        this.fieldStates.plateNumber = data.plateNumber? null:false;


		//__Registered Owner
        if(data.ownerPhoneNumber) 
            this.fieldStates.ownerPhoneNumber = Vue.filter('verifyPhone')( data.ownerPhoneNumber)? null:false;
        else 
            this.fieldStates.ownerPhoneNumber = null;
        
        if(data.ownerPostalCode)
            this.fieldStates.ownerPostalCode = Vue.filter('verifyPostCode')(data.ownerPostalCode, data.ownerProvince?.objectCd)? null:false;      
        else 
            this.fieldStates.ownerPostalCode = null;

        //__Vehicle Impoundment or Disposition
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

		//__Reasonable Grounds
		this.fieldStates.reasonableGroundsOther = (data.reasonableGrounds?.includes('Other') && !data.reasonableGroundsOther)? false: null
		if(data.prescribedTest==true && !data.prescribedTestDate) this.fieldStates.prescribedTestDate = false
		if(data.prescribedTest==true && !data.prescribedTestTime) this.fieldStates.prescribedTestTime = false
		if(!data.prescribedTest){
            this.fieldStates.prescribedTestTime=null;
            this.fieldStates.prescribedTestDate=null;        
        }

		//__Test Administered
		//Alcohol 215(2)
		this.fieldStates.BacResult = (data.prescribedTest==true &&
			data.prohibitionType=='Alcohol' &&
			data.alcoholTest.includes('Approved Instrument') && 
			!data.BacResult)? false: null;

		this.fieldStates.asdExpiryDate = (data.prescribedTest==true &&
			data.prohibitionType=='Alcohol' &&
			data.alcoholTest.includes('Alco-Sensor FST (ASD)') && 
			!data.asd?.expiryDate)? false: null;

		//__Officer
        this.fieldStates.agency = data.agency? null : false;


        for(const field of Object.keys(this.fieldStates)){
            if(this.fieldStates[field]==false){
                if(finalCheck) Vue.filter('findInvalidFields')()
                return false
            }                
        }       

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