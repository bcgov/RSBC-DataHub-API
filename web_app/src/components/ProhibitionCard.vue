<template>
    <div class="card border-light bg-secondary">
		<div class="card-header text-white text-left font-weight-bold small pl-3 pt-1 pb-1 bg-primary">
			{{ form.full_name }}
		</div>
		<div class="card-body bg-light">
			<p class="card-text text-dark">{{ form.description }}</p>
			<p class="card-text">
				<small class="text-muted">
				IDs available: {{ getFormTypeCountInfo()[form.form_type] }}
				</small>
			</p>

			<!-- <router-link class="text-white" v-if="isFormAvailable" :to="{
				name: form.form_type,
				params: { id: getNextAvailableUniqueIdByType(form.form_type)}}">
				<button type="submit" class="btn btn-primary" :id="form.full_name">
					New {{ form.label }} Form
				</button>
			</router-link> -->
			<button @click="startNewForm()" class="btn btn-primary" v-if="isFormAvailable" :id="form.full_name">
				New {{ form.label }} Form
			</button>
			<button type="submit" class="btn btn-primary" v-if="! isFormAvailable" :disabled="! isFormAvailable" :id="form.full_name">
				New {{ form.label }} Form
			</button>

		</div>
    </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import {getFormTypeCount} from "@/utils/forms"

@Component
export default class ProhibitionCard extends Vue {

	@Prop({required: true})
	form: any;

	public getFormTypeCountInfo(){
		return getFormTypeCount()
	}

    public getNextAvailableUniqueIdByType(form_type) {
        // console.log("inside getNextAvailableUniqueIdByType()", form_type)
        for (const form_id in this.$store.state.forms[form_type]) {
            if( ! ("data" in this.$store.state.forms[form_type][form_id])) {                
                return form_id
            }
        }
    }
	
	public startNewForm(){
		const form_id = this.getNextAvailableUniqueIdByType(this.form.form_type)
		const payload = {form_type: this.form.form_type, form_id: form_id}
		// console.log(payload)
		this.$store.commit("Common/editExistingForm",payload)
		Vue.nextTick(()=>
			this.$router.push({   
				name: this.form.form_type,
				params: { id: form_id}
			})
		)
	}

	get isFormAvailable() {
		return getFormTypeCount()[this.form.form_type] > 0 && ! this.form.disabled
	}

}

// export default {
//   name: "ProhibitionCard",
//   props: {
//       form: {}
//   },
//   computed: {
//     // ...mapGetters(["getNextAvailableUniqueIdByType"]),
//     isFormAvailable() {
//       return getFormTypeCount()[this.form.form_type] > 0 && ! this.form.disabled
//     }
//   },
//   methods: {
//     getNextAvailableUniqueIdByType(form_type) {
//         console.log("inside getNextAvailableUniqueIdByType()", form_type)
//         for (const form_id in this.$store.state.forms[form_type]) {
//             if( ! ("data" in this.$store.state.forms[form_type][form_id])) {
//                 const payload = {form_type: form_type, form_id: form_id}
//                 console.log(payload)
//                 this.$store.commit("Common/editExistingForm",payload)
//                 return form_id
//             }
//         }
//     },
//     getFormTypeCountInfo(){
//       return getFormTypeCount()
//     }
//   }
// }
</script>
