<template>
    <b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
		<b-card-header header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b>Excessive Speed</b>      
		</b-card-header>
		<b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">

            <b-row class="mx-3">
                <b-col cols="4">
                    <label class="ml-1 m-0 p-0"> Speed Limit (km/h) <span class="text-danger">*</span></label>
                    <b-form-input
                        v-model="esInfo.speedLimit"
                        :disabled="formPrinted"
                        type="number"
                        @input="update"
                        :state="esState.speedLimit">
                    </b-form-input>                                
                </b-col>				
            </b-row>                

            <b-row class="mx-3">
                <b-col cols="4">
                    <label class="ml-1 m-0 p-0"> Vehicle Speed (km/h) <span class="text-danger">*</span></label>
                    <b-form-input                        
                        v-model="esInfo.vehicleSpeed"
                        :disabled="formPrinted"
                        type="number"
                        @input="update"
                        :state="esState.vehicleSpeed">
                    </b-form-input>                                
                </b-col> 
            </b-row>
            
            <b-row>   
                <b-col cols="4"> 
                    <label class="ml-1 m-0 p-0"> 
                        Vehicle speed estimated by:                         
                    </label>
                    <b-form-radio-group 
                        stacked
                        v-model="esInfo.excessiveSpeedEstimationType"
                        :options="speedEstimationOptions"
                        @change="update"
						:disabled="formPrinted"
						:state="esState.excessiveSpeedEstimationType">                                         
                    </b-form-radio-group> 
                </b-col>                
            </b-row>
			<b-row>   
				<b-col cols="4"> 
					<label class="ml-1 m-0 p-0"> Vehicle speed confirmed by:</label>
					<b-form-radio-group 
						stacked
						v-model="esInfo.excessiveSpeedConfirmationType"                    
						:options="speedConfirmationOptions"
						@change="update"
						:disabled="formPrinted"
						:state="esState.excessiveSpeedConfirmationType">                   
					</b-form-radio-group> 
				</b-col>                
			</b-row> 

		</b-card>
	</b-card>

</template>


<script lang="ts">

import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace } from "vuex-class";

import "@/store/modules/forms/vi";
const viState = namespace("VI");

import { viFormStatesInfoType, viFormDataInfoType, viFormJsonInfoType } from '@/types/Forms/VI';
import Spinner from "@/components/utils/Spinner.vue";

@Component({
    components: {           
        Spinner
    }        
}) 
export default class ExcessiveSpeedCard extends Vue {
    
    @viState.State
    public viInfo: viFormJsonInfoType;

	@Prop({required: true})
    esInfo!: viFormDataInfoType;
	
	@Prop({required: true})
	esState!: viFormStatesInfoType;

	dataReady = false;
	error = '';
	path = '';
	formPrinted = false; 

	speedEstimationOptions = [
        {text: 'Visual', value: 'Visual'},
        {text: 'Pacing', value: 'Pacing'}
    ];
    
    speedConfirmationOptions = [
        {text: 'Laser', value: 'Laser'},
        {text: 'Radar', value: 'Radar'},
        {text: 'Other (explain in incident details)', value: 'Other'}
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

    //TODO validate speed limit and vehicle speed: Must be at least 41 km/h over speed limit
 
}
</script>

<style scoped>

</style>