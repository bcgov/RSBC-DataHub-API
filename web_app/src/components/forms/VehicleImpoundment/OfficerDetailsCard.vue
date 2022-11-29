<template>

	<b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
		<b-card-header header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b>Officer</b>      
		</b-card-header>
		<b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">
			
			<b-row>
				<b-col>
					<label class="ml-1 m-0 p-0"> Agency <span class="text-danger">*</span></label>
					<b-form-input						
						v-model="officerInfo.agency"
						:disabled="formPrinted"
						@input="update"
						:state="officerState.agency">
					</b-form-input>                                
				</b-col>
				<b-col >
					<label class="ml-1 m-0 p-0"> Badge # </label>
					<b-form-input
						v-model="officerInfo.badge_number"
						:disabled="formPrinted"
						@input="update"
						:state="officerState.badgeNumber">
					</b-form-input>  
				</b-col>
				<b-col >
					<label class="ml-1 m-0 p-0"> Last Name of Peace Officer Serving Prohibition Notice </label>
					<b-form-input
						v-model="officerInfo.officer_name"
						:disabled="formPrinted"
						@input="update"
						:state="officerState.officerName">
					</b-form-input>  
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
export default class OfficerDetailsCard extends Vue {   	
	
	@viState.State
    public viInfo: viFormJsonInfoType;
	
	@Prop({required: true})
    officerInfo!: viFormDataInfoType;
	
	@Prop({required: true})
	officerState!: viFormStatesInfoType;

	dataReady = false;
	
	error = '';
	path = '';
	
	formPrinted = false;		
	userInfo;

	mounted() { 
		this.dataReady = false;				        
		this.formPrinted = Boolean(this.viInfo.printed_timestamp);
        this.extractFields();
        this.dataReady = true;
    }

	public extractFields(){
		this.userInfo = this.$store.state.users;
		this.officerInfo.agency = this.userInfo?.agency;
		this.officerInfo.badge_number = this.userInfo?.badge_number;
		this.officerInfo.officer_name = this.userInfo?.last_name;
	}

	public update(){     
        this.recheckStates()		
    }

	public recheckStates(){
        this.$emit('recheckStates')
    }

 
}
</script>



