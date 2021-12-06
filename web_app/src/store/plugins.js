export const plugins = [
  store => {
    window.addEventListener("online", async () => {
      store.commit('networkIsOnline')
      console.log(`Network is online`)
    })
    window.addEventListener("offline", async () => {
      store.commit('networkIsOffline')
      console.log(`Network is offline`)
    })
  }
]