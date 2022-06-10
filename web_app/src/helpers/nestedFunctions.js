import Vue from 'vue'

export default {

    getProp (obj, props) {
      const prop = props.shift()
      if (!obj[prop] || !props.length) {
        return obj[prop]
      }
      return this.getProp(obj[prop], props)
    },

    setProp (obj, props, value) {
      const prop = props.shift()
      if (!obj[prop]) {
        Vue.set(obj, prop, {})
      }
      if (!props.length) {
        if (value && typeof value === 'object' && !Array.isArray(value)) {
          obj[prop] = { ...obj[prop], ...value }
        } else {
          obj[prop] = value
        }
        return
      }
      this.setProp(obj[prop], props, value)
    },

    deleteProp (obj, props) {
      const prop = props.shift()
      if (!obj[prop]) {
        return
      }
      if (!props.length) {
        Vue.delete(obj, prop)
        return
      }
      this.deleteProp(obj[prop], props)
    }

}