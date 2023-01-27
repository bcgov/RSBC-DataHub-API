<template>
    <b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
		<b-card-header class="text-left h3" header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b>Test Administered - 
				<span v-if="taInfo.prohibitionType.length > 0 && taInfo.prohibitionType == 'Alcohol'"> Alcohol 215(2)</span>
				<span v-else-if="taInfo.prohibitionType.length > 0 && taInfo.prohibitionType == 'Drugs'"> Drugs 215(3)</span>
			</b>      
		</b-card-header>
		<b-card v-if="taInfo.prohibitionType.length > 0 && taInfo.prohibitionType == 'Alcohol'" border-variant="light" bg-variant="time" text-variant="dark" class="my-0">

            <b-row class="text-left">   
                <b-col cols="6"> 
                    <label class="ml-1 m-0 mb-2 p-0"> 
                        Which test was used?
                    </label>
                    <b-form-radio-group 
						size="lg"
                        stacked
						:class="(taState.alcoholTest==null)?'':'border border-danger is-invalid'"
                        v-model="taInfo.alcoholTest"                    
                        :options="alcoholTestOptions"
                        @change="update"
						:disabled="formPrinted"
						:state="taState.alcoholTest">                   
                    </b-form-radio-group> 
                </b-col>                
            </b-row>

			<b-row v-if="taInfo.alcoholTest == 'Approved Instrument'" class="text-left">   
                <b-col cols="4">
                    <label class="ml-1 m-0 p-0"> BAC Result (mg%) <span class="text-danger">*</span></label>
                    <b-form-input
						size="lg"
                        v-model="taInfo.BacResult"
                        :disabled="formPrinted"
                        @input="update"
                        :state="taState.BacResult">
                    </b-form-input> 
				</b-col>  
                             
            </b-row>
			<div v-else-if="taInfo.alcoholTest == 'Alco-Sensor FST (ASD)'">

				<b-row class="text-left mt-4"> 
					<b-col cols="4">
						<label 
							class="ml-1 m-0 p-0"> ASD expiry date  
							<span class="text-danger">*</span>
							<span class="text-muted" style="font-size: 12pt;"> YYYYMMDD</span>
						</label>
						<b-input-group class="mb-3">
							<b-form-input
								size="lg"
								:key="updateDate"
								id="prohibition-state-date"
								v-model="taInfo.asd.expiryDate"
								type="text"
								@input="validateDate(false)"
								:disabled="formPrinted"
								:state="taState.asdExpiryDate"
								placeholder="YYYYMMDD"
								autocomplete="off"
							></b-form-input>
							<b-input-group-append>
								<b-form-datepicker
									v-model="asdExpiryDate"
									:disabled="formPrinted"
									button-only
									right
									:allowed-dates="allowedDates"
									locale="en-US"
									aria-controls="asdExpiryDate"
									@context="validateDate(true)"
								></b-form-datepicker>
							</b-input-group-append>
						</b-input-group>   
						<div v-if="dateError" style="font-size:10pt;" class="text-danger text-left m-0 mt-n3 p-0">{{dateError}}</div>
					</b-col>                
				</b-row>
				<b-row class="text-left">   
					<b-col cols="4"> 
						<label class="ml-1 m-0 p-0"> Result</label>
						<b-form-radio-group
							size="lg"
							:class="(taState.asdResult==null)?'':'border border-danger is-invalid'"
							stacked
							v-model="taInfo.asd.result"                    
							:options="asdResultOptions"
							@change="update"
							:disabled="formPrinted"
							:state="taState.asdResult">                   
						</b-form-radio-group> 
					</b-col>                
				</b-row>

			</div>

		</b-card>
		<b-card v-else-if="taInfo.prohibitionType.length > 0 && taInfo.prohibitionType == 'Drugs'" border-variant="light" bg-variant="time" text-variant="dark" class="my-0">

            <b-row class="text-left">   
                <b-col cols="6"> 
                    <label class="ml-1 m-0 mb-2 p-0"> 
                        Which test was used?
                    </label>
                    <b-form-radio-group 
						size="lg"
						:class="(taState.drugsTest==null)?'':'border border-danger is-invalid'"
                        stacked
                        v-model="taInfo.drugsTest"                    
                        :options="drugsTestOptions"
                        @change="update"
						:disabled="formPrinted"
						:state="taState.drugsTest">                   
                    </b-form-radio-group> 
                </b-col>                
            </b-row>			

            <b-row v-if="taInfo.drugsTest == 'Approved Drug Screening Equipment' " class="text-left mt-4">   
                <b-col cols="4"> 
                    <label class="ml-1 m-0 mb-2 p-0">Test result</label>
                    <b-form-checkbox-group
						size="lg" 
                        stacked
                        v-model="taInfo.approvedDrugScreeningEquipment"                    
                        :options="drugsTestResultOptions"
                        @change="update"
						:disabled="formPrinted"
						:state="taState.approvedDrugScreeningEquipment">                   
                    </b-form-checkbox-group> 
                </b-col>                
            </b-row>

		</b-card>
	</b-card>

</template>


<script lang="ts">

import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace } from "vuex-class";
import moment from 'moment-timezone';

import "@/store/modules/forms/mv2634";
const mv2634State = namespace("MV2634");

import { twentyFourHourFormStatesInfoType, twentyFourHourFormDataInfoType, twentyFourHourFormJsonInfoType } from '@/types/Forms/MV2634';
import Spinner from "@/components/utils/Spinner.vue";

@Component({
    components: {           
        Spinner
    }        
}) 
export default class ReasonableGroundsCard extends Vue {	

	@mv2634State.State
    public mv2634Info: twentyFourHourFormJsonInfoType;

	@Prop({required: true})
    taInfo!: twentyFourHourFormDataInfoType;
	
	@Prop({required: true})
	taState!: twentyFourHourFormStatesInfoType;

	dataReady = false;
    updateDate=0;
    asdExpiryDate = '';
    dateError = '';
	error = '';
	path = '';
	formPrinted = false;    

    alcoholTestOptions = [
        {text: 'Alco-Sensor FST (ASD)', value: 'Alco-Sensor FST (ASD)'},
        {text: 'Approved Instrument', value: 'Approved Instrument'},
		{text: 'Prescribed Physical Coordination Test (SFST)', value: 'Prescribed Physical Coordination Test (SFST)'}      
    ];

	drugsTestOptions = [
        {text: 'Approved Drug Screening Equipment', value: 'Approved Drug Screening Equipment'},
        {text: 'Prescribed Physical Coordination Test (SFST)', value: 'Prescribed Physical Coordination Test (SFST)'},
		{text: 'Prescribed Physical Coordination Test (DRE)', value: 'Prescribed Physical Coordination Test (DRE)'}      
    ];

	asdResultOptions = [
        {text: '51-99 mg%', value: 'under'},
        {text: 'Over 99 mg%', value: 'over'}
    ]; 

	drugsTestResultOptions = [
        {text: 'THC', value: 'THC'},
        {text: 'Cocaine', value: 'Cocaine'}
    ];

	mounted() { 
        this.dataReady = false;				        
		this.formPrinted = Boolean(this.mv2634Info.printed_timestamp);        
        this.dataReady = true;
    }	

	public update(){
        this.recheckStates()
    }

	public recheckStates(){
        this.$emit('recheckStates')
    }

	public validateDate(datePicker?){
		if(datePicker){			
			let asdExpiryDate=this.asdExpiryDate.replace('-','')
			asdExpiryDate=asdExpiryDate.replace('-','')
			this.taInfo.asd.expiryDate=asdExpiryDate
			this.updateDate++;
		}
		
		if(!this.taInfo.asd.expiryDate) return

		if(!Number(this.taInfo?.asd?.expiryDate)||this.taInfo?.asd?.expiryDate?.length!=8){
			this.dateError="The selected date is invalid!"
			this.taState.asdExpiryDate=false
		}
		else{ 
						
			const date = moment(this.taInfo.asd?.expiryDate)
			const currentDate = moment() 
			
			
			if(!date.isValid()){
				this.dateError="The selected date is invalid!"
				this.taState.asdExpiryDate=false
			}
			else if(currentDate.format("YYYYMMDD")<this.taInfo.asd.expiryDate){
				this.dateError="The selected date is in the future!"
				this.taState.asdExpiryDate=false
			}			
			else{ 
				this.dateError=""
				if(!datePicker){
					const year = this.taInfo.asd.expiryDate.slice(0,4)
					const month = this.taInfo.asd.expiryDate.slice(4,6)
					const day = this.taInfo.asd.expiryDate.slice(6)
					this.asdExpiryDate = year+'-'+month+'-'+day
				}
				this.taState.asdExpiryDate=null
			}
		}
		this.update();
	}

	public allowedDates(date){
        //TODO: cannot be before the prohibition start date/time
        const day = moment().startOf('day').format('YYYY-MM-DD');           
        return (date < day);           
    }
 
}
</script>




<style scoped>
	label{
		font-size: 16pt;
	}

	input.is-invalid {
		background: #ebc417;
	}
</style>