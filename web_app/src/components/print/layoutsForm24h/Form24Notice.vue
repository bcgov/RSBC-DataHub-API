<template>
    <div v-if="dataReady" class="text-center important-notice" style="font-size:7.5pt;line-height:0.85rem;">

<!-- IMPORTANT NOTICE    -->
        <div style="font-size:14pt; font-weight:bold; line-height:2rem; margin-top:0.5rem;">IMPORTANT NOTICE</div>
        <div style="text-align:justify;">
            If a blood alcohol test was not administered and was not a basis for serving
            this notice, you have a right to forthwith request a test to determine your blood
            alcohol level. In the event the test indicates that your blood alcohol level does
            not exceed 50 milligrams of alcohol in 100 milliliters of blood, the prohibition from
            driving is terminated. The prohibition will not appear on your driving record and
            you will be allowed to drive.
        </div>
        <div style="text-align:justify;">
            If a prescribed physical coordination test was not administered and was not the
            basis for serving this notice, you have a right to forthwith request that the peace
            officer submit you to a prescribed physical coordination test to determine whether
            or not your ability to drive is affected by a drug other than alcohol. In the event
            that the prescribed physical coordination test does not indicate that your ability
            to drive is affected by a drug, the prohibition from driving is terminated. The
            prohibition will not appear on your driving record and you will be allowed to drive.
        </div>
        <div style="text-align:justify;">
            You should be aware that if you drive a motor vehicle while prohibited, you are
            subject to a maximum 60-day impoundment of the vehicle you operate, and a
            charge of Driving While Prohibited, which carries a minimum $500 fine, possible
            imprisonment, and an automatic 12-month driving prohibition.
        </div>

<!-- RIGHT OF REVIEW -->
        <div style="font-size:14pt; font-weight:bold; line-height:2rem;margin-top:0.5rem;">RIGHT OF REVIEW</div>
        <div style="text-align:justify;">
            If you were served with this Notice of 24-Hour Prohibition, you may, within 7 days
            of being served, apply to the Superintendent of Motor Vehicles for a review of
            the prohibition. If you apply for a review, you must: (1) file an application with the
            Superintendent at a Driver Services Centre; and (2) pay the prescribed application
            fee. You may attach any written statement or other evidence that you wish the
            Superintendent to consider.
        </div>
        <div style="text-align:justify;">
            After you have applied for a review, the Superintendent will send you a copy of
            the peace officer’s report and allow you to make a further written submission. In
            a review, the prohibition can only be revoked if: (1) you had the right to request
            and the officer failed to administer a test of your blood alcohol level when you
            requested it (alcohol); (2) you had the right to request and the officer failed to
            administer the prescribed physical coordination test when you requested it
            (drugs); or, (3) you were not the driver. No other factors may be considered. If the
            prohibition is revoked on review, it will be removed from your driving record. All
            review application fees are non-refundable, regardless of the review outcome.
        </div>

<!-- BRITISH COLUMBIA DRIVING RECORD -->
        <div style="font-size:14pt; font-weight:bold; line-height:2rem;margin-top:0.5rem;">BRITISH COLUMBIA DRIVING RECORD</div>
        <div style="text-align:justify;">
            Under the Motor Vehicle Act drivers whose driving records meet criteria prescribed
            in the Motor Vehicle Act Regulations are required to complete remedial and ignition
            interlock programs. The criteria may include driving records of drivers with three or
            more 24-hour prohibitions within 5 years. Other prohibitions on your driving record
            combined with this prohibition may also meet the criteria. See RoadSafetyBC’s
            website for more information: www.gov.bc.ca/roadsafetybc
        </div>
        <div style="text-align:justify;">
            <b>Note:</b> Mandatory remedial and ignition interlock program requirements are not
            subject to a reconsideration process. Ignition interlock program requirements
            may be subject to exemption if satisfactory evidence is provided that a chronic
            medical condition prevents you from participating.
        </div>
        <div style="text-align:justify;">
            If your driving record does not meet the criteria, the Superintendent may still
            require you to participate in a remedial or ignition interlock program under section
            25.1 of the Motor Vehicle Act if the Superintendent finds your driving record to
            be unsatisfactory. You may apply for a reconsideration.
        </div>


    </div>           
</template>     
<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';


import CheckBox from "../pdfUtil/CheckBox.vue";

@Component({
    components:{       
        CheckBox           
    }
})
export default class Form24Notice extends Vue {

    // @Prop({required:true})
    // result!: form20DataInfoType;

    dataReady = false;
    driver=['D','R','I','V','E','R']

    mounted(){
        this.dataReady = false;
        // this.extractInfo();
        this.dataReady = true;
    }

    // public extractInfo(){

    //     if (this.result.withdrawingLawyerName == 'Other'){
    //         this.lawyerName = this.result.withdrawingLawyerNameOther;
    //     } else {
    //         this.lawyerName = this.result.withdrawingLawyerName;
    //     }

    //     const index = this.result.objectingParties.indexOf('Other')

    //     if (index != -1){

    //         const partiesList = this.result.objectingParties.splice(index, 1);
    //         partiesList.push(this.result.objectingPartiesOther);
    //         this.parties = partiesList.join(', ');

    //     } else {
    //         this.parties = this.result.objectingParties.join(', ');
    //     }     
           
    // }

    
}

</script>

<style scoped>

.answer {
    color: rgb(3, 19, 165);
    font-size: 7pt;
    font-weight: 600;
}


.important-notice{
    font-size: 7.75pt !important;
    line-height: 0.95rem !important;
}

.margin-top-0{
    margin-top: 0rem !important;
}

</style>