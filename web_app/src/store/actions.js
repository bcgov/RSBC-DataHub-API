export default {
    initializeStore (context) {
        console.log("inside actions.js initializeStore()")
        context.commit('retrieveFormsFromLocalStorage')
    },

    saveDoNotPrint (context) {
        console.log("inside actions.js saveDoNotPrint()");
        context.commit('stopEditingCurrentForm');
        context.commit('saveFormsToLocalStorage');
    },

    deleteSpecificForm({ commit }, prohibition_index) {
        commit('deleteForm', prohibition_index)
        commit('saveFormsToLocalStorage');
        commit('stopEditingCurrentForm');
    },


}