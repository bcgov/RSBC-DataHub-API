import constants from "../config/constants";
import rsiStore from "@/store"
import {lookupDriverProvince} from "@/utils/lookups"
import fuzzysort from 'fuzzysort'
import {apiHeader} from "@/utils/auth"

// When the vehicle queried from ICBC's API, the returned vehicle make and model
// may not exactly match the vehicle list from PrimeCorp that contains the make
// and model abbreviations used on the printouts. We use a fuzzy search
// algorithm to find the best match.
export async function findVehicleByFuzzySearch(payload) {
    console.log("findVehicleByFuzzySearch()", payload[0])
    const icbcData = payload[0]

    const primeCorpVehicleList = rsiStore.state.Common.vehicles.map(v => v.search);
    const results = fuzzysort.go(icbcData['vehicleMake'] + " - " + icbcData['vehicleModel'], primeCorpVehicleList)
    return await new Promise((resolve, reject) => {
        console.log("findVehicleByFuzzySearch() - results", results, payload)
        if (results.length >= 1) {
            const arrayOfVehicleMakeModel = rsiStore.state.Common.vehicles
            const vehicleObject = arrayOfVehicleMakeModel.filter(v => v.search === results[0].target)
            resolve(vehicleObject[0])
        } else {
            reject({
                "description": "no match found",
                "result": results
            })
        }
    })
}

export async function lookupDriverFromICBC([pathString, dlNumber]) {
    console.log("inside actions.js lookupDriverFromICBC():", pathString, dlNumber)
    // const dlNumber = icbcPayload['dlNumber']
    const url = constants.API_ROOT_URL + "/api/v1/icbc/drivers/" + dlNumber
    return await new Promise((resolve, reject) => {
         fetch(url, {
            "method": 'GET',
            "headers": apiHeader()
        })
            .then(response => response.json())
            .then(data => {
                console.log("ICBC driver data", data)
                if (data.error) {
                    reject("message" in data['error'] ? {"description": data['error'].message }: {"description": "No valid response"})
                } else {
                    const provinceCode = data['party']['addresses'][0]['region']
                    lookupDriverProvince([pathString, provinceCode])
                    resolve(rsiStore.commit("populateDriverFromICBC", data ))
                }
            })
            .catch( (error) => {
                if (error) {
                    reject("error" in error ? error.error : {"description": "No valid response"})
                }
                reject({"description": "Server did not respond"})
            });
        })
}



export async function lookupPlateFromICBC([plateNumber, path]) {

    console.log("inside actions.js lookupPlateFromICBC(): ")
    console.log("plateNumber", plateNumber)
    const url = constants.API_ROOT_URL + "/api/v1/icbc/vehicles/" + plateNumber
    return await new Promise((resolve, reject) => {
        fetch(url, {
        "method": 'GET',
        "headers": apiHeader()
            })
                .then(response => response.json())
                .then(data => {
                    console.log("data", data)
                    if (data.error) {
                        reject("description" in data['error'] ? {"description": data['error'].description }: {"description": "No valid response"})
                    } else {
                        findVehicleByFuzzySearch(data)
                            .then( (result) => {
                                const payload = {"target": {
                                        "id": "vehicle_make",
                                        "path": path,
                                        "value": result
                                    }
                                }
                                console.log("preparing to updateFormField()", result, payload)
                                rsiStore.commit("updateFormField", payload)
                            })
                            .catch( (error) => {
                                console.log("findVehicleByFuzzySearch() - error", error)
                            })
                        resolve(rsiStore.commit("populateVehicleFromICBC", data))
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


