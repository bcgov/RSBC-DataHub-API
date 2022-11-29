export const plugins = [
  store => {
    window.addEventListener("online", async () => {
      store.commit('Common/setIsOnline',true)
      console.log(`Network is online`)
    })
    window.addEventListener("offline", async () => {
      store.commit('Common/setIsOnline',false)
      console.log(`Network is offline`)
    })
  }
]