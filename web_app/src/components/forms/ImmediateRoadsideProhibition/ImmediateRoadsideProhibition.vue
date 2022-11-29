<template>  
	<b-card header-tag="header" bg-variant="light" border-variant="primary" class="mx-auto p-0">
		<b-card-header header-bg-variant="secondary" header-border-variant="dark" header-text-variant="white">            
			<h4>Immediate Roadside Prohibition</h4>      
		</b-card-header>
		<b-card no-body v-if="dataReady" border-variant="light" bg-variant="light" class="my-0 mx-auto p-0" :key="'m12-'+updatedInfo">
			<b-row class="pt-2 pb-0 text-danger border-light">            
				<div class="ml-auto mr-2 h4">{{id}}</div>      
			</b-row>
			
			<drivers-information-card :driverInfo="irpData" :driverState="fieldStates" @recheckStates="recheckStates()" />
			<prohibition-information-card :prohibitionInfo="irpData" :prohibitionState="fieldStates" @recheckStates="recheckStates()"/>
			<vehicle-impoundment-card :viInfo="irpData" :viState="fieldStates" @recheckStates="recheckStates()"/>
			<dl-seized-card :dsInfo="irpData" :dsState="fieldStates" @recheckStates="recheckStates()"/>			
			<officer-details-card :officerInfo="irpData" :officerState="fieldStates" @recheckStates="recheckStates()"/>

		</b-card>

  </b-card>

</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import PrintDocuments from "../PrintDocuments.vue";
import DriversInformationCard from "@/components/forms/ImmediateRoadsideProhibition/DriversInformationCard.vue";
import OfficerDetailsCard from "@/components/forms/ImmediateRoadsideProhibition/OfficerDetailsCard.vue";
import ProhibitionInformationCard from "@/components/forms/ImmediateRoadsideProhibition/ProhibitionInformationCard.vue";
import VehicleImpoundmentCard from "@/components/forms/ImmediateRoadsideProhibition/VehicleImpoundmentCard.vue";
import DlSeizedCard from "@/components/forms/ImmediateRoadsideProhibition/DlSeizedCard.vue";

import { namespace } from "vuex-class";
import "@/store/modules/common";
const commonState = namespace("Common");

import "@/store/modules/forms/irp";
import { irpFormDataInfoType, irpFormJsonInfoType, irpFormStatesInfoType } from "@/types/Forms/IRP";
import { cityInfoType, currentlyEditingFormObjectInfoType, formsInfoType } from "@/types/Common";
const irpState = namespace("IRP");

@Component({
	components:{        
        DriversInformationCard,
		OfficerDetailsCard,
		PrintDocuments,
		ProhibitionInformationCard,
		VehicleImpoundmentCard,
        DlSeizedCard
		
    }
})
export default class ImmediateRoadsideProhibition extends Vue {  

	@irpState.State
    public irpInfo: irpFormJsonInfoType;
	
	@commonState.State
    public formsInfo: formsInfoType;

    @commonState.State
    public currently_editing_form_object: currentlyEditingFormObjectInfoType;

	@commonState.Action
    public UpdateCurrentlyEditingFormObject!: (newCurrentlyEditingFormObject: currentlyEditingFormObjectInfoType) => void	

	@irpState.Action
    public UpdateIRPInfo!: (newIRPInfo: irpFormJsonInfoType) => void

	
	name = 'IRP'; 
	updatedInfo = 0;
    dataReady = false;
    fieldStates = {} as irpFormStatesInfoType;

	id = '';
	movedToPrintPage = false;
	irpFormData = {} as irpFormJsonInfoType;
    irpData = {} as irpFormDataInfoType;

	variants = ["police", "driver", "report" ];

	mounted() {		
		this.id = this.currently_editing_form_object.form_id;
		this.clearStates();		
        const formData = this.$store.state.forms[this.name][this.id];        
        this.UpdateIRPInfo(formData);
		this.extractCurrentlyEditedFormData();
	}

	public extractCurrentlyEditedFormData() {

        //console.log(this.irpInfo)

        if(this.irpInfo?.data?.driversLicenceJurisdiction?.objectCd){
            //console.log('updateData')
            this.irpFormData = this.irpInfo            
        }else{
            //console.log('init')
            this.prepopulateDefaultValues()            
            this.recheckStates()
        }  
        this.irpData = this.irpFormData.data      
		this.dataReady = true;
	}

    public prepopulateDefaultValues(){
        const irpData = {} as irpFormDataInfoType

        irpData.driversNumber=null;
        irpData.givenName='';
        irpData.lastName='';
		irpData.driverGender='';
		irpData.licenseExpiryYear='';
		irpData.bcdlClass='';
        irpData.dob='';
        irpData.driversLicenceJurisdiction= {"objectCd":"BC","objectDsc":"BRITISH COLUMBIA"};
        irpData.address='';
        irpData.driverCity='';
        irpData.driverProvince= {"objectCd":"BC","objectDsc":"BRITISH COLUMBIA"};
        irpData.driverPostalCode='';
		irpData.vehicleImpounded=null; 
		irpData.viNumber='';
        irpData.dlSeized=null;
        irpData.offenceAddress='';
        irpData.offenceCity = {} as cityInfoType;         
        irpData.prohibitionStartDate='';
        irpData.prohibitionStartTime='';
		irpData.prohibitionTypePeriod='';
        irpData.agency='';
        irpData.badge_number='';
        irpData.officer_name='';
		irpData.submitted=false;
        
        this.irpFormData = this.irpInfo
        this.irpFormData.data = irpData
        
    }

	public clearStates(){
        const irpFormStates = {} as irpFormStatesInfoType;
		irpFormStates.driversNumber=null
		irpFormStates.givenName=null
		irpFormStates.lastName=null
		irpFormStates.driverGender=null
        irpFormStates.licenseExpiryYear=null
        irpFormStates.bcdlClass=null
		irpFormStates.dob=null
		irpFormStates.driversLicenceJurisdiction=null
		irpFormStates.address=null 
		irpFormStates.driverCity=null
		irpFormStates.driverProvince=null
		irpFormStates.driverPostalCode=null		
		irpFormStates.vehicleImpounded=null 
        irpFormStates.viNumber=null
        irpFormStates.dlSeized=null		
		irpFormStates.offenceAddress=null
		irpFormStates.offenceCity=null		
		irpFormStates.prohibitionStartDate=null
		irpFormStates.prohibitionStartTime=null
        irpFormStates.prohibitionTypePeriod=null
		irpFormStates.agency=null
		irpFormStates.badge_number=null
		irpFormStates.officer_name=null
		irpFormStates.submitted=null		

        this.fieldStates = irpFormStates;
        this.dataReady = true
    }

	public recheckStates(){
        this.UpdateIRPInfo(this.irpFormData)
        this.$store.commit("updateFormInRoot",this.irpFormData)
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
        const data = this.irpFormData.data
        
        this.fieldStates.driverProvince = data.driverProvince?.objectCd? null:false;
        this.fieldStates.driverPostalCode = Vue.filter('verifyPostCode')(data.driverPostalCode, data.driverProvince?.objectCd)? null:false;      

        for(const field of Object.keys(this.fieldStates)){
            if(this.fieldStates[field]==false){
                // Vue.filter('findInvalidFields')()
                return false
            }                
        }       

        return true;            
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