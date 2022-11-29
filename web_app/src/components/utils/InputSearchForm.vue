<template>
    <div>
        <multiselect
            :class="error? 'err':''"                   
            @input="update"
            v-model="formData"
            :options="optionList"
            :disabled="disabled"           
            tag-placeholder="That isn't an option"
            :label="optionLabelField"
            :placeholder="placeholder"
        />
        <div v-if="error" style="font-size:10pt;" class="text-danger" >{{error}}</div>
    </div>
</template>

<script lang="ts">
    import { Component, Vue, Prop } from 'vue-property-decorator';    
    import Multiselect from 'vue-multiselect'

    @Component({
        components: {
            Multiselect
        },
    })
    export default class InputSearchForm extends Vue {

        @Prop({required: true})
        data!: any;

        @Prop({required: true})
        dataField!: string;
    
        @Prop({required: true})
        optionList!: any[];

        @Prop({required: true})
        optionLabelField!: string;

        @Prop({required: false, default: false})
        disabled!: boolean;

        @Prop({required: false, default: ''})
        placeholder!: string;

        @Prop({required: false, default: ''})
        error!: string;

        formData=''

        mounted(){
            if(this.data[this.dataField][this.optionLabelField])
                this.formData=this.data[this.dataField]
        }

        public update(){
            this.data[this.dataField] = this.formData
            this.$emit('update')
        }

    }

</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style scoped lang="scss">

    ::v-deep .err .multiselect__tags{
        font-size: 12.5pt !important;background: #ebc417; 
        min-height: 2.9rem;
        .multiselect__single{
            font-size: 13.5pt !important;
            margin-top: 0.3rem;
        }       
    }

    ::v-deep .multiselect__tags{
        font-size: 12.5pt !important;
        min-height: 2.9rem;
        .multiselect__single{
            font-size: 13.5pt !important;
            margin-top: 0.3rem;
        }       
    }
    ::v-deep .multiselect__select{
        min-height: 2.7rem;      
    }
    // ::v-deep .multiselect__content-wrapper{
    //     color: rgb(0, 255, 234);
    // }

    input.is-invalid {
		background: #ebc417;
	}
</style>
