<template>

	<b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light">
		<b-card-header header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b>Vehicle information</b>      
		</b-card-header>
		<b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">
			<b-row>
				<b-col cols="3" class="pl-1">
					<label class="ml-0 m-0 p-0"> Jurisdiction </label>
					<b-form-select		
						v-model="vehicleInfo.plateProvince"
						@change="update"
						:disabled="formPrinted"
						:state="vehicleState.plateProvince"
						placeholder="Search for a Jurisdiction"
						style="display: block;">
							<b-form-select-option
								v-for="jurisdiction,inx in jurisdictions" 
								:key="'plt-jurisdiction-'+jurisdiction.objectCd+inx"
								:value="jurisdiction">
									{{jurisdiction.objectDsc}}
							</b-form-select-option>    
					</b-form-select>                          
				</b-col>
				<b-col class="pr-2" cols="4">
					<label class="ml-1 m-0 p-0"> Plate Number</label>
					<b-form-input
						v-model="vehicleInfo.plateNumber"
						:disabled="formPrinted"
                        :state="vehicleState.plateNumber"
						@change="update"
						placeholder="Plate">
					</b-form-input>                                
				</b-col>
				<b-col class="p-0 pt-1" cols="1">
					<b-button 
						class="bg-primary text-white mt-4"
						style="opacity:1;"
						:disabled="formPrinted || !displayIcbcPlateLookup"
						@click="triggerPlateLookup">
						<spinner 
							color="#FFF" 
							v-if="searchingLookup" 
							style="margin:0; padding: 0; transform:translate(-12px,-22px);"/>
						<b style="font-size: 0.875rem;">ICBC Prefill</b>
					</b-button>  
				</b-col>
			</b-row>	
			<b-row>
				<b-col >
					<label class="ml-1 m-0 p-0"> Vehicle Year </label>
					<b-form-select	
						v-model="vehicleInfo.vehicleYear"
						:disabled="formPrinted"
						@change="update"
						:state="vehicleState.vehicleYear"							
						placeholder="Select a vehicle year"
						style="display: block;">
							<b-form-select-option
								v-for="year in vehicleYears" 
								:key="year"
								:value="year">
									{{year}}
							</b-form-select-option>    
					</b-form-select>                                
				</b-col>
				<b-col >
					<label class="ml-1 m-0 p-0"> Vehicle Make and Model </label>
					<b-form-select	
						v-model="vehicleInfo.vehicleMake"
						:disabled="formPrinted"
						@change="update"
						:state="vehicleState.vehicleMake"							
						placeholder="Search for a vehicle make and model"
						style="display: block;">
							<b-form-select-option
								v-for="vehicle,inx in vehicles" 
								:key="vehicle.md+inx"
								:value="vehicle">
									{{vehicle.search}}
							</b-form-select-option>    
					</b-form-select>  
				</b-col>
				
				<b-col >
					<label class="ml-1 m-0 p-0"> Vehicle Colour(s)</label>
					<b-form-select	
						multiple
						v-model="vehicleInfo.vehicleColor"
						:disabled="formPrinted"
						@change="update"
						:state="vehicleState.vehicleColor"							
						placeholder="Search for a car colour"
						style="display: block;">
							<b-form-select-option
								v-for="colour,inx in vehicleColours" 
								:key="'color-code-'+colour.code+inx"
								:value="colour">
									{{colour.display_name}}
							</b-form-select-option>    
					</b-form-select>                                 
				</b-col>
			</b-row>
			<b-row>	
				<b-col cols="4">
					<label class="ml-1 m-0 p-0"> Registration Number</label>
					<b-form-input						
						v-model="vehicleInfo.registrationNumber"						
						:disabled="formPrinted"
                        :state="vehicleState.registrationNumber"
						@change="update">
					</b-form-input>                                
				</b-col>
				<b-col cols="2">
					<b-form-checkbox						
						v-model="vehicleInfo.isNSC"						
						:disabled="formPrinted"
                        :state="vehicleState.isNSC"
						@change="update">NSC?
					</b-form-checkbox>                             
				</b-col>
				<b-col cols="6">
					<label class="ml-1 m-0 p-0"> Vehicle Identification Number (VIN)</label>
					<b-form-input
						:class="vehicleInfo.vin_number.length > 20?'is-invalid':''"
						v-model="vehicleInfo.vin_number"						
						:disabled="formPrinted"
                        :state="vehicleState.vin_number"
						@change="update">
					</b-form-input>
					<div 
						v-if="vehicleInfo.vin_number.length > 20" 
						style="font-size:10pt;" 
						class="text-danger text-left m-0 mt-n p-0">
						The VIN number cannot exceed 20 characters.
					</div>					                             
				</b-col>	
				
			</b-row>	
			<div class="fade-out alert alert-danger mt-4" v-if="error">{{error}}</div>			
		</b-card>	

	</b-card>
</template>


<script lang="ts">

import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace } from "vuex-class";

import "@/store/modules/common";
const commonState = namespace("Common");

import "@/store/modules/forms/vi";
const viState = namespace("VI");

import { jurisdictionInfoType, provinceInfoType, vehicleColourInfoType, vehicleInfoType } from '@/types/Common';
import { viFormStatesInfoType, viFormDataInfoType, viFormJsonInfoType } from '@/types/Forms/VI';
import Spinner from "@/components/utils/Spinner.vue";
import { lookupPlateFromICBC } from '@/utils/icbc';
import {getArrayOfVehicleYears, getArrayOfPlateYears} from "@/utils/vehicle";

@Component({
    components: {           
        Spinner
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
    public vehicleColours: vehicleColourInfoType[];	

	@viState.State
    public viInfo: viFormJsonInfoType;

	@Prop({required: true})
    vehicleInfo!: viFormDataInfoType;
	
	@Prop({required: true})
	vehicleState!: viFormStatesInfoType;

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
	plateYears = [];


	mounted() { 
        this.dataReady = false;
		this.formPrinted = Boolean(this.viInfo.printed_timestamp);
        this.extractFields();
        this.dataReady = true;
    }

	public extractFields(){		
		this.path = 'forms/' + this.viInfo.form_type + '/' + this.viInfo.form_id + '/data';
		this.vehicleYears = getArrayOfVehicleYears();
		this.plateYears = getArrayOfPlateYears();
	}

	public triggerPlateLookup(){		
		this.error = ''
		this.searchingLookup = true;
		lookupPlateFromICBC([this.viInfo.data.plateNumber, this.path ])
			.then(() => {
				const data = this.$store.state.forms['12Hour'][this.viInfo.form_id] //TODO: get this 'data' from ICBC
				this.updateFormFields(data);
				this.searchingLookup = false;
			})
			.catch( error => {
				console.log("error", error)
				this.searchingLookup = false;
				this.error = error.description;
			})
	}

	public updateFormFields(data: any){

		this.vehicleInfo.registrationNumber = data['registrationNumber'];
		this.vehicleInfo.vehicleYear = data['vehicleModelYear'];		
        this.vehicleInfo.vehicleColor = [{code: data['vehicleColour'], display_name: data['vehicleColour'], colour_class: data['vehicleColour']}];
		//TODO: fix color info fields
		this.vehicleInfo.vehicleMake = {
			"md": data['vehicleMake'], 
			"mk": data['vehicleModel'], 
			"search": data['vehicleMake'] + " - " + data['vehicleModel']};	
			
		this.vehicleInfo.vin_number = data['vehicleIdNumber'];
		
		const owner = data['vehicleParties'][0]['party'];
        const address = owner['addresses'][0];

        if(owner.partyType === 'Organisation') {
			this.vehicleInfo.ownerOrganization = true;
            this.vehicleInfo.ownerOrganizationName = owner['orgName'];
        } else {
            this.vehicleInfo.ownerOrganization = false;
            this.vehicleInfo.ownerLastName = owner['lastName'];
            this.vehicleInfo.ownerFirstName = owner['firstName'];
        }

		this.vehicleInfo.driverIsOwner = data["owner_is_driver"]///verify this

		this.vehicleInfo.ownerAddress = address['addressLine1'];
        this.vehicleInfo.ownerCity = address['city'];
		this.vehicleInfo.ownerProvince = address['region'];
        this.vehicleInfo.ownerPostalCode = address['postalCode'];	
	}

	public update(){     
        this.recheckStates()
    }

	public recheckStates(){
        this.$emit('recheckStates')
    }

	get displayIcbcPlateLookup(){
        return this.vehicleInfo.plateProvince.objectCd == "BC" && this.$store.state.isUserAuthorized;
    }

 
}
</script>

<style scoped lang="scss">

	input.is-invalid {
		background: #ebc417;
	}
	select.is-invalid {
		background: #ebc417;
		option {
			background: #FFF;
		}
	}

	.fade-out {
		animation: fadeOut ease 8s;
		-webkit-animation: fadeOut ease 8s;
		-moz-animation: fadeOut ease 8s;
		-o-animation: fadeOut ease 8s;
		-ms-animation: fadeOut ease 8s;
	}
	@keyframes fadeOut {
		0% {
			opacity:1;
		}
		100% {
			opacity:0;
		}
	}

	@-moz-keyframes fadeOut {
		0% {
			opacity:1;
		}
		100% {
			opacity:0;
		}
	}

	@-webkit-keyframes fadeOut {
		0% {
			opacity:1;
		}
		100% {
			opacity:0;
		}
	}

	@-o-keyframes fadeOut {
		0% {
			opacity:1;
		}
		100% {
			opacity:0;
		}
	}

	@-ms-keyframes fadeOut {
		0% {
			opacity:1;
		}
		100% {
			opacity:0;
		}
	}

</style>