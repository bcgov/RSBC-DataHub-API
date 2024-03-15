import { axiosVirusScanClient, buildErrorMessage } from "./form.api";

export const checkVirusScanner = async (file: string): Promise<boolean> => {

    console.log("axiosVirusScanClient.getUri: " + axiosVirusScanClient.getUri());
    const encoded = Buffer.from(`${process.env.VIRUS_SCAN_USER}` + ':' +
        `${process.env.VIRUS_SCAN_PASS}`).toString('base64');

    console.log("encoded: ", encoded, `${process.env.VIRUS_SCAN_PASS}`)

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
        console.error("Error: ", error);
        const errorDetails = "Failed sending email: " + buildErrorMessage(error);
        console.error(errorDetails);
        return false;
    }
}