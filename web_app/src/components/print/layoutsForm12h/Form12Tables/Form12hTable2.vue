<template>
    <div v-if="dataReady">

        <div class="row notice_class" style="font-size:7pt; margin:0.25rem 0 0 0; padding:0rem;">

            <table class="text-left" style="width:100%; border:2px solid #151515; line-height:0.5rem;">
                
                <tr style="height:0.01rem; line-height:0.01rem;">                    
                    <td v-for="inx in Array(100)" :key="inx" class="" style="width:1%;" />                                                                                   
                </tr>
                <tr style="height:0.5rem;line-height:0.5rem;">
                    <td class="" colspan="100" />
                </tr>              

<!-- <ROW1> -->                
                <tr style="height:1.0rem;line-height:0.75rem;">
                    <td class="" colspan="100"> 
                        <div style="margin:0 0.5rem; font-size:8.5pt; text-align:justify;"> 
                            This suspension from driving will be recorded on your British
                            Columbia driving record and may be considered by the
                            Superintendent of Motor Vehicles when reviewing your driving
                            record. 
                        </div>
                    </td>                                                                          
                </tr>
                <tr style="height:0.5rem;line-height:0.5rem;">
                    <td class="" colspan="100" />
                </tr>

<!-- <ROW2> -->                
                <tr style="height:1.0rem;line-height:0.75rem;">
                    <td class="" colspan="100"> 
                        <div style="margin:0 0.5rem; font-size:8.5pt; text-align:justify;"> 
                            YOUR LICENCE TO DRIVE IS HEREBY SUSPENDED UNDER
                            SECTION 90.3 OF THE MOTOR VEHICLE ACT FOR A PERIOD OF
                            12 HOURS COMMENCING AT:
                        </div>
                    </td>                                                                          
                </tr>
                <tr style="height:0.75rem;line-height:0.75rem;">
                    <td class="" colspan="100" />
                </tr>
<!-- <ROW3> --> 
                <tr style="height:1.0rem;line-height:0.75rem;">
                    <td class="" style="border-bottom:1px solid white;" colspan="3" />
                    <td class="text-center answer" style="border-bottom:1px solid #151515;" colspan="12">{{formData.suspensionTime}}</td>
                    <td class="text-center"  style="border-bottom:1px solid white;" colspan="18">hours on the</td>
                    <td class="text-center answer" style="border-bottom:1px solid #151515;" colspan="10">{{formData.suspensionDay}}</td>
                    <td class="text-center"  style="border-bottom:1px solid white;" colspan="12">day of </td>
                    <td class="text-center answer" style="border-bottom:1px solid #151515;" colspan="24">{{formData.suspensionMonth}}</td>
                    <td class="text-center"  style="border-bottom:1px solid white;" colspan="8">year </td>
                    <td class="text-center answer" style="border-bottom:1px solid #151515;" colspan="10">{{formData.suspensionYear}}</td>
                    <td class=""  style="border-bottom:1px solid white;" colspan="3"></td>
                </tr>
                <tr style="height:1.5rem;line-height:0.75rem;">
                    <td class="" colspan="3" />
                    <td class="" style="border-bottom:1px solid #151515;" colspan="94" />
                    <td class="" colspan="3" />
                </tr>
                <tr class="lineheight0-5" style="height:0.5rem; line-height:0.95rem;">
                    <td class="text-center" style="font-size:6pt;" colspan="100">SIGNATURE OF PERSON ACKNOWLEDGING SUSPENSION</td>
                </tr>


            </table>
        </div>
    </div>           
</template>     
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { namespace } from "vuex-class";

import "@/store/modules/forms/mv2906";
const mv2906State = namespace("MV2906");

import CheckBox from "../../pdfUtil/CheckBox.vue";
import { twelveHourFormJsonInfoType } from '@/types/Forms/MV2906';

@Component({
    components:{       
        CheckBox           
    }
})
export default class Form12hTable2 extends Vue {

    @mv2906State.State
    public mv2906Info: twelveHourFormJsonInfoType;   

    dataReady = false;
    formData;

    mounted(){
        this.dataReady = false;
        this.extractInfo();
        this.dataReady = true;
    }

    public extractInfo(){

        const form12 = this.mv2906Info.data

        this.formData = {
            suspensionTime: '',
            suspensionDay:'',
            suspensionMonth: '',
            suspensionYear: ''            
        }

        if (form12.prohibitionStartTime){
            this.formData.suspensionTime = 
                form12.prohibitionStartTime.substr(0,2)+ ':' + form12.prohibitionStartTime.substr(2,2);
        }

        if (form12.prohibitionStartDate){
            this.formData.suspensionDay = Vue.filter('extract-date')( form12.prohibitionStartDate).day.toUpperCase();
            this.formData.suspensionMonth = Vue.filter('extract-date')( form12.prohibitionStartDate).month.toUpperCase();
            this.formData.suspensionYear = Vue.filter('extract-date')( form12.prohibitionStartDate).year;
        }
        
    }
    
}

</script>

<style scoped>

.answer {
    color: rgb(3, 19, 165);
    font-size: 7pt;
    font-weight: 600;
}

.lineheight0-25{
    line-height:0.25rem !important;
}
.lineheight0-50{
    line-height:0.5rem !important;
}
.lineheight0-75{
    line-height:0.75rem !important;
}

.notice_class{
    margin: 0 0 !important;
    padding: 0 0.2rem !important;
}

</style>