<template>

	<b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
		<b-card-header header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b-row><b>Registered Owner</b> 
			<b-button 
				class="bg-primary text-white"
				style="opacity:1; float:right;"
				:disabled="formPrinted"
				@click="populateOwnerFromDriver">
				<spinner color="#FFF" v-if="populatingFromDriver" style="margin:0; padding: 0; transform:translate(-12px,-22px);"/>
				<span style="font-size: 0.875rem;" v-else>Fill from driver</span>
			</b-button>  
			</b-row>   
		</b-card-header>
		<b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">
			<b-row>
				<b-col cols="3">
					<b-form-checkbox
						v-model="ownerInfo.ownerOrganization"
						:disabled="formPrinted"
						@input="update"
						:state="ownerState.ownerOrganization">Owned by corporate entity
					</b-form-checkbox>                                
				</b-col>
			</b-row>
			<b-row v-if="ownerInfo.ownerOrganization">
				<b-col >
					<label class="ml-1 m-0 p-0"> Corporation Name </label>
					<b-form-input
						placeholder="Corporation Name"
						v-model="ownerInfo.ownerOrganizationName"
						:disabled="formPrinted"
						@input="update"
						:state="ownerState.ownerOrganizationName">
					</b-form-input>                                
				</b-col>
				
			</b-row>
			<b-row v-else>
				<b-col>
					<label class="ml-1 m-0 p-0"> Owner's Last Name </label>
					<b-form-input
						placeholder="Owner's Last Name"
						v-model="ownerInfo.ownerLastName"
						:disabled="formPrinted"
						@input="update"
						:state="ownerState.ownerLastName">
					</b-form-input>                                
				</b-col>
				<b-col>
					<label class="ml-1 m-0 p-0"> Owner's First Name </label>
					<b-form-input
						placeholder="Owner's First Name"
						v-model="ownerInfo.ownerFirstName"
						:disabled="formPrinted"
						@input="update"
						:state="ownerState.ownerFirstName">
					</b-form-input>  
				</b-col>
			</b-row>
			<b-row>
				<b-col>					
					<label class="ml-1 m-0 p-0"> Address Line </label>
					<b-form-input
						placeholder="Address Line"
						:disabled="formPrinted"
						v-model="ownerInfo.ownerAddress"
						@input="update"
						:state="ownerState.ownerAddress">
					</b-form-input>
				</b-col>				
			</b-row>
			<b-row>
				<b-col cols="6" >
					<label class="ml-1 m-0 p-0"> City </label>
					<b-form-input						
						v-model="ownerInfo.ownerCity"						
						@input="update"
						:disabled="formPrinted"
						:state="ownerState.ownerCity">
					</b-form-input>                                
				</b-col>
				<b-col cols="2">
					<label class="ml-1 m-0 p-0"> Prov / State </label>
					<b-form-select	
						v-model="ownerInfo.ownerProvince"
						:disabled="formPrinted"
						@change="update"
						:state="ownerState.ownerProvince"							
						placeholder="Search for a Province or State"
						style="display: block;">
							<b-form-select-option
								v-for="province,inx in provinces" 
								:key="'owner-province-'+province.objectCd+inx"
								:value="province">
									{{province.objectDsc}}
							</b-form-select-option>    
					</b-form-select>   
				</b-col>
				<b-col >
					<label class="ml-1 m-0 p-0"> Postal / Zip</label>
					<b-form-input						
						v-model="ownerInfo.ownerPostalCode"						
						@input="update"
						:disabled="formPrinted"
						:state="ownerState.ownerPostalCode">
					</b-form-input> 
					<div
                        v-if="(ownerState.ownerPostalCode != null)" 
                        style="font-size: 9.5pt; " 
                        class="text-left text-danger m-0 p-0">
                        Invalid Postal Code <i>(For CANADA format is A1A 1A1)</i>
                    </div>                                  
				</b-col>
				<b-col>
					<label class="ml-1 m-0 p-0"> Phone </label>
					<b-form-input						
						v-model="ownerInfo.ownerPhoneNumber"						
						:formatter="editPhoneNumber"
						:disabled="formPrinted"
						:state="ownerState.ownerPhoneNumber">
					</b-form-input>  
					<div
                        v-if="(ownerState.ownerPhoneNumber != null)" 
                        style="font-size: 10pt; " 
                        class="text-left text-danger m-0 p-0">
                        Phone number format <i>000-000-0000</i>
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

import "@/store/modules/forms/mv2634";
const mv2634State = namespace("MV2634");

import { provinceInfoType } from '@/types/Common';
import { twentyFourHourFormStatesInfoType, twentyFourHourFormDataInfoType, twentyFourHourFormJsonInfoType } from '@/types/Forms/MV2634';
import Spinner from "@/components/utils/Spinner.vue";

@Component({
    components: {           
        Spinner
    }        
}) 
export default class VehicleOwnerCard extends Vue {   

	@commonState.State
    public provinces: provinceInfoType[];
	
	@mv2634State.State
    public mv2634Info: twentyFourHourFormJsonInfoType;
	
	@Prop({required: true})
    ownerInfo!: twentyFourHourFormDataInfoType;
	
	@Prop({required: true})
	ownerState!: twentyFourHourFormStatesInfoType;

	dataReady = false;	
	error = '';
	path = '';	
	populatingFromDriver = false;	
	formPrinted = false;
	phonePrvValue='';

	mounted() { 
		this.dataReady = false;				        
		this.formPrinted = Boolean(this.mv2634Info.printed_timestamp);
        this.extractFields();
        this.dataReady = true;
    }

	public extractFields(){
		this.path = 'forms/' + this.mv2634Info.form_type + '/' + this.mv2634Info.form_id + '/data'
	}

	public update(){     
        this.recheckStates()		
    }

	public recheckStates(){
		this.$emit('recheckStates')
	}

	public editPhoneNumber(value: string, val){
		this.update()
		if(this.phonePrvValue.slice(-1)=='-' && this.phonePrvValue.length>=value.length) this.phonePrvValue=value.slice(0,-1)
		else if(isNaN(Number(value.slice(-1))) && value.slice(-1)!='-') this.phonePrvValue= value.slice(0,-1) 
		else if(value.length==3) this.phonePrvValue=value.slice(0,3)+'-'; 
		else if(value.length==7) this.phonePrvValue=value.slice(0,7)+'-';
		else if(value.length>12) this.phonePrvValue=value.slice(0,-1)	     
        else this.phonePrvValue=value
		return this.phonePrvValue;
    }
	
	public populateOwnerFromDriver() {
		this.populatingFromDriver = true;
		this.ownerInfo.ownerOrganization = false;
		this.ownerInfo.ownerOrganizationName = '';
		this.ownerInfo.ownerFirstName = this.ownerInfo.givenName;
		this.ownerInfo.ownerLastName = this.ownerInfo.lastName;
		this.ownerInfo.ownerAddress = this.ownerInfo.address;
		this.ownerInfo.ownerCity = this.ownerInfo.driverCity;
		this.ownerInfo.ownerProvince = this.ownerInfo.driverProvince;
		this.ownerInfo.ownerPostalCode = this.ownerInfo.driverPostalCode;
		this.update();
		this.populatingFromDriver = false;
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