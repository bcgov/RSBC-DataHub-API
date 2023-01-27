import rsiStore from "@/store"

export function updateUserIsAuthenticated(payload) {
    if (Array.isArray(payload)) {
        for (const role of payload) {
            if ('approved_dt' in role) {
                if (role.approved_dt) {
                    rsiStore.commit("userIsAuthenticated", true)
                }
            }
        }
    } else {
        rsiStore.commit("userIsAuthenticated", false)
    }

}