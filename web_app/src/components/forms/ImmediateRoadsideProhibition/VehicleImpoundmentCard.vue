<template>
	<b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
		<b-card-header header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b>Vehicle Impoundment or Disposition</b>      
		</b-card-header>
		<b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">

            <b-row>   
                <b-col cols="3"> 
                    <label class="ml-1 m-0 p-0"> Vehicle Impounded? <span class="text-danger">*</span></label>
                    <b-form-radio-group 
                        stacked
                        v-model="viInfo.vehicleImpounded"                    
                        :options="responseOptions"
                        @change="update"
						:disabled="formPrinted"
						:state="viState.vehicleImpounded">                   
                    </b-form-radio-group> 
                </b-col>  
                <b-col v-if="viInfo.vehicleImpounded">
                    <label class="ml-1 m-0 p-0"></label>
                    <b-form-select	
                        v-model="viInfo.viNumber"
                        :disabled="formPrinted"
                        @change="update"                        							
                        placeholder="Search for an Impound Lot Operator"
                        style="display: block;">
                            <b-form-select-option
                                v-for="viInfo,inx in recentViNumbers" 
                                :key="'vd-vi-'+viInfo.viNumber+inx"
                                :value="viInfo.viNumber">
                                    {{viInfo.label}}
                            </b-form-select-option>    
                    </b-form-select>                     
                </b-col>              
            </b-row>                

            <b-row v-if="viInfo.vehicleImpounded">
                <b-col cols="3"></b-col>
                <b-col>
                    <label class="ml-1 m-0 p-0"> Vehicle Impoundment Number <span class="text-danger">*</span></label>
                    <b-form-input						
                        :disabled="formPrinted"
                        v-model="viInfo.viNumber"
                        @input="update"
                        :state="viState.viNumber">
                    </b-form-input> 
                </b-col>
            </b-row>

                        
		</b-card>
	</b-card>
</template>

<script lang="ts">

import { Component, Vue, Prop } from 'vue-property-decorator';
import { namespace } from "vuex-class";

import "@/store/modules/forms/irp";
const irpState = namespace("IRP");

import { irpFormStatesInfoType, irpFormDataInfoType, irpFormJsonInfoType } from '@/types/Forms/IRP';
import Spinner from "@/components/utils/Spinner.vue";
import { getArrayOfRecentViNumbers } from '@/utils/forms';

@Component({
    components: {           
        Spinner
    }        
}) 
export default class VehicleImpoundmentCard extends Vue {     

	@irpState.State
    public irpInfo: irpFormJsonInfoType;

	@Prop({required: true})
    viInfo!: irpFormDataInfoType;
	
	@Prop({required: true})
	viState!: irpFormStatesInfoType;

	dataReady = false;   
	error = '';
	formPrinted = false;
    recentViNumbers = [];

    responseOptions = [
        {text: 'Yes', value: true},
        {text: 'No', value: false}
    ];    

	mounted() { 
        this.dataReady = false;				        
		this.formPrinted = Boolean(this.irpInfo.printed_timestamp);       
        this.recentViNumbers = getArrayOfRecentViNumbers(); 
        console.log(this.recentViNumbers)
        this.dataReady = true;
    }

	public update(){
        this.recheckStates()
    }

	public recheckStates(){
        this.$emit('recheckStates')
    }
 
}
</script>




<style scoped>

</style>