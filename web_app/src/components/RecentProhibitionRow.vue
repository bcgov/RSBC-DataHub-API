<template>
    <tr v-if="prohibition">
        <td>
            {{ prohibition.data.lastName }},
            {{ prohibition.data.givenName }}
            ({{ prohibition.data.driversNumber }})
        </td>
        <td>{{ prohibition.form_type }}</td>
        <td>{{ getServedStatus(prohibition) }}</td>
        <td><span class="text-muted text-secondary">{{ prohibition.form_id }}</span></td>
        <td>
        <h6 v-if="isFormEditable(prohibition)">
            <b-icon-trash variant="danger" @click="deleteSpecificFormFromTable(prohibition)"></b-icon-trash>&nbsp;
            <b-button @click="editForm()" size="sm" class="m-0 p-0 bg-transparent border-0"> 
                <b-icon-pen variant="primary" scale="0.9" />
            </b-button>
            <!-- <router-link :to="{ name: prohibition.form_type, params: { id: prohibition.form_id}}">
                <b-icon-pen variant="primary"></b-icon-pen>
            </router-link> -->
        </h6>
        <div v-if="! isFormEditable(prohibition)">
            <div v-for="(document, index) in getDocumentsToPrint(prohibition.form_type)" v-bind:key="index">
            <print-documents
                v-if="document.reprint"
                :form_object="prohibition"
                :validate="() => { return true }"
                :variants="document.variants">
                Print again
            </print-documents>
            </div>

        </div>
        </td>
    </tr>
</template>


<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import {getFormTypeCount} from "@/utils/forms"
import PrintDocuments from "@/components/forms/PrintDocuments.vue";
import {deleteSpecificForm} from "@/utils/forms"
import { twelveHourFormJsonInfoType } from '@/types/Forms/MV2906';


@Component({
    components: {
        PrintDocuments
    }
})
export default class ProhibitionCard extends Vue {
    
    @Prop({required: true})
    prohibition: twelveHourFormJsonInfoType;
    
    display_spinner: false

    public editForm(){
        const payload = {form_type: this.prohibition.form_type, form_id: this.prohibition.form_id}
        this.$store.commit("Common/editExistingForm",payload)
		Vue.nextTick(()=>
			this.$router.push({   
				name: this.prohibition.form_type,
				params: { id: this.prohibition.form_id}
			})
		)
    }

    public deleteSpecificFormFromTable(form){
        deleteSpecificForm(form)
    }

    public isFormEditable(form_object){
        return ! (this.$store.state.forms[form_object.form_type][form_object.form_id].printed_timestamp)
    }

    public getServedStatus(form_object){
        if (this.$store.state.forms[form_object.form_type][form_object.form_id].printed_timestamp) {
            return "Printed";
        }
        return "Not Printed"
    }

    public getDocumentsToPrint(form_type){
        return this.$store.state.form_schemas.forms[form_type].documents;
    }
}

// <script>

// import { mapMutations, mapGetters, mapActions } from 'vuex';
// import PrintDocuments from "@/components/forms/PrintDocuments";

// import {deleteSpecificForm} from "@/utils/forms"

// export default {
//   name: "RecentProhibitionRow",
//   props: {
//     prohibition: {}
//   },
//   data() {
//     return {
//       display_spinner: false
//     }
//   },
//   computed: {
//     //...mapGetters([
//       // "isFormEditable", 
//       // "getServedStatus", 
//       //"getDocumentsToPrint"])
//   },
//   methods: {
//     // ...mapMutations(["editExistingForm"]),
//     ...mapActions(["saveFormAndGeneratePDF"]),
//     deleteSpecificFormFromTable(form){
//       deleteSpecificForm(form)
//     },
//     isFormEditable(form_object){
//         return ! (this.$store.state.forms[form_object.form_type][form_object.form_id].printed_timestamp)
//     },
//     getServedStatus(form_object){
//         if (this.$store.state.forms[form_object.form_type][form_object.form_id].printed_timestamp) {
//             return "Printed";
//         }
//         return "Not Printed"
//     },
//     getDocumentsToPrint(form_type){
//         return this.$store.state.form_schemas.forms[form_type].documents;
//     },
//   },
//   components: {
//     PrintDocuments
//   }
// }
// </script>
