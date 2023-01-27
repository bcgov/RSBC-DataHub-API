<template>
	<b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
		<b-card-header  class="text-left h3" header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b>Vehicle Impoundment or Disposition</b>      
		</b-card-header>
		<b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">

            <b-row class="text-left">   
                <b-col cols="3"> 
                    <label class="ml-1 m-0 mb-2 p-0"> Vehicle Impounded? <span class="text-danger">*</span></label>
                    <b-form-radio-group
                        :class="(viState.vehicleImpounded==null)?'':'border border-danger is-invalid'"
                        size="lg" 
                        stacked
                        v-model="viInfo.vehicleImpounded"                    
                        :options="responseOptions"
                        @change="update"
						:disabled="formPrinted"
						:state="viState.vehicleImpounded">                   
                    </b-form-radio-group> 
                </b-col>                
            </b-row>
            <b-card no-body v-if="viInfo.vehicleImpounded" class="bg-time border-0">
                <b-row class="text-left">   
                    <b-col cols="3"> 
                        <label class="ml-1 m-0 mb-2 p-0"> Location of Keys? <span class="text-danger">*</span></label>
                        <b-form-radio-group
                            size="lg"
                            :class="(viState.locationOfKeys==null)?'':'border border-danger is-invalid'"  
                            stacked
                            v-model="viInfo.locationOfKeys"                    
                            :options="keyLocationOptions"
                            @change="update"
                            :disabled="formPrinted"
                            :state="viState.locationOfKeys">                   
                        </b-form-radio-group> 
                    </b-col>                
                </b-row>
                <b-row class="text-left mx-1 mt-0">
                    <b-col>
                        <label class="ml-1 m-0 p-0"></label>
                        <input-search-form-imp-lot
                            :data="viInfo"
                            dataField="impoundLot"
                            :optionList="impound_lot_operators"
                            :error="''"
                            :disabled="formPrinted"
                            placeholder="Search for an Impound Lot Operator"
                            @update="update"
                        />
                    </b-col>
                </b-row>

                <b-row class="text-left mx-3">
                    <label class="ml-1 m-0 p-0"> Impound Lot Operator Name <span class="text-danger">*</span></label>
                    <b-form-input
                        size="lg"						
						:disabled="formPrinted"
						v-model="viInfo.impoundLot.name"
						@input="update"
						:state="viState.impoundLotName">
					</b-form-input> 
                </b-row>

                <b-row class="text-left mx-1">
                    <b-col>
                        <label class="ml-1 m-0 p-0"> Public lot address <span class="text-danger">*</span></label>
                        <b-form-input
                            size="lg"
                            placeholder="Public lot address"
                            v-model="viInfo.impoundLot.lot_address"
                            :disabled="formPrinted"
                            @input="update"
                            :state="viState.impoundLotAddress">
                        </b-form-input>                                
                    </b-col>
					<b-col >
						<label class="ml-1 m-0 p-0"> City <span class="text-danger">*</span></label>
						<b-form-input
                            size="lg"
							placeholder="City"
							v-model="viInfo.impoundLot.city"
							:disabled="formPrinted"
							@input="update"
							:state="viState.impoundLotCity">
						</b-form-input>  
					</b-col>
					<b-col >					
						<label class="ml-1 m-0 p-0"> Public phone <span class="text-danger">*</span></label>
						<b-form-input
                            size="lg"
							placeholder="Public phone"
							v-model="viInfo.impoundLot.phone"
							:disabled="formPrinted"
							@input="update"
							:state="viState.impoundLotPhone">
						</b-form-input>                             
					</b-col>
				</b-row>
            </b-card>
            <b-card no-body v-else-if="viInfo.vehicleImpounded != null"  class="bg-time border-0">
                <b-row class="text-left">   
                    <b-col cols="4"> 
                        <label class="ml-1 m-0 p-0"> Reason for not towing? <span class="text-danger">*</span></label>
                        <b-form-radio-group
                            size="lg"
                            :class="(viState.notImpoundingReason==null)?'':'border border-danger is-invalid'"
                            stacked
                            v-model="viInfo.notImpoundingReason"                    
                            :options="notImpoundingOptions"
                            @change="update"
                            :disabled="formPrinted"
                            :state="viState.notImpoundingReason">                   
                        </b-form-radio-group> 
                    </b-col>                
                </b-row> 
                <b-row v-if="viInfo.notImpoundingReason == 'Released to other driver'" class="text-left">
                    <b-col >
                        <label class="ml-1 m-0 p-0"> Vehicle Released To <span class="text-danger">*</span></label>
                        <b-form-input
                            size="lg"                            
                            v-model="viInfo.vehicleReleasedTo"
                            :disabled="formPrinted"
                            @input="update"
                            :state="viState.vehicleReleasedTo">
                        </b-form-input>                                
                    </b-col>
                    <b-col >
                        <label 
                            class="ml-1 m-0 p-0"> Date Released 
                            <span class="text-danger">*</span>
                            <span class="text-muted" style="font-size: 9pt;"> YYYYMMDD</span>
                        </label>
                        <b-input-group class="mb-3">
                            <b-form-input
                                size="lg"
                                :key="updateDate"
                                v-model="viInfo.releasedDate"
                                type="text"
                                @input="validateDate(false)"
                                :disabled="formPrinted"
                                :state="viState.releasedDate"
                                placeholder="YYYYMMDD"
                                autocomplete="off"
                            ></b-form-input>
                            <b-input-group-append>
                                <b-form-datepicker
                                    v-model="dateReleased"
                                    :disabled="formPrinted"
                                    button-only
                                    right
                                    :allowed-dates="allowedDates"
                                    locale="en-US"
                                    aria-controls="dateReleased"
                                    @context="validateDate(true)"
                                ></b-form-datepicker>
                            </b-input-group-append>
                        </b-input-group>   
                        <div v-if="dateError" style="font-size:10pt;" class="text-danger text-left m-0 mt-n3 p-0">{{dateError}}</div>
                    </b-col>
                    <b-col>					
                        <label 
                            class="ml-1 m-0 p-0"> Time 
                            <span class="text-danger">*</span>
                            <span class="text-muted" style="font-size: 9pt;"> HHMM in Pacific Time</span>
                        </label>
                        <b-form-input
                            size="lg"
                            placeholder="HHMM"
                            v-model="viInfo.releasedTime"
                            :disabled="formPrinted"
                            @input="update"
                            :state="viState.releasedTime">
                        </b-form-input>                             
                    </b-col>
                </b-row>
            </b-card>
		</b-card>
	</b-card>
</template>

<script lang="ts">

import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace } from "vuex-class";
import moment from 'moment-timezone';

import "@/store/modules/common";
const commonState = namespace("Common");

import "@/store/modules/forms/mv2634";
const mv2634State = namespace("MV2634");

import InputSearchFormImpLot from '@/components/utils/InputSearchFormImpLot.vue'

import { impoundLotOperatorsInfoType, jurisdictionInfoType, provinceInfoType } from '@/types/Common';
import { twentyFourHourFormStatesInfoType, twentyFourHourFormDataInfoType, twentyFourHourFormJsonInfoType } from '@/types/Forms/MV2634';
import Spinner from "@/components/utils/Spinner.vue";

@Component({
    components: {           
        Spinner,
        InputSearchFormImpLot
    }        
}) 
export default class VehicleImpoundmentCard extends Vue {   

    @commonState.State
    public impound_lot_operators: impoundLotOperatorsInfoType[];	

	@mv2634State.State
    public mv2634Info: twentyFourHourFormJsonInfoType;

	@Prop({required: true})
    viInfo!: twentyFourHourFormDataInfoType;
	
	@Prop({required: true})
	viState!: twentyFourHourFormStatesInfoType;

	dataReady = false;
    updateDate=0;
    dateReleased = '';
    dateError = '';
	error = '';
	formPrinted = false;

    responseOptions = [
        {text: 'Yes', value: true},
        {text: 'No', value: false}
    ];

    keyLocationOptions = [
        {text: 'With vehicle', value: 'With vehicle'},
        {text: 'With driver', value: 'With driver'}
    ];

    notImpoundingOptions = [
        {text: 'Released to other driver', value: 'Released to other driver'},
        {text: 'Left at roadside', value: 'Left at roadside'},
		{text: 'Private tow', value: 'Private tow'},
        {text: 'Seized for investigation', value: 'Seized for investigation'}
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
			let dateReleased=this.dateReleased.replace('-','')
			dateReleased=dateReleased.replace('-','')
			this.viInfo.releasedDate=dateReleased
			this.updateDate++;
		}
		
		if(!this.viInfo.releasedDate) return

		if(!Number(this.viInfo?.releasedDate)||this.viInfo?.releasedDate?.length!=8){
			this.dateError="The selected date is invalid!"
			this.viState.releasedDate=false
		}
		else{ 
						
			const date = moment(this.viInfo.releasedDate)
			const currentDate = moment() 
			
			
			if(!date.isValid()){
				this.dateError="The selected date is invalid!"
				this.viState.releasedDate=false
			}
			else if(currentDate.format("YYYYMMDD")<this.viInfo.releasedDate){
				this.dateError="The selected date is in the future!"
				this.viState.releasedDate=false
			}			
			else{ 
				this.dateError=""
				if(!datePicker){
					const year = this.viInfo.releasedDate.slice(0,4)
					const month = this.viInfo.releasedDate.slice(4,6)
					const day = this.viInfo.releasedDate.slice(6)
					this.dateReleased = year+'-'+month+'-'+day
				}
				this.viState.releasedDate=null
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