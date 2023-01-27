<template>
    <div class="text-center important-notice" style="">

<!-- IMPORTANT NOTICE    -->
        <div style="font-size:14pt; font-weight:bold; line-height:2rem; margin-top:0.25rem;">IMPORTANT NOTICE</div>
        <div style="font-size:13pt; line-height:1.4rem; text-align:justify; margin:1rem 2rem;">
            Be warned that if you drive a motor vehicle while
            suspended, the following section of the Motor
            Vehicle Act will apply:
        </div>      

<!-- RIGHT OF REVIEW -->
        <div class="text-left" style="font-size:13pt; font-weight:bold; line-height:2rem;margin:3rem 1rem 0 2rem;">Driving While Suspended</div>
        <div class="row" style="font-size:11pt; line-height:1.10rem; text-align:justify; margin:1rem 1.75rem;">
            <div class="" style="width:15%;">
                90.4 (1)
            </div>
            <div style="width:85%; text-align:justify;">
                A person who holds a driver’s licence on which
                a condition has been imposed under section 25
                (10.1) commits an offence if the person drives
                a motor vehicle on a highway or industrial road
                knowing that the person’s driver’s licence has been
                suspended under section 90.1 or 90.3.           
            </div>
        </div>
       

    </div>           
</template>     
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';


@Component
export default class Form12Notice extends Vue {

    
}

</script>

<style scoped>

.answer {
    color: rgb(3, 19, 165);
    font-size: 7pt;
    font-weight: 600;
}


.important-notice{
    font-size: 8.5pt !important;
    line-height: 0.95rem !important;
}

.margin-top-0{
    margin-top: 0rem !important;
}

</style>