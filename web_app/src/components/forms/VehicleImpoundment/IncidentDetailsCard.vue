<template>
    <b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
		<b-card-header header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b>Incident Details</b>      
		</b-card-header>
		<b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">
           
            <b-row>   
                <b-col>                                       
					<b-form-textarea						
						rows="10"
                        v-model="incidentInfo.incidentDetails"
                        @change="update"
						:disabled="formPrinted"
						:state="incidentState.incidentDetails">						
					</b-form-textarea>
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
export default class IncidentDetailsCard extends Vue {	
    
    @viState.State
    public viInfo: viFormJsonInfoType;

	@Prop({required: true})
    incidentInfo!: viFormDataInfoType;
	
	@Prop({required: true})
	incidentState!: viFormStatesInfoType;

	dataReady = false;    
	error = '';
	path = '';
	formPrinted = false;     

	mounted() { 
        this.dataReady = false;				        
		this.formPrinted = Boolean(this.viInfo.printed_timestamp);        
        this.dataReady = true;
    }	

	public update(){
		//TODO: apply the max:765 rule
        this.recheckStates()
    }

	public recheckStates(){
        this.$emit('recheckStates')
    }
 
}
</script>

<style scoped>

</style>