'use server'
import { axiosApiClient, handleError } from "@/app/_nonRoutingAssets/lib/form.api";
import { AxiosResponse } from "axios";
import { ActionResponse, AvailableReviewDates } from "../interfaces";

//------------------------------------------
// Get available review dates 
//------------------------------------------
export async function getAvailableReviewDates(prohibitionNumber: string, driverLastName: string): Promise<ActionResponse> {
    let url = axiosApiClient.getUri() + `/schedule`;
    console.log("Get available review dates url: " + url);

    const formData = new FormData();
    formData.append('prohibition_number', prohibitionNumber);
    formData.append('last_name', driverLastName);
    const encoded = Buffer.from(`${process.env.FLASK_BASIC_AUTH_USER}` + ':' +
        `${process.env.FLASK_BASIC_AUTH_PASS}`).toString('base64');
    const config = {
        headers: {
            'Authorization': 'Basic ' + encoded,
            'Content-Type': 'text/html',
        },
    };
    try {
        const response = await axiosApiClient.post(url, formData, config);
        console.log("after the call: ",response.data);
        const actionResponse: ActionResponse = {
            data: {
                data: response.data,
                is_success: true,
                error: ''    
            }
          };
        return actionResponse;
    } catch (error) {
        return handleError(error);
    }
}

export async function scheduleReviewDate(prohibitionNumber: string, selectedReviewDate: string, driverLastName: string): Promise<ActionResponse> {
    let url = axiosApiClient.getUri() + '/v1/publish/event/form?form=review_schedule_picker';
    console.log("scheduleReviewDate url: ", url);

    var config = {
        headers: { 'Content-Type': 'application/xml' }
    };
    let xmlData = getScheduleReviewDateXml(prohibitionNumber, selectedReviewDate, driverLastName);

    try {
        const response = await axiosApiClient.post(url, xmlData, config);

        console.debug("Post scheduleReviewDate return code: " + response.status);
        return response;
    } catch (error) {
        return handleError(error);
    }
}

function getScheduleReviewDateXml(prohibitionNumber: string, selectedReviewDate: string, driverLastName: string | null | undefined): string {
    // Construct the XML string using the data from step1Data, step2Data, and step3InputProps.
    const xmlString = `
        <?xml version="1.0" encoding="UTF-8"?>
        <form xmlns:fr="http://orbeon.org/oxf/xml/form-runner" fr:data-format-version="4.0.0">
            <submitted>false</submitted>
            <before-you-begin-section>
                <help-text/>
            </before-you-begin-section>
            <schedule-review-section>
                <prohibition-number>${prohibitionNumber}</prohibition-number>
                <prohibition-number-clean>${prohibitionNumber.replace('-', '')}</prohibition-number-clean>
                <prohibition-no-image filename="Combo prohibition no.png" mediatype="image/png">/fr/service/persistence/crud/gov-pssg/review_schedule_picker/form/7490a2bdcb0062a565a5e7aa2b4144560c83d8e7.bin</prohibition-no-image>
                <last-name>${driverLastName}</last-name>
                <control-3/>
                <api-error/>
                <timeslot-selected>${selectedReviewDate}</timeslot-selected>
            </schedule-review-section>
        </form>
            `;
    return xmlString;
}