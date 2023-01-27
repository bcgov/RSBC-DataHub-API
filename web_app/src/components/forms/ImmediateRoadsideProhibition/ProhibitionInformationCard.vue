<template>
    <b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
		<b-card-header header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b>Prohibition</b>      
		</b-card-header>
		<b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">
            
            <b-row class="mx-3">
                <b-col cols="8">
                    <label class="ml-1 m-0 p-0"> Intersection or Address of Offence <span class="text-danger">*</span></label>
                    <b-form-input
                        v-model="prohibitionInfo.offenceAddress"
                        :disabled="formPrinted"
                        @input="update"
                        :state="prohibitionState.offenceAddress">
                    </b-form-input>                                
                </b-col>
				<b-col >                   
                    <label class="ml-1 m-0 p-0">City<span class="text-danger">*</span></label>
                    <b-form-select	
                        v-model="prohibitionInfo.offenceCity"
                        :disabled="formPrinted"
                        @change="update"
                        style="display: block;">
                            <b-form-select-option
                                v-for="city,inx in cities" 
                                :key="'offence-city-'+city.objectCd+inx"
                                :value="city">
                                    {{city.objectDsc}}
                            </b-form-select-option>    
                    </b-form-select> 
                </b-col>
            </b-row>                

            <b-row class="mx-3">                
                <b-col >
                    <label 
                        class="ml-1 m-0 p-0"> Date of Driving - <span style="font-size: 9pt;">care or control</span>  
                        <span class="text-danger">*</span>
                        <span class="text-muted" style="font-size: 9pt;"> YYYYMMDD</span>
                    </label>
                    <b-input-group class="mb-3">
                        <b-form-input
                            :key="updateDate"
                            id="prohibition-state-date"
                            v-model="prohibitionInfo.prohibitionStartDate"
                            type="text"
                            @input="validateDate(false)"
                            :disabled="formPrinted"
                            :state="prohibitionState.prohibitionStartDate"
                            placeholder="YYYYMMDD"
                            autocomplete="off"
                        ></b-form-input>
                        <b-input-group-append>
                            <b-form-datepicker
                                v-model="prohibitionStartDate"
                                :disabled="formPrinted"
                                button-only
                                right
                                :allowed-dates="allowedDates"
                                locale="en-US"
                                aria-controls="prohibitionStartDate"
                                @context="validateDate(true)"
                            ></b-form-datepicker>
                        </b-input-group-append>
                    </b-input-group>   
                    <div v-if="dateError" style="font-size:10pt;" class="text-danger text-left m-0 mt-n3 p-0">{{dateError}}</div>
                </b-col>
                <b-col>					
                    <label 
                        class="ml-1 m-0 p-0"> Time of Driving - <span style="font-size: 9pt;">care or control</span>
                        <span class="text-danger">*</span>
                        <span class="text-muted" style="font-size: 9pt;"> HHMM in Pacific Time</span>
                    </label>
                    <b-form-input
                        placeholder="HHMM"
                        v-model="prohibitionInfo.prohibitionStartTime"
                        :disabled="formPrinted"
                        @input="update"
                        :state="prohibitionState.prohibitionStartTime">
                    </b-form-input>                             
                </b-col>
            </b-row>
            <b-row>   
                <b-col cols="4"> 
                    <label class="ml-1 m-0 p-0"> Prohibition period and type:</label>
                    <b-form-radio-group 
                        stacked
                        v-model="prohibitionInfo.prohibitionTypePeriod"                    
                        :options="prohibitionTypeOptions"
                        @change="update"
						:disabled="formPrinted"
						:state="prohibitionState.prohibitionTypePeriod">                   
                    </b-form-radio-group> 
                </b-col>                
            </b-row>
		</b-card>
	</b-card>

</template>


<script lang="ts">

import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace } from "vuex-class";
import moment from 'moment-timezone';

import "@/store/modules/common";
const commonState = namespace("Common");

import "@/store/modules/forms/irp";
const irpState = namespace("IRP");

import { cityInfoType } from '@/types/Common';
import { irpFormStatesInfoType, irpFormDataInfoType, irpFormJsonInfoType } from '@/types/Forms/IRP';
import Spinner from "@/components/utils/Spinner.vue";

@Component({
    components: {           
        Spinner
    }        
}) 
export default class ProhibitionInformationCard extends Vue {   

	@commonState.State
    public cities: cityInfoType[];

	@irpState.State
    public irpInfo: irpFormJsonInfoType;

	@Prop({required: true})
    prohibitionInfo!: irpFormDataInfoType;
	
	@Prop({required: true})
	prohibitionState!: irpFormStatesInfoType;

	dataReady = false;
    updateDate=0;
    prohibitionStartDate = '';
    dateError = '';
	error = '';
	path = '';
	formPrinted = false;    

    prohibitionTypeOptions = [
        {text: '3 days WARN', value: '3DaysW'},
        {text: '7 days WARN', value: '7DaysW'},
        {text: '30 days WARN', value: '30DaysW'},
        {text: '90 days FAIL', value: '90DaysF'},
        {text: '90 days REFUSAL', value: '90DaysR'}
    ];

	mounted() { 
        this.dataReady = false;				        
		this.formPrinted = Boolean(this.irpInfo.printed_timestamp);        
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
			let prohibitionStartDate=this.prohibitionStartDate.replace('-','')
			prohibitionStartDate=prohibitionStartDate.replace('-','')
			this.prohibitionInfo.prohibitionStartDate=prohibitionStartDate
			this.updateDate++;
		}
		
		if(!this.prohibitionInfo.prohibitionStartDate) return

		if(!Number(this.prohibitionInfo?.prohibitionStartDate)||this.prohibitionInfo?.prohibitionStartDate?.length!=8){
			this.dateError="The selected date is invalid!"
			this.prohibitionState.prohibitionStartDate=false
		}
		else{ 
						
			const date = moment(this.prohibitionInfo.prohibitionStartDate)
			const currentDate = moment() 
			
			
			if(!date.isValid()){
				this.dateError="The selected date is invalid!"
				this.prohibitionState.prohibitionStartDate=false
			}
			else if(currentDate.format("YYYYMMDD")<this.prohibitionInfo.prohibitionStartDate){
				this.dateError="The selected date is in the future!"
				this.prohibitionState.prohibitionStartDate=false
			}			
			else{ 
				this.dateError=""
				if(!datePicker){
					const year = this.prohibitionInfo.prohibitionStartDate.slice(0,4)
					const month = this.prohibitionInfo.prohibitionStartDate.slice(4,6)
					const day = this.prohibitionInfo.prohibitionStartDate.slice(6)
					this.prohibitionStartDate = year+'-'+month+'-'+day
				}
				this.prohibitionState.prohibitionStartDate=null
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




<style scoped>

</style>