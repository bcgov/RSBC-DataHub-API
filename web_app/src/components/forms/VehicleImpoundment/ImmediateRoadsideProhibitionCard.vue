<template>
    <b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
		<b-card-header header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b>Immediate Roadside Prohibition</b>      
		</b-card-header>
		<b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">
            
            <b-row>   
                <b-col cols="10"> 
                    <label class="ml-1 m-0 p-0"> 
                        Was an IRP issued as part of this vehicular impound? 
                        <span class="text-muted" style="display: block;">
                            In accordance with Section 215.46 and 253 of the 
							Motor Vehicle Act
							<span class="text-danger">*</span> 
                        </span>
                    </label>
                    <b-form-radio-group 
                        stacked
                        v-model="irpInfo.irp"
                        :options="responseOptions"
                        @change="update"
						:disabled="formPrinted"
						:state="irpState.irp">
                                         
                    </b-form-radio-group> 
                </b-col>                
            </b-row>

            <div v-if="irpInfo.irp">
                <b-row>   
                    <b-col cols="2"> 
                        <label class="ml-1 m-0 p-0"> 
                            Duration <span class="text-danger">*</span>    
                        </label>
                        <b-form-radio-group 
                            stacked
                            v-model="irpInfo.irpType"                    
                            :options="irpTypeOptions"
                            @change="update"
                            :disabled="formPrinted"
                            :state="irpState.irpType">                   
                        </b-form-radio-group> 
                    </b-col>                
                </b-row> 
				<b-row >   
                    <b-col cols="4">
                        <label class="ml-1 m-0 p-0"> IRP Number </label>
                        <b-form-input
                            v-model="irpInfo.iprNumber"
                            :disabled="formPrinted"
                            @input="update"
                            :state="irpState.iprNumber">
                        </b-form-input> 
                    </b-col>  

					<b-col cols="4">
                        <label class="ml-1 m-0 p-0"> This VI Number 
							<span style="font-size: 9pt;">(repeated here for your records)</span> 

						</label>
                        <b-form-input
                            v-model="viInfo.form_id"
                            disabled>
                        </b-form-input> 
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
export default class ImmediateRoadsideProhibitionCard extends Vue {	

	@commonState.State
    public cities: cityInfoType[];
    
    @viState.State
    public viInfo: viFormJsonInfoType;

	@Prop({required: true})
    irpInfo!: viFormDataInfoType;
	
	@Prop({required: true})
	irpState!: viFormStatesInfoType;

	dataReady = false;
    updateDate=0;
    prohibitionStartDate = '';
    dateError = '';
	error = '';
	path = '';
	formPrinted = false;    

    irpTypeOptions = [
        {            
            value: "duration_3-day",
            text: "3-Day"
        },
        {            
            value: "duration_7-day",
            text: "7-Day"
        },
		{
            value: "duration_30-day",
            text: "30-Day"
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
			this.irpInfo.prohibitionStartDate=prohibitionStartDate
			this.updateDate++;
		}
		
		if(!this.irpInfo.prohibitionStartDate) return

		if(!Number(this.irpInfo?.prohibitionStartDate)||this.irpInfo?.prohibitionStartDate?.length!=8){
			this.dateError="The selected date is invalid!"
			this.irpState.prohibitionStartDate=false
		}
		else{ 
						
			const date = moment(this.irpInfo.prohibitionStartDate)
			const currentDate = moment() 
			
			
			if(!date.isValid()){
				this.dateError="The selected date is invalid!"
				this.irpState.prohibitionStartDate=false
			}
			else if(currentDate.format("YYYYMMDD")<this.irpInfo.prohibitionStartDate){
				this.dateError="The selected date is in the future!"
				this.irpState.prohibitionStartDate=false
			}			
			else{ 
				this.dateError=""
				if(!datePicker){
					const year = this.irpInfo.prohibitionStartDate.slice(0,4)
					const month = this.irpInfo.prohibitionStartDate.slice(4,6)
					const day = this.irpInfo.prohibitionStartDate.slice(6)
					this.prohibitionStartDate = year+'-'+month+'-'+day
				}
				this.irpState.prohibitionStartDate=null
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