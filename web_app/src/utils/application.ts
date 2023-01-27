import constants from "../config/constants";
import {apiHeader} from "@/utils/auth"

export async function applyToUnlockApplication(application) {
    console.log("inside actions.js applyToUnlockApplication(): ")
    const url = constants.API_ROOT_URL + "/api/v1/users"
    return await new Promise((resolve, reject) => {
        fetch(url, {
            "method": 'POST',
            "body": JSON.stringify(application),
            "headers": apiHeader(),
                })
                    .then(response => {
                        return response
                    })
                    .then( (response) => {
                        const data = response.json()
                        if (response.status === 201) {
                            console.log("applyToUnlockApplication() - success", data)
                            resolve(data)
                        } else {
                            reject(data)
                        }
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