'use server'

import { axiosVirusScanClient, handleError } from "./form.api";

export const checkVirusScanner = async (file: string): Promise<boolean> => {

    console.log("axiosVirusScanClient.getUri: " + axiosVirusScanClient.getUri());
    const encoded = Buffer.from(`${process.env.CLAMAV_CLIENT_BASIC_AUTH_USER}` + ':' +
        `${process.env.CLAMAV_CLIENT_BASIC_AUTH}`).toString('base64');

    //console.log("encoded: ", encoded, `${process.env.CLAMAV_CLIENT_BASIC_AUTH}`)

    var config = {
        headers: {
            'Authorization': 'Basic ' + encoded,
            'Content-Type': 'application/json'
        }
    };

    var data = {
        document: `${file}`
    };
    try {
        const response = (await axiosVirusScanClient.post(axiosVirusScanClient.getUri() + '/avscan', data, config));
        console.debug("File was scanned successfully with return code: " + response.status);
        return true;
    } catch (error) {
        await handleError(error);
        return false;
    }
}