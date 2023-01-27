<template>
	<b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
		<b-card-header header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b>Driver's Information</b>      
		</b-card-header>
		<b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">

			<b-row>
				<b-col class="pr-1" cols="3">
					<b-form-group>
					<label class="m-0 p-0"> Driver's Licence Number</label>
					<b-form-input
						v-model="driverInfo.driversNumber"
						:disabled="formPrinted"
                        :state="driverState.driversNumber"
						@input="update"
						placeholder="Driver's Licence Number">
					</b-form-input> 
					</b-form-group>                             
				</b-col>
				<b-col class="p-0 pt-1" cols="1">
					<b-button 
						class="bg-primary text-white"
						style="opacity:1; float:left; margin-top:1.42rem;"
						:disabled="formPrinted || !displayIcbcLicenceLookup"
						@click="triggerDriversLookup">
						<spinner color="#FFF" v-if="searchingLookup" style="margin:0; padding: 0; transform:translate(-12px,-22px);"/>
						<span style="font-size: 0.875rem;" v-else>ICBC Prefill</span>
					</b-button>  
				</b-col>
				<b-col class="p-0 pt-1" cols="1">
					<b-button 
						class="bg-primary text-white"
						style="opacity:1; float:right; margin-top:1.42rem;"
						@click="launchDlScanner">
						<spinner color="#FFF" v-if="searchingDl" style="margin:0; padding: 0; transform:translate(-12px,-22px);"/>
						<span style="font-size: 0.875rem;" v-else>Scan DL</span>
					</b-button>  
				</b-col>
				<b-col cols="3" class=" pl-1">
					<label class="ml-0 m-0 p-0"> Prov / State / International </label>
					<b-form-select	
						v-model="driverInfo.driversLicenceJurisdiction"
						@change="update"
						:disabled="formPrinted"
						:state="driverState.driversLicenceJurisdiction"						
						placeholder="Search for a Jurisdiction"
						style=" ">
							<b-form-select-option
								v-for="jurisdiction,inx in jurisdictions" 
								:key="'dr-jurisdiction-'+jurisdiction.objectCd+inx"
								:value="jurisdiction">
									{{jurisdiction.objectDsc}}
							</b-form-select-option>    
					</b-form-select>                          
				</b-col>
			</b-row>
			<b-row>
				<b-col >
					<label class="ml-1 m-0 p-0"> Surname <span class="text-danger">*</span></label>
					<b-form-input
						placeholder="Last Name"
						v-model="driverInfo.lastName"
						:disabled="formPrinted"
						@input="update"
						:state="driverState.lastName">
					</b-form-input>                                
				</b-col>
				<b-col >
					<label class="ml-1 m-0 p-0"> Given Names </label>
					<b-form-input
						placeholder="Given Names"
						v-model="driverInfo.givenName"
						:disabled="formPrinted"
						@input="update"
						:state="driverState.givenName">
					</b-form-input>  
				</b-col>
				<b-col >
					<label class="ml-1 m-0 p-0"> Date of Birth <span class="text-muted" style="font-size: 9pt;">YYYYMMDD ({{age}} yrs)</span></label>
					
					<b-input-group class="mb-3">
						<b-form-input
							:key="updateDate"
							id="dob"
							v-model="driverInfo.dob"
							type="text"
							@input="validateDate(false)"
							:disabled="formPrinted"
							:state="driverState.dob"
							placeholder="YYYYMMDD"
							autocomplete="off"
						></b-form-input>
						<b-input-group-append>
							<b-form-datepicker
								v-model="dob"
								:disabled="formPrinted"
								button-only
								right
								:allowed-dates="allowedDates"
								locale="en-US"
								aria-controls="dob"
								@context="validateDate(true)"
							></b-form-datepicker>
						</b-input-group-append>
					</b-input-group> 
					<div v-if="dateError" style="font-size:10pt;" class="text-danger text-left m-0 mt-n3 p-0">{{dateError}}</div>                             
				</b-col>
			</b-row>			
			<b-row>
				<b-col cols="6" >
					<label class="ml-1 m-0 p-0">Gender</label>
					<b-form-select	
						v-model="driverInfo.driver_gender"
						:disabled="formPrinted"
						@change="update"
						:state="driverState.driver_gender"
						style="display: block;">
							<b-form-select-option
								v-for="gender,inx in genderOptions" 
								:key="'dr-gender-'+gender.value+inx"
								:value="gender.value">
									{{gender.text}}
							</b-form-select-option>    
					</b-form-select>                                
				</b-col>
				<b-col cols="2">
					<label class="ml-1 m-0 p-0"> License Expiry Year</label>
					<b-form-input
						placeholder="YYYY"				
						v-model="driverInfo.dlExpiryYear"						
						@input="update"
						:disabled="formPrinted"
						:state="driverState.dlExpiryYear">
					</b-form-input>   
				</b-col>
				<b-col v-if="driverInfo.driversLicenceJurisdiction.objectCd == 'BC'">
					<label class="ml-1 m-0 p-0"> BCDL Class</label>
					<b-form-input	
						type="number"					
						v-model="driverInfo.dlClass"						
						@input="update"
						:disabled="formPrinted"
						:state="driverState.dlClass">
					</b-form-input>                  
				</b-col>
			</b-row>
			<div class="fade-out alert alert-danger mt-4" v-if="error">{{error}}</div>			
		</b-card>

		<b-modal v-model="showScannerMessage" id="bv-modal-scanner" header-class="bg-warning text-light">            
			<template v-slot:modal-title>					               
				<h2 class="mb-0 text-light"> Driver's Licence Scanner </h2>                                 
			</template>
			<div v-if="scannerOpened">
				<div>Please scan the BC Driver's licence</div>
				<br />
				<b-spinner></b-spinner>

			</div>
			<div class="alert-warning pt-2 pb-2" v-if=" ! scannerOpened">
				<div>Requesting access to the scanner</div>
				<div class="small">
					{{ scannerMessage }}
				</div>
			</div>
			<template v-slot:modal-footer>
				<b-button 
					variant="primary" 
					@click="closeScannner()">
					Cancel
				</b-button>
			</template>            
			<template v-slot:modal-header-close>                 
				<b-button variant="outline-warning" class="text-light closeButton" @click="$bvModal.hide('bv-modal-scanner')"
				>&times;</b-button>
			</template>
		</b-modal>   

	</b-card>		
</template>

<script lang="ts">

import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace } from "vuex-class";
import moment from 'moment-timezone';

import "@/store/modules/common";
const commonState = namespace("Common");

import "@/store/modules/forms/vi";
const viState = namespace("VI");

import rsiStore from "@/store";

import { jurisdictionInfoType, provinceInfoType } from '@/types/Common';
import { viFormStatesInfoType, viFormDataInfoType, viFormJsonInfoType } from '@/types/Forms/VI';
import Spinner from "@/components/utils/Spinner.vue";
import {lookupDriverFromICBC} from "@/utils/icbc";
import {lookupDriverProvince} from "@/utils/lookups";
import dlScanner from "@/helpers/dlScanner";

@Component({
    components: {           
        Spinner
    }        
}) 
export default class DriversInformationCard extends Vue {   

	@commonState.State
    public jurisdictions: jurisdictionInfoType[];

	@commonState.State
    public provinces: provinceInfoType[];
	
	@viState.State
    public viInfo: viFormJsonInfoType;
	
	@Prop({required: true})
    driverInfo!: viFormDataInfoType;
	
	@Prop({required: true})
	driverState!: viFormStatesInfoType;

	dataReady = false;
	dob=''
	age = 0;
	error = '';
	path = '';
	showScannerMessage = false;
	scannerOpened = false;
	scannerMessage = '';
	searchingLookup = false;
	searchingDl = false;
	formPrinted = false;	
	dateError=''
	updateDate=0;

	genderOptions = [
        {text: 'Gender Diveres', value: 'Gender Diveres'},
        {text: 'Female', value: 'Female'},
		{text: 'Male', value: 'Male'},
        {text: 'Unknown', value: 'Unknown'}
    ];

	mounted() { 
		this.dataReady = false;				        
		this.formPrinted = Boolean(this.viInfo.printed_timestamp);
        this.extractFields();
        this.dataReady = true;
    }

	public extractFields(){
		this.age = 0;
		this.path = 'forms/' + this.viInfo.form_type + '/' + this.viInfo.form_id + '/data'
	}

	public triggerDriversLookup(){
		console.log("inside triggerDriversLookup()")
		this.error = ''
		this.searchingLookup = true;
		lookupDriverFromICBC([this.path, this.viInfo.data.driversNumber])
			.then(() => {
				const data = this.$store.state.forms['12Hour'][this.viInfo.form_id]
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
		this.driverInfo.driversNumber = data.number;
        this.driverInfo.dob = data['dob'];
        this.driverInfo.givenName = data['name']['given'];
        this.driverInfo.lastName = data['name']['surname'];	
		this.update()	
	}

	public handledScannedBarCode(event) {
		const { data, device, reportId } = event;
		dlScanner.readFromScanner(device, reportId, data)
		.then( dlData => {
			rsiStore.commit("populateDriverFromBarCode", dlData)
			this.updateFormFields(dlData)
			return dlData['address']['province']
		})
		.then( provinceCode => {
			lookupDriverProvince([this.path, provinceCode])
		})
		.then( () => {
			this.$bvModal.hide('dl-scanner')
		})
	}

	async launchDlScanner() {
		console.log('inside launchDlScanner')
		this.$bvModal.show('dl-scanner')

		const scanner = await dlScanner.openScanner();

		scanner.addEventListener("inputreport", this.handledScannedBarCode);

		this.scannerOpened = !!scanner.opened;

    }

	public closeScannner(){
		this.showScannerMessage = false;
	}

	public update(){     
        this.recheckStates()		
    }

	public recheckStates(){
        this.$emit('recheckStates')
    }

	get displayIcbcLicenceLookup(){

        return this.driverInfo?.driversLicenceJurisdiction?.objectCd == "BC" && this.$store.state.isUserAuthorized;
    }

	public validateDate(datePicker?){
		if(datePicker){			
			let dob=this.dob.replace('-','')
			dob=dob.replace('-','')
			this.driverInfo.dob=dob
			this.updateDate++;
		}
		
		if(!this.driverInfo.dob) return

		if(!Number(this.driverInfo?.dob)||this.driverInfo?.dob?.length!=8){
			this.dateError="The selected date is invalid!"
			this.driverState.dob=false
		}
		else{ 
						
			const date = moment(this.driverInfo.dob)
			const currentDate = moment() 
			const age = currentDate.diff(date, 'years')
			this.age = age? age : 0
			
			if(!date.isValid()){
				this.dateError="The selected date is invalid!"
				this.driverState.dob=false
			}
			else if(currentDate.format("YYYYMMDD")<this.driverInfo.dob){
				this.dateError="The selected date is in the future!"
				this.driverState.dob=false
			}
			else if(this.age<10 || this.age>120){
				this.dateError="Driver must be between 10 and 120 years old!"
				this.driverState.dob=false
			}
			else{ 
				this.dateError=""
				if(!datePicker){
					const year = this.driverInfo.dob.slice(0,4)
					const month = this.driverInfo.dob.slice(4,6)
					const day = this.driverInfo.dob.slice(6)
					this.dob = year+'-'+month+'-'+day
				}
				this.driverState.dob=null
			}
		}
		this.update();
	}

	public allowedDates(date){
        const day = moment().startOf('day').format('YYYY-MM-DD');           
        return (date < day);           
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
