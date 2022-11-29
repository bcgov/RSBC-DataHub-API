<template>
	<b-col>
		<div v-if="colour.code"  :class="selectedColourClass" > 
			<div class="btn"                
				@click="toggleColour(colour)"
				:class="dynamicClass"
				>
				{{ colour.display_name }}
			</div>
		</div>
		<div v-else>
			
		</div>
	</b-col>
</template>


<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';
import { vehicleColourInfoType} from '@/types/Common';

@Component
export default class ColourSample extends Vue {

	@Prop({required: true})
	colour!: vehicleColourInfoType;

	@Prop({required: true})
	selected!: vehicleColourInfoType[];
	
	get dynamicClass() {
		return 'btn-colour-' + this.colour.colour_class;
	}

	get selectedColourClass() {
		const index = this.selected.findIndex(item => item.code==this.colour.code)
		if (index>-1) {
			return 'selected'
		}
		return ''
	}

	public toggleColour(colour) {
		this.$emit("toggle-colour", colour)
	}

}
</script>

<style lang="scss" scoped>



.selected {
  padding: 2px 2px 2px 2px;
  border: 7px solid red;
}


.btn.btn-colour-blue {
  background-color: blue;
  color: white;
  width: 9rem;
}

.btn.btn-colour-red {
  background-color: red;
  color: white;
  width: 9rem;
}

.btn.btn-colour-green {
  background-color: green;
  color: white;
  width: 9rem;
}

.btn.btn-colour-black {
  background-color: black;
  color: white;
  width: 9rem;
}

.btn.btn-colour-purple {
  background-color: purple;
  color: white;
  width: 9rem;
}

.btn.btn-colour-beige {
  background-color: beige;
  color: black;
  width: 9rem;
}

.btn.btn-colour-brown {
  background-color: saddlebrown;
  color: white;
  width: 9rem;
}

.btn.btn-colour-bronze {
  background-color: #cd7f32;
  color: white;
  width: 9rem;
}

.btn.btn-colour-burgundy {
  background-color: #800020;
  color: white;
  width: 9rem;
}

.btn.btn-colour-copper {
  background-color: #B87333;
  color: white;
  width: 9rem;
}

.btn.btn-colour-ivory {
  background-color: ivory;
  color: black;
  width: 9rem;
}

.btn.btn-colour-darkblue {
  background-color: darkblue;
  color: white;
  width: 9rem;
}

.btn.btn-colour-darkgreen {
  background-color: #013220;
  color: white;
  width: 9rem;
}

.btn.btn-colour-gold {
  background-color: darkgoldenrod;
  color: white;
  width: 9rem;
}

.btn.btn-colour-grey {
  background-color: dimgrey;
  color: white;
  width: 9rem;
}

.btn.btn-colour-lightblue {
  background-color: lightblue;
  color: black;
  width: 9rem;
}

.btn.btn-colour-lightgreen {
  background-color: lightgreen;
  color: black;
  width: 9rem;
}

.btn.btn-colour-orange {
  background-color: orangered;
  color: white;
  width: 9rem;
}

.btn.btn-colour-maroon {
  background-color: maroon;
  color: white;
  width: 9rem;
}

.btn.btn-colour-pink {
  background-color: hotpink;
  color: black;
  width: 9rem;
}

.btn.btn-colour-silver {
  background-color: silver;
  color: black;
  width: 9rem;
}

.btn.btn-colour-tan {
  background-color: tan;
  color: black;
  width: 9rem;
}

.btn.btn-colour-turquoise {
  background-color: turquoise;
  color: black;
  width: 9rem;
}

.btn.btn-colour-white {
  background-color: white;
  border: solid 1px black;
  color: black;
  width: 9rem;
}

.btn.btn-colour-yellow {
  background-color: yellow;
  color: black;
  width: 9rem;
}

.btn.btn-colour-other {
  background: repeating-linear-gradient(
	45deg,
	#606dbc,
	#606dbc 10px,
	#465298 10px,
	#465298 20px
  );
  border: solid 1px black;
  color: white;
  width: 9rem;
}

.btn.btn-colour-primer {
  background-color: darkgrey;
  color: black;
  width: 9rem;
}

</style>