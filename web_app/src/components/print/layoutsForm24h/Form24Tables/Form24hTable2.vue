<template>
    <div v-if="dataReady">

        <div class="row notice_class" style="font-size:7pt; margin:0.25rem 0 0 0; padding:0rem;">

            <table class="text-left" style="width:100%; border:2px solid #151515; line-height:0.5rem;">
                
                <tr style="height:0.01rem; line-height:0.01rem;">                    
                    <td v-for="inx in Array(100)" :key="inx" class="" style="width:1%;" />                                                                                   
                </tr>              
<!-- <ROW1> -->
                <tr class="lineheight0-50" style="height:0.5rem; line-height:1rem;">
                    <td class="text-center" style="font-size:9pt" colspan="100"><b>NOTICE OF DRIVING PROHIBITION</b></td>                                                                        
                </tr>
                <tr style="height:1.0rem;line-height:0.75rem;">
                    <td class="" colspan="100"> 
                        <div style="margin:0 0.5rem; font-size:8.0pt; text-align:justify;"> 
                            You are prohibited under section 215 of the Motor Vehicle Act from driving a motor
                            vehicle for 24 hours commencing at:                            
                        </div>
                    </td>                                                                          
                </tr>
                <tr style="height:0.25rem;line-height:0.25rem;">
                    <td class="" colspan="100" />
                </tr>

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
                <tr style="height:1.25rem;line-height:0.75rem;">
                    <td class="" colspan="3" />
                    <td class="" style="border-bottom:1px solid #151515;" colspan="94" />
                    <td class="" colspan="3" />
                </tr>
                <tr class="lineheight0-5" style="height:0.5rem; line-height:0.75rem;">
                    <td class="text-center" style="font-size:6pt;" colspan="100">SIGNATURE OF PERSON ACKNOWLEDGING</td>
                </tr>


            </table>
        </div>
    </div>           
</template>     
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { namespace } from "vuex-class";

import "@/store/modules/forms/mv2634";
const mv2634State = namespace("MV2634");

import CheckBox from "../../pdfUtil/CheckBox.vue";
import { twentyFourHourFormJsonInfoType } from '@/types/Forms/MV2634';


@Component({
    components:{       
        CheckBox           
    }
})
export default class Form24hTable2 extends Vue {

    @mv2634State.State
    public mv2634Info: twentyFourHourFormJsonInfoType;   

    dataReady = false;

    formData;

    mounted(){
        this.dataReady = false;
        this.extractInfo();
        this.dataReady = true;
    }

    public extractInfo(){

        const form24 = this.mv2634Info.data

        this.formData = {
            suspensionTime: '',
            suspensionDay:'',
            suspensionMonth: '',
            suspensionYear: ''            
        }

        if (form24.prohibitionStartTime){
            this.formData.suspensionTime = 
                form24.prohibitionStartTime.substr(0,2)+ ':' + form24.prohibitionStartTime.substr(2,2);
        }

        if (form24.prohibitionStartDate){
            this.formData.suspensionDay = Vue.filter('extract-date')( form24.prohibitionStartDate).day.toUpperCase();
            this.formData.suspensionMonth = Vue.filter('extract-date')( form24.prohibitionStartDate).month.toUpperCase();
            this.formData.suspensionYear = Vue.filter('extract-date')( form24.prohibitionStartDate).year;
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