<template>	
	<b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
		<b-card-header class="text-left h3" header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b>Driver's Information</b>      
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
			<b-row>
				<b-col class="pr-1 text-left" cols="3">
					<b-form-group>
					<label class="m-0 p-0"> Driver's Licence Number <span class="text-danger">*</span></label>
					<b-form-input
						size="lg"
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
						size="lg"
						class="bg-primary text-white"
						style="float:left; margin-top:1.7rem;"
						:disabled="formPrinted || !displayIcbcLicenceLookup"
						@click="triggerDriversLookup">
						<spinner color="#FFF" v-if="searchingLookup" style="margin:0; padding: 0; transform:translate(-12px,-22px);"/>
						<span style="font-size: 14pt;" v-else>ICBC Prefill</span>
					</b-button>  
				</b-col>
				<b-col class="p-0 pt-1" cols="1">
					<b-button 
						size="lg"
						class="bg-primary text-white"
						style="opacity:1; float:right; margin-top:1.7rem;"
						@click="launchDlScanner">
						<spinner color="#FFF" v-if="searchingDl" style="margin:0; padding: 0; transform:translate(-12px,-22px);"/>
						<span style="font-size: 14pt;" v-else>Scan DL</span>
					</b-button>  
				</b-col>
				<b-col cols="3" class="text-left pl-1">
					<label class="ml-0 m-0 p-0"> Prov / State / International </label>
					<input-search-form
                        :data="driverInfo"
                        dataField="driversLicenceJurisdiction"
                        :optionList="jurisdictions"
                        optionLabelField="objectDsc"
                        :error="driverState.driversLicenceJurisdiction==false?'Please select one!':''"
                        :disabled="formPrinted"
                        placeholder="Search for a Jurisdiction"
                        @update="update"
                    />                     
				</b-col>
			</b-row>
			<b-row class="text-left">
				<b-col>
					<label class="ml-1 m-0 p-0"> Last Name <span class="text-danger">*</span></label>
					<b-form-input
						size="lg"
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
						size="lg"
						placeholder="Given Names"
						v-model="driverInfo.givenName"
						:disabled="formPrinted"
						@input="update"
						:state="driverState.givenName">
					</b-form-input>  
				</b-col>
				<b-col >
					<label class="ml-1 m-0 p-0"> Date of Birth <span class="text-danger">* </span><span class="text-muted" style="font-size: 12pt;">YYYYMMDD ({{age}} yrs)</span></label>
					
					<b-input-group class="mb-3">
						<b-form-input
							size="lg"
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
			<b-row class="text-left">
				<b-col cols="8">					
					<label class="ml-1 m-0 p-0"> Address <span class="text-danger">*</span></label>
					<b-form-input
						size="lg"
						placeholder="Address"
						:disabled="formPrinted"
						v-model="driverInfo.address"
						@input="update"
						:state="driverState.address">
					</b-form-input>
				</b-col>
				<b-col>
					<label class="ml-1 m-0 p-0"> Phone </label>
					<b-form-input
						size="lg"						
						v-model="driverInfo.driverPhoneNumber"						
						:formatter="editPhoneNumber"
						:disabled="formPrinted"
						:state="driverState.driverPhoneNumber">
					</b-form-input>  
					<div
                        v-if="(driverState.driverPhoneNumber != null)" 
                        style="font-size: 10pt; " 
                        class="text-left text-danger m-0 p-0">
                        Phone number format <i>000-000-0000</i>
                    </div> 

				</b-col>
			</b-row>
			<b-row class="text-left">
				<b-col cols="5" >
					<label class="ml-1 m-0 p-0"> City <span class="text-danger">*</span></label>
					<b-form-input
						size="lg"						
						v-model="driverInfo.driverCity"						
						@input="update"
						:disabled="formPrinted"
						:state="driverState.driverCity">
					</b-form-input>                                
				</b-col>
				<b-col cols="3">
					<label class="ml-1 m-0 p-0"> Prov / State <span class="text-danger">*</span></label>
					<input-search-form
                        :data="driverInfo"
                        dataField="driverProvince"
                        :optionList="provinces"
                        optionLabelField="objectDsc"
                        :error="driverState.driverProvince==false?'Please select one!':''"
                        :disabled="formPrinted"
                        placeholder="Search for a Province or State"
                        @update="update"
                    />                    
				</b-col>
				<b-col >
					<label class="ml-1 m-0 p-0"> Postal / Zip</label>
					<b-form-input
						size="lg"						
						v-model="driverInfo.driverPostalCode"						
						@input="update"
						:disabled="formPrinted"
						:state="driverState.driverPostalCode">
					</b-form-input> 
					<div
                        v-if="(driverState.driverPostalCode != null)" 
                        style="font-size: 8.5pt; " 
                        class="text-left text-danger m-0 p-0">
                        Invalid Postal Code for Prov/State <i>(For CANADA the format is A1A 1A1)</i>
                    </div>                                  
				</b-col>
			</b-row>
			
						

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

import "@/store/modules/forms/mv2906";
const mv2906State = namespace("MV2906");

import rsiStore from "@/store";

import InputSearchForm from '@/components/utils/InputSearchForm.vue'

import { jurisdictionInfoType, provinceInfoType } from '@/types/Common';
import { twelveHourFormStatesInfoType, twelveHourFormDataInfoType, twelveHourFormJsonInfoType } from '@/types/Forms/MV2906';
import Spinner from "@/components/utils/Spinner.vue";
import {lookupDriverFromICBC} from "@/utils/icbc";
import {lookupDriverProvince} from "@/utils/lookups";
import dlScanner from "@/helpers/dlScanner";

@Component({
    components: {           
        Spinner,
		InputSearchForm
    }        
}) 
export default class DriversInformationCard extends Vue {   

	@commonState.State
    public jurisdictions: jurisdictionInfoType[];

	@commonState.State
    public provinces: provinceInfoType[];
	
	@mv2906State.State
    public mv2906Info: twelveHourFormJsonInfoType;
	
	@Prop({required: true})
    driverInfo!: twelveHourFormDataInfoType;
	
	@Prop({required: true})
	driverState!: twelveHourFormStatesInfoType;

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
	phonePrvValue=''
	displayIcbcLicenceLookup=true
	errorDismissCountDown=0

	mounted() { 
		this.dataReady = false;						        
		this.formPrinted = Boolean(this.mv2906Info.printed_timestamp);
        this.extractFields();
		this.checkIcbcLicenceLookupAllowed()
        this.dataReady = true;
    }

	public extractFields(){
		this.age = 0;
		this.path = 'forms/' + this.mv2906Info.form_type + '/' + this.mv2906Info.form_id + '/data'
	}

	public triggerDriversLookup(){
		console.log("inside triggerDriversLookup()")
		this.error = ''
		this.searchingLookup = true;
		lookupDriverFromICBC([this.path, this.mv2906Info.data.driversNumber])
			.then(() => {
				const data = this.$store.state.forms['12Hour'][this.mv2906Info.form_id]
				this.updateFormFields(data);
				this.searchingLookup = false;
			})
			.catch( error => {
				console.log("error", error)
				this.searchingLookup = false;
				this.error = error.description;
				this.errorDismissCountDown=3;
			})
	}

	public updateFormFields(data: any){
		this.driverInfo.driversNumber = data.number;		
        this.driverInfo.address = data['address']['street'];
        this.driverInfo.driverCity = data['address']['city'];
        this.driverInfo.driverPostalCode = data['address']['postalCode'];
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
		this.checkIcbcLicenceLookupAllowed() 
        this.recheckStates()		
    }

	public recheckStates(){
        this.$emit('recheckStates')
    }

	public checkIcbcLicenceLookupAllowed(){
        this.displayIcbcLicenceLookup = this.driverInfo?.driversLicenceJurisdiction?.objectCd == "BC" && this.$store.state.isUserAuthorized;
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

	public editPhoneNumber(value: string){
		this.update()
		if(this.phonePrvValue.slice(-1)=='-' && this.phonePrvValue.length>=value.length) this.phonePrvValue=value.slice(0,-1)
		else if(isNaN(Number(value.slice(-1))) && value.slice(-1)!='-') this.phonePrvValue= value.slice(0,-1) 
		else if(value.length==3) this.phonePrvValue=value.slice(0,3)+'-'; 
		else if(value.length==7) this.phonePrvValue=value.slice(0,7)+'-';
		else if(value.length>12) this.phonePrvValue=value.slice(0,-1)	     
        else this.phonePrvValue=value
		return this.phonePrvValue;
    }

	public allowedDates(date){
        const day = moment().startOf('day').format('YYYY-MM-DD');           
        return (date < day);           
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
	// select.is-invalid {
	// 	background: #ebc417;
	// 	option {
	// 		background: #FFF;
	// 	}
	// }

</style>
