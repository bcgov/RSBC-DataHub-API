<template>
    <div v-if="dataReady" class="outer-page text-center review-instructions" style="font-size:6pt;line-height:0.7rem;">

<!-- < PART - 1 > -->
<!-- REVIEW INSTRUCTIONS    -->        
        <div class="line-height-2 review-title1 margin-top-0-5" style="font-size:9pt; font-weight:bold; line-height:0.9rem; margin-top:0.15rem;text-decoration:underline;">REVIEW INSTRUCTIONS AND OTHER IMPORTANT INFORMATION</div>
        <div class="review-title2" style="font-weight:bold; line-height:1rem; margin-top:0.25rem;">REVIEW INSTRUCTIONS</div>        
        <div style="text-align:justify;">
            No review is available when a vehicle is impounded for 3 or 7 days. Under section 256 of the Motor Vehicle Act (MVA), the owner of a motor vehicle impounded for 30 days or longer may, within 15 days of
            the impoundment, apply to the Superintendent of Motor Vehicles (the “Superintendent”) for a review. The owner must: (1) file an application with the Superintendent at any Driver Licensing Office, and (2) pay
            the prescribed hearing fee. Before filing the application for review, the owner may request a copy of all the evidence the Superintendent will consider during the review. The owner may also attach any written
            statement or other evidence they wish the Superintendent to consider. To ensure all written evidence is considered, the Superintendent must receive it before the scheduled review date.
        </div>
        <div style="text-align:justify;margin-top:0.25rem;">
           The owner may request an oral hearing at the time of application by paying the prescribed oral hearing fee. If the applicant requests an oral hearing and fails to appear on the date, and at the time and place
            arranged for the hearing without prior notice to the Superintendent, the applicant’s right to an oral hearing is deemed to have been waived, and the review will be conducted based on any written evidence
            that is available. The filing of an application for review does not stay the impoundment of the motor vehicle.
        </div>
<!-- PERIOD OF IMPOUNDMENT -->
        <div class="review-title2" style=" font-weight:bold; line-height:1rem; margin-top:0.25rem;">PERIOD OF IMPOUNDMENT</div>
        <div style="text-align:justify;">
            If an eligible owner does not apply for a review under the MVA section 256, the vehicle will remain impounded until it is eligible for release. In the case of a 7 day impoundment under the MVA section 251,
            the vehicle will be impounded for 30 days or 60 days if the records of the Superintendent indicate that the owner has, within the two years before the date of this impoundment, owned one or more vehicles
            that have been subject to impoundment. The Superintendent will notify the owner and the impound lot operator when the impoundment term is 30 or 60 days.
        </div>
<!-- DISPOSAL OF UNCLAIMED VEHICLES -->
        <div class="review-title2" style=" font-weight:bold; line-height:1rem; margin-top:0.25rem;">DISPOSAL OF UNCLAIMED VEHICLES</div>
        <div style="text-align:justify; border-bottom:1px solid #151515; padding-bottom:1rem;">
            If the owner of a motor vehicle does not pay the towing and storage charges associated with the impoundment, the vehicle may be disposed of after the expiry of the impoundment under the Warehouse
            Lien Act, or under the MVA section 255(7). If an owner does not claim a vehicle, the Superintendent may direct the Insurance Corporation of British Columbia to refuse to issue the owner a driver’s licence,
            a vehicle licence and corresponding number plates, or any permit until payment has been made to the impound lot operator (ILO) that stored the vehicle.
        </div> 
             

<!-- < PART - 2 > -->
<!-- INFORMATION FOR DRIVERS   -->        
        <div class="line-height-2 review-title1 margin-top-0-5" style="font-size:9pt; font-weight:bold; line-height:0.9rem; margin-top:0.15rem;text-decoration:underline;">INFORMATION FOR DRIVERS</div>
        <div class="review-title2" style=" font-weight:bold; line-height:1rem; margin-top:0.25rem;">REASONS FOR IMPOUNDMENT</div>        
        <div style="text-align:justify;">
            The notice of impoundment indicates the reason(s) the vehicle you were driving was impounded. Under the Motor Vehicle Act, these reasons are:
        </div>
        <ul class="text-left mb-0">
            <li>Driving while prohibited or with a suspended driver’s licence.</li>
            <li>Driving without a valid licence having been previously convicted for the same offence.</li>
            <li>Committing an excessive speeding offence (more than 40 km/h over the speed limit).</li>
            <li> Being involved in a street race (see section 250 of the Motor Vehicle Act at <span style="text-decoration:underline;">www.bclaws.ca</span> for a full definition).</li>
            <li style="text-align:justify;">
                Stunt driving, which includes activities such as lifting any or all of a vehicle’s tires off the road surface, causing a vehicle to lose traction, causing the vehicle to spin, driving in an oncoming lane longer
                than necessary to pass, blocking other vehicles or driving too close to another vehicle, pedestrian or fixed object (see section 250 of the Motor Vehicle Act at 
                <span style="text-decoration:underline;">www.bclaws.ca</span> for a full definition).
            </li>
            <li>Failing to ride properly astride a motorcycle.</li>
            <li>Failing to obey learner/novice motorcycle restrictions and conditions.</li>
            <li>Being served with an immediate roadside prohibition for drinking and driving.</li>
        </ul>
<!-- EARLY RELEASE FOR UNLICENSED DRIVER IMPOUNDMENTS -->
        <div class="review-title2" style=" font-weight:bold; line-height:1rem; margin-top:0.25rem;">EARLY RELEASE FOR UNLICENSED DRIVER IMPOUNDMENTS</div>
        <div style="text-align:justify;">
            If the vehicle was impounded because you were “Driving without a valid driver’s licence, and with a notice on the driving record indicating a previous conviction for driving while unlicensed”, and for no other
            reason, the vehicle can be released immediately if you obtain a valid British Columbia driver’s licence. Bring a copy of the notice of impoundment with you to a Driver Licensing Office when you apply for a
            driver’s licence. If you do not own the vehicle you were driving, the owner should attend with you or provide written authorization for you or another person to retrieve the vehicle from the impound lot.
            For the location of your nearest Driver Licensing Office <span style="text-decoration:underline;">visit www.icbc.com</span>.
        </div>
<!-- DUTY OF DRIVER -->
        <div class="review-title2" style=" font-weight:bold; line-height:1rem; margin-top:0.25rem;">DUTY OF DRIVER</div>
        <div style="text-align:justify;">
            Under section 251(8) of the Motor Vehicle Act, a driver who is not the owner of the vehicle must make all reasonable efforts to notify the owner of the impounded vehicle of the impoundment as soon
            as practicable.
        </div>

<!-- < PART - 3 > -->
<!-- INFORMATION FOR VEHICLE OWNERS   -->        
        <div class="line-height-2 review-title1 margin-top-1" style="font-size:9pt; font-weight:bold; line-height:1rem; margin-top:0.5rem;text-decoration:underline;">INFORMATION FOR VEHICLE OWNERS</div>
        <div class="review-title2" style=" font-weight:bold; line-height:1rem; margin-top:0.25rem;">HOW ARE IMPOUNDMENT DAYS CALCULATED?</div>        
        <div style="text-align:justify;">
            Vehicle impoundment terms are calculated in full days. Partial days, including the day the vehicle was impounded do not count.
        </div>
<!-- EARLY DISPOSAL AGREEMENT -->
        <div class="review-title2" style=" font-weight:bold; line-height:1rem; margin-top:0.25rem;">EARLY DISPOSAL AGREEMENT</div>
        <div style="text-align:justify;">
            If you do not intend to claim your vehicle following an impoundment you may enter into an early disposal agreement with the impound lot operator (ILO). Under this agreement you transfer ownership of the
            vehicle to the ILO and in exchange do not accumulate the full costs and charges that normally apply to a full length impoundment. Any vehicle transferred under such an agreement cannot be registered
            again for use on a highway.
        </div>

<!-- WHO CAN APPLY FOR A REVIEW AND ON WHAT GROUNDS? -->
        <div class="line-height-1" style="font-weight:bold; line-height:0.5rem; margin-top:0.25rem;">WHO CAN APPLY FOR A REVIEW AND ON WHAT GROUNDS?</div>
        <div class="review-title2 line-height-1" style="line-height:1rem; text-decoration:underline;"><i>A review is not available for a 3-day or 7-day impoundment.</i></div>
        <div style="text-align:justify;">
            An owner who was not the driver may apply for a review on the following grounds:
        </div>
        <ul class="text-left mb-1">
            <li>Reasonable care and diligence was taken in entrusting the vehicle to another driver.</li>
            <li>The driver took the vehicle without the owner’s knowledge or consent.</li>
            <li>The person driving the vehicle was not prohibited or suspended.</li>
            <li>The person driving the vehicle held a valid driver’s licence or was exempt from the requirement to hold a licence.</li>
            <li>A notice to impound the vehicle of an unlicensed driver should not have been on his or her driving record.</li>
        </ul>
        <div style="text-align:justify;">
            An owner who was the driver may apply for a review on the following grounds:          
        </div>
        <ul class="text-left mb-1">
            <li>He or she was neither prohibited nor suspended, or had no reason to believe they were prohibited or suspended.</li>
            <li>He or she held a valid driver’s licence or was exempt from the requirement to hold a licence.</li>
            <li>A notice to impound the vehicle of an unlicensed driver should not have been on his or her driving record.</li>
        </ul>
        <div style="text-align:justify;">
            A cohabitant of an owner, who also holds a valid driver’s licence and with no reasonable alternative form of transportation may apply for a review on the following grounds:
        </div>
        <ul class="text-left mb-1">
            <li>He or she will suffer a loss or curtailment of employment or educational opportunities.</li>
            <li>The impoundment will prevent the cohabitant, or a person under their care, from obtaining medical treatment.</li>           
        </ul>
        <div style="text-align:justify;">
            Business owners may apply for early release of a vehicle if they can demonstrate that:
        </div>
        <ul class="text-left mb-1">
            <li>The vehicle is used in an active sole proprietorship, partnership or company (i.e. a business),</li>
            <li>There is a reasonable prospect of earning income that is dependent on the impounded vehicle, <span style="text-decoration:underline;">and</span></li>
            <li>That the continued impoundment would impose an economic hardship on the business.</li>
        </ul>
        <div style="text-align:justify;">
            More information on the various review grounds, including review and applicable vehicle release fees is available at <span style="text-decoration:underline;">www.gov.bc.ca/roadsafetybc</span>.
        </div>
<!-- CLAIMING YOUR VEHICLE AFTER THE IMPOUNDMENT -->
        <div class="review-title2" style=" font-weight:bold; line-height:1rem; margin-top:0.25rem;">CLAIMING YOUR VEHICLE AFTER THE IMPOUNDMENT</div>
        <div style="text-align:justify;">
            At the end of a 3 or 7 day impoundment the vehicle may be claimed directly from the impound lot. If the impoundment is for 30 or 60 days, you will need to attend a Driver Licensing Office to request release
            of the vehicle. The Driver Licensing Office will fax an order of release to the impound lot, and the owner, or someone authorized by the owner, will be able to claim the vehicle. The vehicle owner is
            responsible for paying all towing and storage fees to the impound lot operator. For the location of your nearest Driver Licensing Office visit 
            <span style="text-decoration:underline;">www.icbc.com</span>.
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
export default class FormViNotice extends Vue {

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


.review-instructions{
    font-size: 7pt !important;
    line-height: 0.95rem !important;
}

.review-title1{
    font-size: 10pt !important;
}

.review-title2{
    font-size: 7.5pt !important;
}

.line-height-2{
    line-height: 2rem !important;
}

.line-height-1{
    line-height: 1rem !important;
}

.margin-top-0-5{
    margin-top: 0.5rem !important;
}

.margin-top-1{
    margin-top: 1rem !important;
}

.margin-top-0{
    margin-top: 0rem !important;
}
.outer-page{
    margin-top: 3rem !important;
}

</style>