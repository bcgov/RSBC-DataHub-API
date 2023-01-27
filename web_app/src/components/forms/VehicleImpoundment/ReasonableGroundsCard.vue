<template>
    <b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
		<b-card-header header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b>Reasonable Grounds</b>      
		</b-card-header>
		<b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">

            <b-row class="mx-3">
                <b-col cols="8">
                    <label class="ml-1 m-0 p-0"> Intersection or Address of Offence <span class="text-danger">*</span></label>
                    <b-form-input
                        v-model="rgInfo.offenceAddress"
                        :disabled="formPrinted"
                        @input="update"
                        :state="rgState.offenceAddress">
                    </b-form-input>                                
                </b-col>
				<b-col >                   
                    <label class="ml-1 m-0 p-0">City<span class="text-danger">*</span></label>
                    <b-form-select	
                        v-model="rgInfo.offenceCity"
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
                <b-col cols="3">
                    <label class="ml-1 m-0 p-0"> Agency File # <span class="text-danger">*</span></label>
                    <b-form-input                        
                        v-model="rgInfo.agencyFileNumber"
                        :disabled="formPrinted"
                        @input="update"
                        :state="rgState.agencyFileNumber">
                    </b-form-input>                                
                </b-col> 
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
                            v-model="rgInfo.prohibitionStartDate"
                            type="text"
                            @input="validateDate(false)"
                            :disabled="formPrinted"
                            :state="rgState.prohibitionStartDate"
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
                        v-model="rgInfo.prohibitionStartTime"
                        :disabled="formPrinted"
                        @input="update"
                        :state="rgState.prohibitionStartTime">
                    </b-form-input>                             
                </b-col>
            </b-row>
            
            <b-row>   
                <b-col cols="10"> 
                    <label class="ml-1 m-0 p-0"> 
                        7-Day Impoundment for the following reason(s) 
                        <span class="text-muted">
                            Section 251 and 253 of the Motor Vehicle Act
                        </span>
                    </label>
                    <b-form-checkbox-group 
                        stacked
                        v-model="rgInfo.impoundReason"  
                                        
                        :options="reasonsOptions"
                        @change="update"
						:disabled="formPrinted"
						:state="rgState.impoundReason">
                                         
                    </b-form-checkbox-group> 
                </b-col>                
            </b-row>

            <div v-if="rgInfo.impoundReason.includes('Unlicensed (UL)')">
                <b-row >   
                    <b-col cols="8">
                        <label class="ml-1 m-0 p-0"> UL Prohibition Number </label>
                        <b-form-input
                            v-model="rgInfo.unlicensedProhibitionNumber"
                            :disabled="formPrinted"
                            @input="update"
                            :state="rgState.unlicensedProhibitionNumber">
                        </b-form-input> 
                    </b-col>  
                                
                </b-row>

                <b-row>   
                    <b-col cols="12"> 
                        <label class="ml-1 m-0 p-0"> 
                            Does the officer have grounds to believe that 
                            the Driver resides in British Columbia? 
                            (explain in incident details)    
                        </label>
                        <b-form-radio-group 
                            stacked
                            v-model="rgInfo.unlicensedBcResident"                    
                            :options="responseOptions"
                            @change="update"
                            :disabled="formPrinted"
                            :state="rgState.unlicensedBcResident">                   
                        </b-form-radio-group> 
                    </b-col>                
                </b-row>  
            </div>  

		</b-card>
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

import { viFormStatesInfoType, viFormDataInfoType, viFormJsonInfoType } from '@/types/Forms/VI';
import Spinner from "@/components/utils/Spinner.vue";
import { cityInfoType } from '@/types/Common';

@Component({
    components: {           
        Spinner
    }        
}) 
export default class ReasonableGroundsCard extends Vue {	

	@commonState.State
    public cities: cityInfoType[];
    
    @viState.State
    public viInfo: viFormJsonInfoType;

	@Prop({required: true})
    rgInfo!: viFormDataInfoType;
	
	@Prop({required: true})
	rgState!: viFormStatesInfoType;

	dataReady = false;
    updateDate=0;
    prohibitionStartDate = '';
    dateError = '';
	error = '';
	path = '';
	formPrinted = false;    

    reasonsOptions = [
        {            
            value: "Excessive Speed",
            html: "Excessive Speed <span class='text-muted'>- Committing an offence under section 148 of the Motor Vehicle Act</span>"
        },
        {            
            value: "Prohibited",
            html: "Prohibited <span class='text-muted'>- Driving while prohibited under the Motor Vehicle Act, Criminal Code, Youth Justice Act or Youth Criminal Justice Act (Canada).</span>"
        },
		{
            value: "Suspended",
            html: "Suspended <span class='text-muted'>- Driving while suspended under section 89 or section 232 of the Motor Vehicle Act.</span>"
        },
        {
            value: "Street Racing",
            html: "Street Racing <span class='text-muted'>- Driving or operating a motor vehicle in a race as defined in the Motor Vehicle Act and the officer intends to charge with an offence.</span>"
        },
        {           
            value: "Stunt Driving",
            html: "Stunt Driving <span class='text-muted'>- Driving or operating a motor vehicle in a stunt as defined in the Motor Vehicle Act and the officer intends to charge with an offence.</span>"
        },
        {            
            value: "Motorcycle (seating)",
            html: "Motorcycle (seating) <span class='text-muted'>- Committing an offence under section 194 (1) or (2) of the Motor Vehicle Act.</span>"
        },
		{            
            value: "Motorcycle (restrictions)",
            html: "Motorcycle (restrictions)<span class='text-muted'>- Committing an offence under section 25(15) of the Motor Vehicle Act relating to a restriction or condition of a motorcycle learner or novice driver’s licence.</span>"
        },
        {  
            value: "Unlicensed (UL)",
            html: "Unlicensed (UL) <span class='text-muted'>- Driving without a valid driver’s licence and with a notice on the driving record indicating a previous conviction for driving while unlicensed.</span>"
        }
    ];

	responseOptions = [
        {text: 'Yes', value: true},
        {text: 'No', value: false}
    ];	

	mounted() { 
        this.dataReady = false;				        
		this.formPrinted = Boolean(this.viInfo.printed_timestamp);        
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
			this.rgInfo.prohibitionStartDate=prohibitionStartDate
			this.updateDate++;
		}
		
		if(!this.rgInfo.prohibitionStartDate) return

		if(!Number(this.rgInfo?.prohibitionStartDate)||this.rgInfo?.prohibitionStartDate?.length!=8){
			this.dateError="The selected date is invalid!"
			this.rgState.prohibitionStartDate=false
		}
		else{ 
						
			const date = moment(this.rgInfo.prohibitionStartDate)
			const currentDate = moment() 
			
			
			if(!date.isValid()){
				this.dateError="The selected date is invalid!"
				this.rgState.prohibitionStartDate=false
			}
			else if(currentDate.format("YYYYMMDD")<this.rgInfo.prohibitionStartDate){
				this.dateError="The selected date is in the future!"
				this.rgState.prohibitionStartDate=false
			}			
			else{ 
				this.dateError=""
				if(!datePicker){
					const year = this.rgInfo.prohibitionStartDate.slice(0,4)
					const month = this.rgInfo.prohibitionStartDate.slice(4,6)
					const day = this.rgInfo.prohibitionStartDate.slice(6)
					this.prohibitionStartDate = year+'-'+month+'-'+day
				}
				this.rgState.prohibitionStartDate=null
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