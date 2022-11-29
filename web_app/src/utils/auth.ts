import rsiStore from "@/store"


export function apiHeader(){
    const headers = new Headers();
    headers.set('Content-Type', 'application/json')
    if (rsiStore.state.keycloak.token) {
        headers.set('Authorization', 'Bearer ' + rsiStore.state.keycloak.token)
    }
    return headers
}

export function getKeycloakUsername(){
    if (rsiStore.state.keycloak) {
        return rsiStore.state.keycloak.userName;
    }
    return ''
}