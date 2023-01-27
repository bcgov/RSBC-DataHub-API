<template>
    <b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
		<b-card-header header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b>Linkage</b>      
		</b-card-header>
		<b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">
           
            <b-row>   
                <b-col cols="10"> 
                    <label class="ml-1 m-0 p-0"> 
                        The officer determined the following (relationship 
						between driver, owner and the vehicle)
                    </label>                    
					<b-form-checkbox-group
						stacked
                        v-model="linkageInfo.linkage"
                        @change="update"
						:disabled="formPrinted"
						:state="linkageState.linkage">
						<b-form-checkbox value="keys">
							Location of vehicle key(s) (explain below or in 
							the incident details)
						</b-form-checkbox>
						<b-row v-if="linkageInfo.linkage.includes('keys')">   
							<b-col cols="8">
								<label class="ml-1 m-0 p-0"> Where were the keys located? </label>
								<b-form-input
									v-model="linkageInfo.keyLinkageLocation"
									:disabled="formPrinted"
									@input="update"
									:state="linkageState.keyLinkageLocation">
								</b-form-input> 
							</b-col>	
						</b-row>
						<b-form-checkbox value="principal_operator">
							The driver is a principal operator
						</b-form-checkbox>
						<b-form-checkbox value="owner_within">
							The owner was in the vehicle
						</b-form-checkbox>
						<b-form-checkbox value="owner_aware">
							The owner was aware the driver was in possession 
							of the vehicle (explain in the incident details)
						</b-form-checkbox>
						<b-form-checkbox value="transfer">
							Vehicle subject to a transfer notice 
							(explain in the incident details)
						</b-form-checkbox>
						<b-form-checkbox value="other">
							Other (explain in the incident details)
						</b-form-checkbox>
					</b-form-checkbox-group>
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
export default class LinkageCard extends Vue {	
    
    @viState.State
    public viInfo: viFormJsonInfoType;

	@Prop({required: true})
    linkageInfo!: viFormDataInfoType;
	
	@Prop({required: true})
	linkageState!: viFormStatesInfoType;

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
        this.recheckStates()
    }

	public recheckStates(){
        this.$emit('recheckStates')
    }
 
}
</script>

<style scoped>

</style>