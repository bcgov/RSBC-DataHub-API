<template>
	<b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
		<b-card-header header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b>Impound Lot</b>      
		</b-card-header>
		<b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">
        
            <b-row>   
                <b-col>
                    <label 
                        class="ml-1 m-0 p-0"> The motor vehicle was impounded on 
                        <span class="text-danger">*</span>
                        <span class="text-muted" style="font-size: 9pt;"> YYYYMMDD</span>
                    </label>
                    <b-input-group class="mb-3">
                        <b-form-input
                            :key="updateDate"
                            id="dr"
                            v-model="ilInfo.impoundedDate"
                            type="text"
                            @input="validateDate(false)"
                            :disabled="formPrinted"
                            :state="ilState.impoundedDate"
                            placeholder="YYYYMMDD"
                            autocomplete="off"
                        ></b-form-input>
                        <b-input-group-append>
                            <b-form-datepicker
                                v-model="dateImpounded"
                                :disabled="formPrinted"
                                button-only
                                right
                                :allowed-dates="allowedDates"
                                locale="en-US"
                                aria-controls="dateImpounded"
                                @context="validateDate(true)"
                            ></b-form-datepicker>
                        </b-input-group-append>
                    </b-input-group>   
                    <div v-if="dateError" style="font-size:10pt;" class="text-danger text-left m-0 mt-n3 p-0">{{dateError}}</div>
                </b-col>              
            </b-row>
            <b-row class="mx-3">
                <label class="ml-1 m-0 p-0"></label>
                <b-form-select	
                    v-model="ilInfo.impoundLot"
                    :disabled="formPrinted"
                    @change="update"                        							
                    placeholder="Search for an Impound Lot Operator"
                    style="display: block;">
                        <b-form-select-option
                            v-for="lot,inx in impound_lot_operators" 
                            :key="'vd-lot-'+lot.name+inx"
                            :value="lot">
                                {{lot.name}}, {{lot.lot_address}}, {{lot.city}}, {{lot.phone}}
                        </b-form-select-option>    
                </b-form-select> 
            </b-row>

            <b-row class="mx-3">
                <label class="ml-1 m-0 p-0"> Impound Lot Operator Name <span class="text-danger">*</span></label>
                <b-form-input						
                    :disabled="formPrinted"
                    v-model="ilInfo.impoundLot.name"
                    @input="update"
                    :state="ilState.impoundLotName">
                </b-form-input> 
            </b-row>

            <b-row class="mx-3">
                <b-col>
                    <label class="ml-1 m-0 p-0"> Public lot address <span class="text-danger">*</span></label>
                    <b-form-input
                        placeholder="Public lot address"
                        v-model="ilInfo.impoundLot.lot_address"
                        :disabled="formPrinted"
                        @input="update"
                        :state="ilState.impoundLotAddress">
                    </b-form-input>                                
                </b-col>
                <b-col >
                    <label class="ml-1 m-0 p-0"> City <span class="text-danger">*</span></label>
                    <b-form-input
                        placeholder="City"
                        v-model="ilInfo.impoundLot.city"
                        :disabled="formPrinted"
                        @input="update"
                        :state="ilState.impoundLotCity">
                    </b-form-input>  
                </b-col>
                <b-col >					
                    <label class="ml-1 m-0 p-0"> Public phone <span class="text-danger">*</span></label>
                    <b-form-input
                        placeholder="Public phone"
                        v-model="ilInfo.impoundLot.phone"
                        :disabled="formPrinted"
                        @input="update"
                        :state="ilState.impoundLotPhone">
                    </b-form-input>                             
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

import "@/store/modules/forms/vi";
const viState = namespace("VI");

import { impoundLotOperatorsInfoType } from '@/types/Common';
import { viFormStatesInfoType, viFormDataInfoType, viFormJsonInfoType } from '@/types/Forms/VI';
import Spinner from "@/components/utils/Spinner.vue";

@Component({
    components: {           
        Spinner
    }        
}) 
export default class ImpoundLotCard extends Vue {   

    @commonState.State
    public impound_lot_operators: impoundLotOperatorsInfoType[];	

	@viState.State
    public viInfo: viFormJsonInfoType;

	@Prop({required: true})
    ilInfo!: viFormDataInfoType;
	
	@Prop({required: true})
	ilState!: viFormStatesInfoType;

	dataReady = false;
    updateDate=0;
    dateImpounded = '';
    dateError = '';
	error = '';
	formPrinted = false;

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
			let dateImpounded=this.dateImpounded.replace('-','')
			dateImpounded=dateImpounded.replace('-','')
			this.ilInfo.impoundedDate=dateImpounded
			this.updateDate++;
		}
		
		if(!this.ilInfo.impoundedDate) return

		if(!Number(this.ilInfo?.impoundedDate)||this.ilInfo?.impoundedDate?.length!=8){
			this.dateError="The selected date is invalid!"
			this.ilState.impoundedDate=false
		}
		else{ 
						
			const date = moment(this.ilInfo.impoundedDate)
			const currentDate = moment() 
			
			
			if(!date.isValid()){
				this.dateError="The selected date is invalid!"
				this.ilState.impoundedDate=false
			}
			else if(currentDate.format("YYYYMMDD")<this.ilInfo.impoundedDate){
				this.dateError="The selected date is in the future!"
				this.ilState.impoundedDate=false
			}			
			else{ 
				this.dateError=""
				if(!datePicker){
					const year = this.ilInfo.impoundedDate.slice(0,4)
					const month = this.ilInfo.impoundedDate.slice(4,6)
					const day = this.ilInfo.impoundedDate.slice(6)
					this.dateImpounded = year+'-'+month+'-'+day
				}
				this.ilState.impoundedDate=null
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