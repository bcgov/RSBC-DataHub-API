import rsiStore from "@/store"

export async function lookupDriverProvince([pathString, provinceCode]) {
    console.log("inside actions.js lookupDriverProvince(): ", pathString, provinceCode)
    const jurisdictionArray = rsiStore.state.Common.jurisdictions.filter(o => o.objectCd === provinceCode)
    return await new Promise((resolve, reject) => {
        if (jurisdictionArray.length > 0) {
            const event = {
                "target": {
                    "value": jurisdictionArray[0],
                    "path": pathString,
                    "id": "province"
                }
            }
            resolve(rsiStore.commit("updateFormField", event))
        } else {
            reject({"error": "Can't find " + provinceCode + " in list of jurisdictions"})
        }
    })
}