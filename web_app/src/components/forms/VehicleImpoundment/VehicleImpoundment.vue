<template>
<!-- 
			<form-card title="Generate PDF for Printing">
			<div class="d-flex">
				<print-documents
				v-for="(document, index) in getDocumentsToPrint(name)" v-bind:key="index"
				:form_object="getCurrentlyEditedFormInfo"
				:validate="validate"
				:variants="document.variants">
				{{ document.name }}
				</print-documents>
			</div>
			</form-card>-->

	<b-card header-tag="header" bg-variant="light" border-variant="primary" class="mx-auto p-0">
		<b-card-header header-bg-variant="secondary" header-border-variant="dark" header-text-variant="white">            
			<h4>Vehicle Impoundment</h4>      
		</b-card-header>
		<b-card no-body v-if="dataReady" border-variant="light" bg-variant="light" class="my-0 mx-auto p-0" :key="'m12-'+updatedInfo">
			<b-row class="pt-2 pb-0 text-danger border-light">            
				<div class="ml-auto mr-2 h4">{{id}}</div>      
			</b-row>
			
			<drivers-information-card :driverInfo="viData" :driverState="fieldStates" @recheckStates="recheckStates()" />
			<vehicle-information-card :vehicleInfo="viData" :vehicleState="fieldStates" @recheckStates="recheckStates()"/>
			<vehicle-owner-card :ownerInfo="viData" :ownerState="fieldStates" @recheckStates="recheckStates()"/>
			<impound-lot-card :ilInfo="viData" :ilState="fieldStates" @recheckStates="recheckStates()"/>
			<reasonable-grounds-card :rgInfo="viData" :rgState="fieldStates" @recheckStates="recheckStates()"/>		
			<excessive-speed-card
				v-if="viData.impoundReason.includes('Excessive Speed')" 
				:esInfo="viData" 
				:esState="fieldStates"
				@recheckStates="recheckStates()"/>
			<immediate-roadside-prohibition-card :irpInfo="viData" :irpState="fieldStates" @recheckStates="recheckStates()"/>		
			<linkage-card :linkageInfo="viData" :linkageState="fieldStates" @recheckStates="recheckStates()"/>		
			<incident-details-card :incidentInfo="viData" :incidentState="fieldStates" @recheckStates="recheckStates()"/>
			<officer-details-card :officerInfo="viData" :officerState="fieldStates" @recheckStates="recheckStates()"/>

		</b-card>
		<b-card class="mt-5">
            <b-button @click="navigateToPrintPage" variant="primary"><b style="font-size:15pt">Print All Copies</b> </b-button>
        </b-card>

	</b-card>
	
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import PrintDocuments from "../PrintDocuments.vue";
import DriversInformationCard from "@/components/forms/VehicleImpoundment/DriversInformationCard.vue";
import OfficerDetailsCard from "@/components/forms/VehicleImpoundment/OfficerDetailsCard.vue";
import VehicleInformationCard from "@/components/forms/VehicleImpoundment/VehicleInformationCard.vue";
import VehicleOwnerCard from "@/components/forms/VehicleImpoundment/VehicleOwnerCard.vue";
import ImpoundLotCard from "@/components/forms/VehicleImpoundment/ImpoundLotCard.vue";
import ReasonableGroundsCard from "@/components/forms/VehicleImpoundment/ReasonableGroundsCard.vue";
import ExcessiveSpeedCard from "@/components/forms/VehicleImpoundment/ExcessiveSpeedCard.vue";
import LinkageCard from "@/components/forms/VehicleImpoundment/LinkageCard.vue";
import IncidentDetailsCard from "@/components/forms/VehicleImpoundment/IncidentDetailsCard.vue";
import ImmediateRoadsideProhibitionCard from "@/components/forms/VehicleImpoundment/ImmediateRoadsideProhibitionCard.vue";


import { namespace } from "vuex-class";

import "@/store/modules/common";
const commonState = namespace("Common");

import "@/store/modules/forms/vi";
const viState = namespace("VI");


import { viFormDataInfoType, viFormJsonInfoType, viFormStatesInfoType } from "@/types/Forms/VI";
import { cityInfoType, currentlyEditingFormObjectInfoType, formsInfoType, impoundLotOperatorsInfoType } from "@/types/Common";


@Component({
	components: {
		ImmediateRoadsideProhibitionCard,
		IncidentDetailsCard,
		LinkageCard,
		ExcessiveSpeedCard,
		ReasonableGroundsCard,
		ImpoundLotCard,
		DriversInformationCard,
		OfficerDetailsCard,
		VehicleInformationCard,
		VehicleOwnerCard,
		PrintDocuments
	}
})
export default class VehicleImpoundment extends Vue {  

	@viState.State
    public viInfo: viFormJsonInfoType;
	
	@commonState.State
    public formsInfo: formsInfoType;

    @commonState.State
    public currently_editing_form_object: currentlyEditingFormObjectInfoType;

	@commonState.Action
    public UpdateCurrentlyEditingFormObject!: (newCurrentlyEditingFormObject: currentlyEditingFormObjectInfoType) => void	

	@viState.Action
    public UpdateVIInfo!: (newVIInfo: viFormJsonInfoType) => void
	
	name = 'VI'; 
	updatedInfo = 0;
    dataReady = false;
    fieldStates = {} as viFormStatesInfoType;

	id = '';
	movedToPrintPage = false;
	viFormData = {} as viFormJsonInfoType;
    viData = {} as viFormDataInfoType;

	variants = ["driver", "police", "ilo", "report"];

	mounted() {		
		this.id = this.currently_editing_form_object.form_id;
		this.clearStates();		
        const formData = this.$store.state.forms[this.name][this.id];        
        this.UpdateVIInfo(formData);
		this.extractCurrentlyEditedFormData();
	}

	public extractCurrentlyEditedFormData() {

        //console.log(this.viInfo)

        if(this.viInfo?.data?.driversLicenceJurisdiction?.objectCd){
            //console.log('updateData')
            this.viFormData = this.viInfo            
        }else{
            //console.log('init')
            this.prepopulateDefaultValues()            
            this.recheckStates()
        }  
        this.viData = this.viFormData.data      
		this.dataReady = true;
	}

    public prepopulateDefaultValues(){
        const viData = {} as viFormDataInfoType

        viData.driversNumber=null;
        viData.givenName='';
        viData.lastName='';
        viData.dob='';
        viData.driversLicenceJurisdiction= {"objectCd":"BC","objectDsc":"BRITISH COLUMBIA"};
        viData.plateProvince= {"objectCd":"BC","objectDsc":"BRITISH COLUMBIA"};
        viData.plateNumber='';
		viData.ownerFirstName='';
		viData.ownerLastName='';
		viData.ownerOrganization = null;
		viData.ownerOrganizationName='';
		viData.ownerDob = '';
		viData.ownerAddress='';
		viData.ownerCity='';
		viData.ownerEmail = '';
		viData.ownerPhoneNumber='';
		viData.ownerPostalCode='';
		viData.ownerProvince= {"objectCd":"BC","objectDsc":"BRITISH COLUMBIA"};
        viData.driverIsOwner = null;
		viData.dlClass = '';
		viData.driver_gender = ''; 		
		viData.dlExpiryYear = '';
		viData.registrationNumber='';        
        viData.vehicleYear='';
        viData.vehicleMake={md:'', mk:'', search:''};
        viData.vehicleColor=[];		
		viData.vin_number=''; 
        viData.impoundLot= {} as impoundLotOperatorsInfoType;
        viData.impoundedDate = '';
		viData.incidentDetails=''; 
        viData.offenceAddress='';
        viData.offenceCity = {} as cityInfoType; 
        viData.agencyFileNumber='';
        viData.prohibitionStartDate='';
        viData.prohibitionStartTime='';
        viData.agency='';
        viData.badge_number='';
        viData.officer_name='';	
		viData.isNSC = null;
		viData.irp = null;
		viData.iprNumber='';
		viData.irpType='';
		viData.keyLinkageLocation='';
		viData.unlicensedProhibitionNumber='';
		viData.unlicensedBcResident = null;
		viData.speedLimit = '';
		viData.vehicleSpeed = '';
		viData.excessiveSpeedEstimationType='';		
		viData.excessiveSpeedConfirmationType='';
		viData.linkage = [];   
		viData.impoundReason = [];     
        viData.submitted=false;
        
        this.viFormData = this.viInfo;
        this.viFormData.data = viData;
        
    }

	public clearStates(){
        const viFormStates = {} as viFormStatesInfoType;        
                
        viFormStates.ownerFirstName=null;
		viFormStates.ownerLastName=null;
		viFormStates.ownerDob=null;
		viFormStates.ownerOrganization=null;
		viFormStates.ownerOrganizationName=null;  
		viFormStates.ownerAddress=null;
		viFormStates.ownerCity=null;
		viFormStates.ownerEmail=null;
		viFormStates.ownerPhoneNumber=null;
		viFormStates.ownerPostalCode=null;
		viFormStates.ownerProvince=null;
		viFormStates.driverIsOwner=null; 
		viFormStates.dlClass=null;
		viFormStates.driver_gender=null;
		viFormStates.driversNumber=null;
		viFormStates.dlExpiryYear=null;
		viFormStates.givenName=null;
		viFormStates.lastName=null;
		viFormStates.dob=null;
		viFormStates.driversLicenceJurisdiction=null;		
		viFormStates.plateProvince=null;
		viFormStates.plateNumber=null;	
		viFormStates.registrationNumber=null;
		viFormStates.vehicleYear=null;
		viFormStates.vehicleMake=null;
		viFormStates.vehicleColor=null;		
		viFormStates.vin_number=null;		
		viFormStates.impoundLotName=null;
		viFormStates.impoundLotAddress=null;
		viFormStates.impoundLotCity=null;
		viFormStates.impoundLotPhone=null;
		viFormStates.impoundedDate=null;
		viFormStates.incidentDetails=null;
		viFormStates.offenceAddress=null;
		viFormStates.offenceCity=null;
		viFormStates.agencyFileNumber=null;
		viFormStates.prohibitionStartDate=null;
		viFormStates.prohibitionStartTime=null;
		viFormStates.agency=null;
		viFormStates.badge_number=null;
		viFormStates.officer_name=null;
		viFormStates.submitted=null;
		viFormStates.isNSC=null;
		viFormStates.irp=null;
		viFormStates.iprNumber=null;
		viFormStates.irpType=null;
		viFormStates.linkage=null;
		viFormStates.keyLinkageLocation=null;
		viFormStates.impoundReason=null; 
		viFormStates.speedLimit = null;
		viFormStates.vehicleSpeed = null;
		viFormStates.excessiveSpeedConfirmationType=null;
		viFormStates.excessiveSpeedEstimationType=null;
		viFormStates.unlicensedBcResident=null;
		viFormStates.unlicensedProhibitionNumber=null;   

        this.fieldStates = viFormStates;
        this.dataReady = true
    }

	public recheckStates(){
        this.UpdateVIInfo(this.viFormData)
        this.$store.commit("updateFormInRoot",this.viFormData)
        console.log('check')			
        const specialFields = ['dob']
        for(const field of Object.keys(this.fieldStates)){
            if(this.fieldStates[field]==false && !specialFields.includes(field)){
                this.checkStates()
                return 
            }
        }  
    }

	public checkStates(){
        const data = this.viFormData.data
        
        
        for(const field of Object.keys(this.fieldStates)){
            if(this.fieldStates[field]==false){
                // Vue.filter('findInvalidFields')()
                return false
            }                
        }       

        return true;            
    }

	public navigateToPrintPage(){
        if(this.checkStates()){
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