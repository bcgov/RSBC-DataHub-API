<template>
    <b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
		<b-card-header class="text-left h3" header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b>Prohibition</b>      
		</b-card-header>
		<b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">

            <b-row class="text-left">   
                <b-col cols="4"> 
                    <label class="m-0 mb-2 p-0"> Type of Prohibition (select one) <span class="text-danger">*</span></label>
                    <b-form-radio-group
                        :class="(prohibitionState.prohibitionType==null)?'':'border border-danger is-invalid'"
                        size="lg"
                        stacked
                        v-model="prohibitionInfo.prohibitionType"                    
                        :options="prohibitionTypeOptions"
                        @change="update"
						:disabled="formPrinted"
						:state="prohibitionState.prohibitionType">                   
                    </b-form-radio-group> 
                </b-col>                
            </b-row>
            
            <b-row class="text-left">
                <b-col cols="8">
                    <label class="ml-1 m-0 p-0"> Intersection or Address of Offence <span class="text-danger">*</span></label>
                    <b-form-input
                        size="lg"
                        v-model="prohibitionInfo.offenceAddress"
                        :disabled="formPrinted"
                        @input="update"
                        :state="prohibitionState.offenceAddress">
                    </b-form-input>                                
                </b-col>
				<b-col >                   
                    <label class="ml-1 m-0 p-0">City<span class="text-danger">*</span></label>
                    <input-search-form
                        :data="prohibitionInfo"
                        dataField="offenceCity"
                        :optionList="cities"
                        optionLabelField="objectDsc"
                        :error="prohibitionState.offenceCity==false?'Please select one!':''"
                        :disabled="formPrinted"
                        placeholder="Search for a BC city or town name"
                        @update="update"
                    />                  
                </b-col>
            </b-row>                

            <b-row class="text-left">
                <b-col cols="3">
                    <label class="ml-1 m-0 p-0"> Agency File Number <span class="text-danger">*</span></label>
                    <b-form-input 
                        size="lg"                 
                        v-model="prohibitionInfo.agencyFileNumber"
                        :disabled="formPrinted"
                        @input="update"
                        :state="prohibitionState.agencyFileNumber">
                    </b-form-input>                                
                </b-col> 
                <b-col >
                    <label 
                        class="ml-1 m-0 p-0"> Date of Driving - <span style="font-size: 15pt;">care or control</span>  
                        <span class="text-danger">*</span>
                        <span class="text-muted" style="font-size: 14pt;"> YYYYMMDD</span>
                    </label>
                    <b-input-group class="mb-3">
                        <b-form-input
                            size="lg"
                            :key="updateDate"
                            id="prohibition-state-date"
                            v-model="prohibitionInfo.prohibitionStartDate"
                            type="text"
                            @input="validateDate(false,false)"
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
                                @context="validateDate(true,false)"
                            ></b-form-datepicker>
                        </b-input-group-append>
                    </b-input-group>   
                    <div v-if="dateError" style="font-size:10pt;" class="text-danger text-left m-0 mt-n3 p-0">{{dateError}}</div>
                </b-col>
                <b-col>					
                    <label 
                        class="ml-1 m-0 p-0"> Time of Driving - <span style="font-size: 15pt;">care or control</span>
                        <span class="text-danger">*</span>
                        <span class="text-muted" style="font-size: 14pt;"> HHMM in Pacific Time</span>
                    </label>
                    <b-form-input
                        size="lg"
                        placeholder="HHMM"
                        v-model="prohibitionInfo.prohibitionStartTime"
                        :disabled="formPrinted"
                        @input="validateDate(false, true)"
                        :state="prohibitionState.prohibitionStartTime">
                    </b-form-input>
                    <div v-if="timeError" style="font-size:10pt;" class="text-danger text-left m-0 mt-0 p-0">{{timeError}}</div>                            
                </b-col>
            </b-row>
		</b-card>
	</b-card>

</template>


<script lang="ts">

import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace } from "vuex-class";
import moment from 'moment-timezone';

import InputSearchForm from '@/components/utils/InputSearchForm.vue'

import "@/store/modules/common";
const commonState = namespace("Common");

import "@/store/modules/forms/mv2906";
const mv2906State = namespace("MV2906");

import { cityInfoType } from '@/types/Common';
import { twelveHourFormStatesInfoType, twelveHourFormDataInfoType, twelveHourFormJsonInfoType } from '@/types/Forms/MV2906';
import Spinner from "@/components/utils/Spinner.vue";

@Component({
    components: {           
        Spinner,
        InputSearchForm
    }        
}) 
export default class ProhibitionInformationCard extends Vue {   

	@commonState.State
    public cities: cityInfoType[];

	@mv2906State.State
    public mv2906Info: twelveHourFormJsonInfoType;

	@Prop({required: true})
    prohibitionInfo!: twelveHourFormDataInfoType;
	
	@Prop({required: true})
	prohibitionState!: twelveHourFormStatesInfoType;

	dataReady = false;
    updateDate=0;
    prohibitionStartDate = '';
    dateError = '';
    timeError = '';
	error = '';
	path = '';
	formPrinted = false;    

    prohibitionTypeOptions = [
        {text: 'Alcohol 90.3(2)', value: 'Alcohol'},
        {text: 'Drugs 90.3(2.1)', value: 'Drugs'}
    ];

	mounted() { 
        this.dataReady = false;				        
		this.formPrinted = Boolean(this.mv2906Info.printed_timestamp);        
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
			let prohibitionStartDate=this.prohibitionStartDate.replace('-','')
			prohibitionStartDate=prohibitionStartDate.replace('-','')
			this.prohibitionInfo.prohibitionStartDate=prohibitionStartDate
			this.updateDate++;
		}

        let prbTime='0000'
        
        const timeFormat = /^([0-1][0-9]|2[0-3])[0-5][0-9]$/
        if( !Number(this.prohibitionInfo?.prohibitionStartTime) ||
            this.prohibitionInfo?.prohibitionStartTime?.length!=4 ||
            timeFormat.test(this.prohibitionInfo?.prohibitionStartTime)==false
        ){
            if(timeInput){
                this.timeError="The input time is invalid!"
                this.prohibitionState.prohibitionStartTime=false                
            }
        }else{
            this.timeError=""
            this.prohibitionState.prohibitionStartTime=null;
            prbTime=this.prohibitionInfo.prohibitionStartTime
        }
        
		
		if(!this.prohibitionInfo.prohibitionStartDate) return

		if(!Number(this.prohibitionInfo?.prohibitionStartDate)||this.prohibitionInfo?.prohibitionStartDate?.length!=8){
			this.dateError="The selected date is invalid!"
			this.prohibitionState.prohibitionStartDate=false
		}
		else{ 
						
			const date = moment(this.prohibitionInfo.prohibitionStartDate)
			const currentDate = moment() 
			// console.log(currentDate.format("YYYYMMDDHHmm"))
            const prbDateTime = this.prohibitionInfo.prohibitionStartDate+prbTime
            // console.log(prbDateTime)
			
			if(!date.isValid()){
				this.dateError="The selected date is invalid!"
				this.prohibitionState.prohibitionStartDate=false
			}
			else if(currentDate.format("YYYYMMDDHHmm")<prbDateTime){
				this.dateError="The selected date/time is in the future!"
                this.timeError="The selected date/time is in the future!"
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
    
    input.is-invalid {
		background: #ebc417;
	}

    label{
        font-size: 16pt;
    }

</style>
