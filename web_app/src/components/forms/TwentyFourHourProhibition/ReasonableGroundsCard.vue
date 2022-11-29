<template>
    <b-card v-if="dataReady && rgInfo.prohibitionType.length > 0" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
		<b-card-header class="text-left h3" header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b>Reasonable Grounds</b>      
		</b-card-header>
		<b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">

            <b-row class="text-left">   
                <b-col> 
                    <label class="ml-1 m-0 mb-2 p-0"> 
                        The driver was operating a motor vehicle or had care and 
                        control of a motor vehicle for the purposes of MVA section 
                        215(1) based on (select at least one):
                    </label>
                    <b-form-checkbox-group
                        size="lg"
                        :class="(rgState.reasonableGrounds==null)?'':'border border-danger is-invalid'" 
                        stacked
                        v-model="rgInfo.reasonableGrounds"                    
                        :options="reasonableGroundsOptions"
                        @change="update"
						:disabled="formPrinted"
						:state="rgState.reasonableGrounds">                   
                    </b-form-checkbox-group> 
                </b-col>                
            </b-row>

			<b-row v-if="rgInfo.reasonableGrounds.includes('Other')" class="text-left mt-n3">   
                <b-col>
                    <label class="ml-1 m-0 p-0"> Other </label>
                    <b-form-input
                        size="lg"
                        v-model="rgInfo.reasonableGroundsOther"
                        :disabled="formPrinted"
                        @input="update"
                        :state="rgState.reasonableGroundsOther">
                    </b-form-input> 
				</b-col>  
                             
            </b-row>

            <b-row class="text-left mt-4">   
                <b-col> 
                    <label class="ml-1 m-0 mb-2 p-0"> Was a prescribed test used to form reasonable grounds?</label>
                    <b-form-radio-group 
                        size="lg"
                        :class="(rgState.prescribedTest==null)?'':'border border-danger is-invalid'"
                        stacked
                        v-model="rgInfo.prescribedTest"                    
                        :options="responseOptions"
                        @change="update"
						:disabled="formPrinted"
						:state="rgState.prescribedTest">                   
                    </b-form-radio-group> 
                </b-col>                
            </b-row>            
            <b-row v-if="rgInfo.prescribedTest" class="text-left"> 
                <b-col cols="4">
                    <label 
                        class="ml-1 m-0 p-0"> Date of test  
                        <span class="text-danger">*</span>
                        <span class="text-muted" style="font-size: 9pt;"> YYYYMMDD</span>
                    </label>
                    <b-input-group class="mb-3">
                        <b-form-input
                            size="lg"
                            :key="updateDate"
                            id="prohibition-state-date"
                            v-model="rgInfo.prescribedTestDate"
                            type="text"
                            @input="validateDate(false, false)"
                            :disabled="formPrinted"
                            :state="rgState.prescribedTestDate"
                            placeholder="YYYYMMDD"
                            autocomplete="off"
                        ></b-form-input>
                        <b-input-group-append>
                            <b-form-datepicker
                                v-model="prescribedTestDate"
                                :disabled="formPrinted"
                                button-only
                                right
                                :allowed-dates="allowedDates"
                                locale="en-US"
                                aria-controls="prescribedTestDate"
                                @context="validateDate(true, false)"
                            ></b-form-datepicker>
                        </b-input-group-append>
                    </b-input-group>   
                    <div v-if="dateError" style="font-size:10pt;" class="text-danger text-left m-0 mt-n3 p-0">{{dateError}}</div>
                </b-col>
                <b-col cols="4">					
                    <label 
                        class="ml-1 m-0 p-0"> Time 
                        <span class="text-danger">*</span>
                        <span class="text-muted" style="font-size: 9pt;"> HHMM in Pacific Time</span>
                    </label>
                    <b-form-input
                        size="lg"
                        placeholder="HHMM"
                        v-model="rgInfo.prescribedTestTime"
                        :disabled="formPrinted"
                        @input="validateDate(false, false)"
                        :state="rgState.prescribedTestTime">
                    </b-form-input>
                    <div v-if="timeError" style="font-size:10pt;" class="text-danger text-left m-0 mt-0 p-0">{{timeError}}</div>                             
                </b-col>
            </b-row>

            <b-row v-else-if="rgInfo.prescribedTest != null" class="text-left mt-4">   
                <b-col cols="6"> 
                    <label class="ml-1 m-0 mb-2 p-0"> Why was a prescribed test not used?</label>
                    <b-form-radio-group 
                        size="lg"
                        stacked
                        v-model="rgInfo.prescribedNoTestReason"                    
                        :options="prescribedTestNotUsedOptions"
                        @change="update"
						:disabled="formPrinted"
						:state="rgState.prescribedNoTestReason">                   
                    </b-form-radio-group> 
                </b-col>                
            </b-row> 


		</b-card>
	</b-card>

</template>


<script lang="ts">

import { Component, Vue, Prop, Watch } from 'vue-property-decorator';
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
    rgInfo!: twentyFourHourFormDataInfoType;
	
	@Prop({required: true})
	rgState!: twentyFourHourFormStatesInfoType;

	dataReady = false;
    updateDate=0;
    prescribedTestDate = '';
    dateError = '';
    timeError = '';
	error = '';
	path = '';
	formPrinted = false;    

    reasonableGroundsOptions = [
        {text: 'Witnessed by officer', value: 'Witnessed by officer'},
        {text: 'Admission by driver', value: 'Admission by driver'},
		{text: 'Independent witness', value: 'Independent witness'},
        {text: 'Video surveillance', value: 'Video surveillance'},
        {text: 'Other', value: 'Other'}
    ];

	responseOptions = [
        {text: 'Yes', value: true},
        {text: 'No', value: false}
    ];

	prescribedTestNotUsedOptions = [
        {text: 'Refused by driver', value: 'Refused by driver'},
        {
			text: 'Opinion formed the driver was affected by alcohol and/or drugs', 
			value: 'Opinion formed the driver was affected by alcohol and/or drugs'
		}
    ];

    @Watch('rgInfo.prohibitionStartDate')
    prohibitionDateChanged(v){
        this.validateDate(false,false)
    }

    @Watch('rgInfo.prohibitionStartTime')
    prohibitionTimeChanged(v){
        this.validateDate(false,false)
    }

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

	public validateDate(datePicker, timeInput){
		if(datePicker){			
			let prescribedTestDate=this.prescribedTestDate.replace('-','')
			prescribedTestDate=prescribedTestDate.replace('-','')
			this.rgInfo.prescribedTestDate=prescribedTestDate
			this.updateDate++;
		}

        let testTime='0000'
        
        const timeFormat = /^([0-1][0-9]|2[0-3])[0-5][0-9]$/
        if( !Number(this.rgInfo?.prescribedTestTime) ||
            this.rgInfo?.prescribedTestTime?.length!=4 ||
            timeFormat.test(this.rgInfo?.prescribedTestTime)==false
        ){
            if(timeInput){
                this.timeError="The input time is invalid!"
                this.rgState.prescribedTestTime=false                
            }
        }else{
            this.timeError=""
            this.rgState.prescribedTestTime=null;
            testTime=this.rgInfo.prescribedTestTime
        }
		
		if(!this.rgInfo.prescribedTestDate) return

		if(!Number(this.rgInfo?.prescribedTestDate)||this.rgInfo?.prescribedTestDate?.length!=8){
			this.dateError="The selected date is invalid!"
			this.rgState.prescribedTestDate=false
		}
		else{ 
						
			const date = moment(this.rgInfo.prescribedTestDate)
            const prbDate = this.rgInfo.prohibitionStartDate? this.rgInfo.prohibitionStartDate : '21000101'
            const prbTime = this.rgInfo.prohibitionStartTime? this.rgInfo.prohibitionStartTime : '2359'
			const prbDateTime  = prbDate+prbTime
			const testDateTime = this.rgInfo.prescribedTestDate+testTime
			
			if(!date.isValid()){
				this.dateError="The selected date is invalid!"
				this.rgState.prescribedTestDate=false
			}
            else if(prbDateTime>testDateTime){
				this.dateError="The selected date/time cannot be before care or control date / time!"
                this.timeError="The selected date/time cannot be before care or control date / time!"
				this.rgState.prescribedTestDate=false
			}			
			else{ 
				this.dateError=""
				if(!datePicker){
					const year = this.rgInfo.prescribedTestDate.slice(0,4)
					const month = this.rgInfo.prescribedTestDate.slice(4,6)
					const day = this.rgInfo.prescribedTestDate.slice(6)
					this.prescribedTestDate = year+'-'+month+'-'+day
				}
				this.rgState.prescribedTestDate=null
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

	label{
		font-size: 16pt;
	}

	input.is-invalid {
		background: #ebc417;
	}
</style>