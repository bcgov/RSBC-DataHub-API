<template>
  <b-col>
    <div :class="selectedColourClass">
      <div class="btn"
           @click="toggleColour(colour)"
           :class="dynamicClass"
           >
        {{ colour.display_name }}
      </div>
    </div>
  </b-col>

</template>

<script>
export default {
  name: "ColourSample",
  props: {
    selected: [],
    colour: {
      colour_class: '',
      display_name: '',
    },
  },
  computed: {
    isSelected() {
      let i;
      for(i = 0; i < this.selected.length; i++) {
        if(this.selected[i].code === this.colour.code) {
          return true
        }
      }
      return false;
    },
    dynamicClass() {
      return 'btn-colour-' + this.colour.colour_class;
    },
    selectedColourClass() {
      if (this.isSelected) {
        return 'selected'
      }
      return ''
    }
  },
  methods: {
    toggleColour(colour) {
      this.$emit("toggle-colour", colour)
    }
  }
}
</script>

<style>

.selected {
  padding: 2px 2px 2px 2px;
  border: 5px solid red;
}


.btn.btn-colour-blue {
  background-color: blue;
  color: white;
}

.btn.btn-colour-red {
  background-color: red;
  color: white;
}

.btn.btn-colour-green {
  background-color: green;
  color: white;
}

.btn.btn-colour-black {
  background-color: black;
  color: white;
}

.btn.btn-colour-purple {
  background-color: purple;
  color: white;
}

.btn.btn-colour-beige {
  background-color: beige;
  color: black;
}

.btn.btn-colour-brown {
  background-color: saddlebrown;
  color: white;
}

.btn.btn-colour-bronze {
  background-color: #cd7f32;
  color: white;
}

.btn.btn-colour-burgundy {
  background-color: #800020;
  color: white;
}

.btn.btn-colour-copper {
  background-color: #B87333;
  color: white;
}

.btn.btn-colour-ivory {
  background-color: ivory;
  color: black;
}

.btn.btn-colour-darkblue {
  background-color: darkblue;
  color: white;
}

.btn.btn-colour-darkgreen {
  background-color: #013220;
  color: white;
}

.btn.btn-colour-gold {
  background-color: darkgoldenrod;
  color: white;
}

.btn.btn-colour-grey {
  background-color: dimgrey;
  color: white;
}

.btn.btn-colour-lightblue {
  background-color: lightblue;
  color: black;
}

.btn.btn-colour-lightgreen {
  background-color: lightgreen;
  color: black;
}

.btn.btn-colour-orange {
  background-color: orangered;
  color: white;
}

.btn.btn-colour-maroon {
  background-color: maroon;
  color: white;
}

.btn.btn-colour-pink {
  background-color: hotpink;
  color: black;
}

.btn.btn-colour-silver {
  background-color: silver;
  color: black;
}

.btn.btn-colour-tan {
  background-color: tan;
  color: black;
}

.btn.btn-colour-turquoise {
  background-color: turquoise;
  color: black;
}

.btn.btn-colour-white {
  background-color: white;
  border: solid 1px black;
  color: black;
}

.btn.btn-colour-yellow {
  background-color: yellow;
  color: black;
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
}

.btn.btn-colour-primer {
  background-color: darkgrey;
  color: black;
}

</style>