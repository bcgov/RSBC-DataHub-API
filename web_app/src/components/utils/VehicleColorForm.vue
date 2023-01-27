<template>
    <div>        
        <div class="row" style="margin:-.75rem 0 -0.35rem 0;">
            <label class="m-0 p-0"> Vehicle Colour(s)</label>
            <b-button variant="primary" class="ml-auto py-0 my-0" @click="vehicleColorModal=true;" >Edit</b-button>
        </div>
        <multiselect                   
            @input="update"
            v-model="formData"
            :options="optionList"
            :disabled="disabled"           
            tag-placeholder="That isn't an option"
            :label="optionLabelField"
            :placeholder="placeholder"
            :max="2"
            :track-by="optionTrackField"
            :multiple="true" 
            :taggable="true"
        />
        <div v-if="error" class="text-danger" >{{error}}</div>

        <b-modal v-model="vehicleColorModal" title="Choose one or two colours" :ok-only="true" size="lg" :hide-header="true">
            <b-card>
                <p class="card-header">
                    <span class="h4">Selected Colour(s)</span>
                    <span class="text-muted"> - click colour tiles below to add / remove</span>
                </p>
                <div class="card-body">
                    <span class="text-muted" v-if="formData.length == 0">None selected</span>
                    <div class="h4" v-else>
                        <multiselect                   
                            @input="update"
                            v-model="formData"
                            :options="optionList"
                            :disabled="disabled"           
                            tag-placeholder="That colour isn't an option"
                            :label="optionLabelField"
                            :placeholder="placeholder"
                            :max="2"
                            :track-by="optionTrackField"
                            :multiple="true" 
                            :taggable="true"
                        />
                    </div>                    
                </div>
            </b-card>
            <b-container>
                <b-row v-for="(row, key) in rows" :key="key">
                    <colour-sample 
                        v-for="colour in row" :key="colour['code']"
                        :colour="colour"
                        :selected="formData"
                        @toggle-colour="toggleColour"
                    />                    
                </b-row>
            </b-container>
        </b-modal>
    </div>
</template>

<script lang="ts">
    import { Component, Vue, Prop } from 'vue-property-decorator';    
    import Multiselect from 'vue-multiselect'
    import ColourSample from "./ColourSample.vue";

    @Component({
        components: {
            Multiselect,
            ColourSample
        },
    })
    export default class VehicleColorForm extends Vue {

        @Prop({required: true})
        data!: any;

        @Prop({required: true})
        label!: string;

        @Prop({required: true})
        dataField!: string;
    
        @Prop({required: true})
        optionList!: any[];

        @Prop({required: true})
        optionLabelField!: string;
        
        @Prop({required: true})
        optionTrackField!: string;

        @Prop({required: false, default: false})
        disabled!: boolean;

        @Prop({required: false, default: ''})
        placeholder!: string;

        @Prop({required: false, default: ''})
        error!: string;

        formData=[]
        maxColumns=4

        vehicleColorModal=false

        mounted(){
            if(this.data[this.dataField][this.optionLabelField])
                this.formData=this.data[this.dataField]
        }

        get rows() {
            const rows = []
            const rowCount = Math.ceil(this.optionList.length / this.maxColumns)
            for (let row = 0; row < rowCount; row++) {
                const colorsInRow = this.optionList.slice(row * this.maxColumns, row * this.maxColumns + this.maxColumns);
                if(colorsInRow.length < this.maxColumns){
                    for(let i=0; i<(this.maxColumns-colorsInRow.length); i++ )
                        colorsInRow.push({code: '', display_name: '', colour_class:''})
                }
                rows.push(colorsInRow)
            }
            return rows
        }
        
        public toggleColour(colour) {
            const index = this.formData.findIndex(item => item.code==colour.code)
            if(index>-1){
                this.formData.splice(index, 1);
            }else if(this.formData.length<2){
                this.formData.push(colour)
            }
            this.update()
        }

        public update(){
            this.data[this.dataField] = this.formData
            this.$emit('update')
        }        
    }

</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style scoped lang="scss">

    label{
            font-size: 16pt;
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
</style>
