<template>
    <div :class="checkboxClass" >
        <div
            :style="{position: 'absolute',
                margin: boxMargin,            
                border: '1px solid #151515 !important',             
                width: boxSize, 
                transform:'translate('+shiftBox+')',           
                height: boxSize,           
            }">
            <div :style="{transform:'translate('+shiftmark+')',color:checkColor, fontSize:checkFontSize}" v-html="getCheck()"/>
        </div> 
        <div v-if="text" :style="{display:'inline-block', marginLeft: marginLeft, textIndent: 0 }" v-html="text">{{text}}</div>
    </div>

</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

@Component
export default class CheckBox extends Vue {
   
    @Prop({required: true})
    text!: string;

    @Prop({required: true})
    check!: string;

    @Prop({default:'#151515'})
    checkColor!: string;

    @Prop({default:'10pt'})
    checkFontSize!: string;

    @Prop({default: '0px,-2px'})
    shiftmark!: string;

    @Prop({default: '0px,4px'})
    shiftBox!: string;

    @Prop({default: '1em'})
    boxSize!: string;

    @Prop({default: '-0.25rem 0 0 -1rem'})
    boxMargin!: string;

    @Prop({default: '1.75rem'})
    marginLeft!: string;

    @Prop({default: 'checkbox'})
    checkboxClass!: string;


    public getCheck(){
        if(this.check=='?') return "&#63"
        else if(this.check) return "&#10003"
        return ""
    }

}
</script>