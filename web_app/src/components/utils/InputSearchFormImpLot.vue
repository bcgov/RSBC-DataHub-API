<template>
    <div>
        <multiselect                   
            @input="update"
            v-model="formData"
            :options="optionList"
            :disabled="disabled"           
            tag-placeholder="That isn't an option"
            :custom-label="customLabel"
            :placeholder="placeholder"
        />
        <div v-if="error" class="text-danger" >{{error}}</div>
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
    export default class InputSearchFormImpLot extends Vue {

        @Prop({required: true})
        data!: any;

        @Prop({required: true})
        dataField!: string;
    
        @Prop({required: true})
        optionList!: any[];

        @Prop({required: false, default: false})
        disabled!: boolean;

        @Prop({required: false, default: ''})
        placeholder!: string;

        @Prop({required: false, default: ''})
        error!: string;

        formData=''

        mounted(){
            if(this.data[this.dataField]['name'])
                this.formData=this.data[this.dataField]
        }

        public update(){
            if(this.formData){
                this.data[this.dataField] = this.formData
                this.$emit('update')
            }
        }

        public customLabel({city, lot_address, name, phone}){
            return `${name}, ${lot_address}, ${city}, ${phone}`
        }
    }

</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style scoped lang="scss">
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
</style>
