<template>
    <b-card v-if="dataReady" header-tag="header" bg-variant="gov-accent-grey" border-variant="light" >		
        <b-card-header class="text-left h3" header-bg-variant="light" header-border-variant="bright" header-text-variant="dark">            
            <b>Vehicle Disposition</b>      
        </b-card-header>
        <b-card border-variant="light" bg-variant="time" text-variant="dark" class="my-0">

            <b-row class="text-left">   
                <b-col cols="3">
                    <label class="m-0 mb-2 p-0"> Vehicle Towed? <span class="text-danger">*</span></label>
                    <b-form-radio-group
                        :class="(vdState.vehicleImpounded==null)?'':'border border-danger is-invalid'"
                        size="lg" 
                        stacked
                        v-model="vdInfo.vehicleImpounded"                    
                        :options="responseOptions"
                        @change="update"
                        :disabled="formPrinted"
                        :state="vdState.vehicleImpounded">                   
                    </b-form-radio-group> 
                </b-col>                
            </b-row>
            <b-card no-body v-if="vdInfo.vehicleImpounded" class="bg-time border-0">
                <b-row class="text-left">   
                    <b-col cols="3"> 
                        <label class="m-0 mb-2 p-0"> Location of Keys? <span class="text-danger">*</span></label>
                        <b-form-radio-group
                            :class="(vdState.locationOfKeys==null)?'':'border border-danger is-invalid'" 
                            size="lg"
                            stacked
                            v-model="vdInfo.locationOfKeys"                    
                            :options="keyLocationOptions"
                            @change="update"
                            :disabled="formPrinted"
                            :state="vdState.locationOfKeys">                   
                        </b-form-radio-group> 
                    </b-col>                
                </b-row>
                <b-card no-body class="bg-timelight border-0">
                    <b-row class="text-left mx-1 mt-0">
                        <b-col>
                            <label class="m-0 p-0"></label>
                            <input-search-form-imp-lot
                                :data="vdInfo"
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
                            v-model="vdInfo.impoundLot.name"
                            @input="update"
                            :state="vdState.impoundLotName">
                        </b-form-input> 
                    </b-row>

                    <b-row class="text-left mx-1">
                        <b-col>
                            <label class="m-0 p-0"> Public lot address <span class="text-danger">*</span></label>
                            <b-form-input
                                size="lg"
                                placeholder="Public lot address"
                                v-model="vdInfo.impoundLot.lot_address"
                                :disabled="formPrinted"
                                @input="update"
                                :state="vdState.impoundLotAddress">
                            </b-form-input>                                
                        </b-col>
                        <b-col >
                            <label class="m-0 p-0"> City <span class="text-danger">*</span></label>
                            <b-form-input
                                size="lg"
                                placeholder="City"
                                v-model="vdInfo.impoundLot.city"
                                :disabled="formPrinted"
                                @input="update"
                                :state="vdState.impoundLotCity">
                            </b-form-input>  
                        </b-col>
                        <b-col >					
                            <label class=" m-0 p-0"> Public phone <span class="text-danger">*</span></label>
                            <b-form-input
                                size="lg"
                                placeholder="Public phone"
                                v-model="vdInfo.impoundLot.phone"
                                :disabled="formPrinted"
                                @input="update"
                                :state="vdState.impoundLotPhone">
                            </b-form-input>                             
                        </b-col>                    
                    </b-row>
                </b-card>
            </b-card>


            <b-card no-body v-else-if="vdInfo.vehicleImpounded != null" class="bg-time border-0" >
                <b-row class="text-left">   
                    <b-col cols="4"> 
                        <label class="m-0 mb-2 p-0"> Reason for not towing? <span class="text-danger">*</span></label>
                        <b-form-radio-group
                            :class="(vdState.notImpoundingReason==null)?'':'border border-danger is-invalid'"
                            size="lg"  
                            stacked
                            v-model="vdInfo.notImpoundingReason"                    
                            :options="notImpoundingOptions"
                            @change="update"
                            :disabled="formPrinted"
                            :state="vdState.notImpoundingReason">                   
                        </b-form-radio-group> 
                    </b-col>                
                </b-row> 
                <b-row v-if="vdInfo.notImpoundingReason == 'Released to other driver'" class="text-left">
                    <b-col >
                        <label class="ml-1 m-0 p-0"> Vehicle Released To <span class="text-danger">*</span></label>
                        <b-form-input 
                            size="lg"                           
                            v-model="vdInfo.vehicleReleasedTo"
                            :disabled="formPrinted"
                            @input="update"
                            :state="vdState.vehicleReleasedTo">
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
                                id="dr"
                                v-model="vdInfo.releasedDate"
                                type="text"
                                @input="validateDate(false, false)"
                                :disabled="formPrinted"
                                :state="vdState.releasedDate"
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
                                    @context="validateDate(true, false)"
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
                            v-model="vdInfo.releasedTime"
                            :disabled="formPrinted"
                            @input="validateDate(false, true)"
                            :state="vdState.releasedTime">
                        </b-form-input>
                        <div v-if="timeError" style="font-size:10pt;" class="text-danger text-left m-0 mt-0 p-0">{{timeError}}</div>                              
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

import InputSearchFormImpLot from '@/components/utils/InputSearchFormImpLot.vue'

import "@/store/modules/common";
const commonState = namespace("Common");

import "@/store/modules/forms/mv2906";
const mv2906State = namespace("MV2906");

import { impoundLotOperatorsInfoType, jurisdictionInfoType, provinceInfoType } from '@/types/Common';
import { twelveHourFormStatesInfoType, twelveHourFormDataInfoType, twelveHourFormJsonInfoType } from '@/types/Forms/MV2906';
import Spinner from "@/components/utils/Spinner.vue";

@Component({
    components: {           
        Spinner,
        InputSearchFormImpLot
    }        
}) 
export default class VehicleDispositionCard extends Vue {   

    @commonState.State
    public impound_lot_operators: impoundLotOperatorsInfoType[];	

    @mv2906State.State
    public mv2906Info: twelveHourFormJsonInfoType;

    @Prop({required: true})
    vdInfo!: twelveHourFormDataInfoType;
    
    @Prop({required: true})
    vdState!: twelveHourFormStatesInfoType;

    dataReady = false;
    updateDate=0;
    dateReleased = '';
    dateError = '';
    timeError = '';
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
        {text: 'Left at roadside', value: 'Left at roadside'}
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
            let dateReleased=this.dateReleased.replace('-','')
            dateReleased=dateReleased.replace('-','')
            this.vdInfo.releasedDate=dateReleased
            this.updateDate++;
        }

        let releaseTime='0000'
        
        const timeFormat = /^([0-1][0-9]|2[0-3])[0-5][0-9]$/
        if( !Number(this.vdInfo?.releasedTime) ||
            this.vdInfo?.releasedTime?.length!=4 ||
            timeFormat.test(this.vdInfo?.prohibitionStartTime)==false
        ){
            if(timeInput){
                this.timeError="The input time is invalid!"
                this.vdState.releasedTime=false                
            }
        }else{
            this.timeError=""
            this.vdState.releasedTime = null;
            releaseTime = this.vdInfo.releasedTime;
        }
        
        if(!this.vdInfo.releasedDate) return

        if(!Number(this.vdInfo?.releasedDate)||this.vdInfo?.releasedDate?.length!=8){
            this.dateError="The selected date is invalid!"
            this.vdState.releasedDate=false
        }
        else{ 
                        
            const date = moment(this.vdInfo.releasedDate)
            // const currentDate = moment()
            // const releaseDateTime = this.vdInfo.releasedDate+releaseTime
            // console.log(releaseDateTime)
            
            
            if(!date.isValid()){
                this.dateError="The selected date is invalid!"
                this.vdState.releasedDate=false
            }
            //-TODO-future-work
            // else if(currentDate.format("YYYYMMDDHHmm")< releaseDateTime){
            // 	this.dateError="The selected date/time is before  the prohibition Start Date!"
            //     this.timeError="The selected date/time is before  the prohibition Start Date!"
            // 	this.vdState.releasedDate=false
            // }			
            else{ 
                this.dateError=""
                if(!datePicker){
                    const year = this.vdInfo.releasedDate.slice(0,4)
                    const month = this.vdInfo.releasedDate.slice(4,6)
                    const day = this.vdInfo.releasedDate.slice(6)
                    this.dateReleased = year+'-'+month+'-'+day
                }
                this.vdState.releasedDate=null
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