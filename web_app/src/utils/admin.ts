import constants from "../config/constants";
import rsiStore from "@/store"
import moment from "moment-timezone";

import {apiHeader} from "@/utils/auth"

export async function adminAddUserRole(new_user) {

    console.log("inside actions.js adminAddUserRole()", new_user)

    const url = constants.API_ROOT_URL + "/api/v1/admin/users/" + new_user.user_guid + "/roles"
    const payload = {"role_name": "administrator"}
    return await new Promise((resolve, reject) => {
        fetch(url, {
            "method": 'POST',
            "body": JSON.stringify(payload),
            "headers": apiHeader(),
            })
                .then(response => {
                    if (response.status === 200) {
                        return response.json()
                    }
                })
                .then( () => {
                    return resolve(rsiStore.commit("addAdminUserRole", {
                        username: new_user.username,
                        user_guid: new_user.user_guid,
                        first_name: new_user.first_name,
                        last_name: new_user.last_name,
                        badge_number: new_user.badge_number,
                        agency: new_user.agency,
                        role_name: payload.role_name,
                        approved_dt: moment().tz("America/Vancouver"),
                        submitted_dt: moment().tz("America/Vancouver")
                    }))
                })
                .catch((error) => {
                    console.log("error", error)
                    if (error) {
                        return reject("message" in error ? {"description": error.message }: {"description": "No valid response"})
                    }
                    return reject({"description": "Server did not respond"})
                    });
            })
}


export async function adminApproveUserRole(new_user) {
    console.log("inside actions.js adminApproveUserRole(): ")
    const url = constants.API_ROOT_URL + "/api/v1/admin/users/" + new_user.user_guid + "/roles/officer"
    return await new Promise((resolve, reject) => {
        fetch(url, {
        "method": 'PATCH',
        "headers": apiHeader(),
            })
                .then(response => {
                    if (response.status === 200) {
                        return response.json()
                    }
                })
                .then( data => {
                    new_user.role_name = data.role_name
                    new_user.approved_dt = data.approved_dt
                    new_user.submitted_dt = data.submitted_dt
                    resolve(rsiStore.commit("updateAdminUserRole", new_user))
                })
                .catch((error) => {
                    console.log("error", error)
                    if (error) {
                        reject("message" in error ? {"description": error.message }: {"description": "No valid response"})
                    }
                    reject({"description": "Server did not respond"})
                    });
            })
}


export async function adminDeleteUserRole(payload) {
    console.log("inside actions.js adminDeleteUserRole(): ", payload)
    const url = constants.API_ROOT_URL + "/api/v1/admin/users/" + payload.user_guid + "/roles/" + payload.role_name
    return await new Promise((resolve, reject) => {
        fetch(url, {
        "method": 'DELETE',
        "headers": apiHeader(),
            })
                .then(response => {
                    console.log(response)
                    if (response.status === 200) {
                        resolve(rsiStore.commit("deleteAdminUserRole", payload))
                    }
                })
                .catch(error => {
                    console.log("error", error)
                    if (error) {
                        reject("message" in error ? {"description": error.message }: {"description": "No valid response"})
                    }
                    reject({"description": "Server did not respond"})
                    });
            })
}