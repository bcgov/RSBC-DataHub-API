<template>
    <div>

        <div class="row margin-top-n0-40" style="font-size:5.9pt; margin:0.15rem 0 0 0;">

            <table class="border-0 border-dark text-left" style="width:100%; line-height:0.5rem;">

                <tr style="height:0.01rem; line-height:0.01rem; border-right:0px solid #151515;">                                                         
                    <td v-for="inx in Array(101)" :key="inx" class="border-0 border-dark" style="width:1%;" />                                                                                   
                </tr>              
<!-- <ROW1> -->                          
                <tr style="height:1.75rem; line-height:0.95rem;">
                    <td class="" style="" colspan="70">MV2906 (102018)</td>                                                            
                    <td class="answer" style="font-size:8pt" colspan="30">{{copyType}}</td>
                </tr>
            </table>
        </div>
    </div>           
</template>     
<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';


@Component
export default class Form12hTable6 extends Vue {

    @Prop({required:true})
    copyType!: string;
   
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

.margin-top-n0-40{
    margin-top: -0.4rem !important;
}

.margin-top-n0-25{
    margin-top: -0.25rem !important;
}

</style>