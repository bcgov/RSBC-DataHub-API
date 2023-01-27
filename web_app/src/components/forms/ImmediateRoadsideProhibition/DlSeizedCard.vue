<template>
	<b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
		<b-card-header header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
			<b>Driver's Licence</b>      
		</b-card-header>
		<b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">

            <b-row>   
                <b-col cols="3"> 
                    <label class="ml-1 m-0 p-0"> Seized Driver's Licence? <span class="text-danger">*</span></label>
                    <b-form-radio-group 
                        stacked
                        v-model="dsInfo.dlSeized"                    
                        :options="responseOptions"
                        @change="update"
						:disabled="formPrinted"
						:state="dsState.dlSeized">                   
                    </b-form-radio-group> 
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

@Component({
    components: {           
        Spinner
    }        
}) 
export default class DlSeizedCard extends Vue {     

	@irpState.State
    public irpInfo: irpFormJsonInfoType;

	@Prop({required: true})
    dsInfo!: irpFormDataInfoType;
	
	@Prop({required: true})
	dsState!: irpFormStatesInfoType;

	dataReady = false;   
	error = '';
	formPrinted = false;

    responseOptions = [
        {text: 'Yes', value: true},
        {text: 'No', value: false}
    ];    

	mounted() { 
        this.dataReady = false;				        
		this.formPrinted = Boolean(this.irpInfo.printed_timestamp); 
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