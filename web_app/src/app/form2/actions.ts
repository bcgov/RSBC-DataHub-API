'use server'
import { buildErrorMessage } from "@/app/_nonRoutingAssets/lib/form.api";
import { AvailableReviewDates } from "../interfaces";

//------------------------------------------
// Get available review dates 
//------------------------------------------
export const getAvailableReviewDates = async (prohibitionNumber: string, driverLastName: string | null | undefined): Promise< [Array<AvailableReviewDates>, string | null] > => {
    let url = `/fake url`;
   //console.log("Get available review dates, url: " + axiosApiClient.getUri() + url);
    
    try {
      //const { data } = await axiosClient.get(url);
      let newdata: Array<AvailableReviewDates> = [
                {
                    "label": "Fri, Mar 8, 2024 at 9:30AM (Pacific Time)",
                    "value": "MjAyNC0wMy0wOCAwOTowMDowMCAtMDg6MDB8MjAyNC0wMy0wOCAwOTozMDowMCAtMDg6MDA="
                },
                {
                    "label": "Fri, Mar 8, 2024 at 10:30AM (Pacific Time)",
                    "value": "MjAyNC0wMy0wOCAxMDozMDowMCAtMDg6MDB8MjAyNC0wMy0wOCAxMTowMDowMCAtMDg6MDA="
                },
                {
                    "label": "Mon, Mar 11, 2024 at 9:30AM (Pacific Time)",
                    "value": "MjAyNC0wMy0xMSAwOTowMDowMCAtMDc6MDB8MjAyNC0wMy0xMSAwOTozMDowMCAtMDc6MDA="
                },
                {
                    "label": "Mon, Mar 11, 2024 at 10:30AM (Pacific Time)",
                    "value": "MjAyNC0wMy0xMSAxMDowMDowMCAtMDc6MDB8MjAyNC0wMy0xMSAxMDozMDowMCAtMDc6MDA="
                },
                {
                    "label": "Mon, Mar 11, 2024 at 11:00AM (Pacific Time)",
                    "value": "MjAyNC0wMy0xMSAxMTowMDowMCAtMDc6MDB8MjAyNC0wMy0xMSAxMTozMDowMCAtMDc6MDA="
                },
                {
                    "label": "Mon, Mar 11, 2024 at 11:30AM (Pacific Time)",
                    "value": "MjAyNC0wMy0xMSAxMzowMDowMCAtMDc6MDB8MjAyNC0wMy0xMSAxMzozMDowMCAtMDc6MDA="
                },
                {
                    "label": "Tue, Mar 12, 2024 at 9:30AM (Pacific Time)",
                    "value": "MjAyNC0wMy0xMiAwOTozMDowMCAtMDc6MDB8MjAyNC0wMy0xMiAxMDowMDowMCAtMDc6MDA="
                },
                {
                    "label": "Wed, Mar 13, 2024 at 9:30AM (Pacific Time)",
                    "value": "MjAyNC0wMy0xMyAwOTowMDowMCAtMDc6MDB8MjAyNC0wMy0xMyAwOTozMDowMCAtMDc6MDA="
                },
                {
                    "label": "Wed, Mar 13, 2024 at 12:30AM (Pacific Time)",
                    "value": "MjAyNC0wMy0xMyAxMTozMDowMCAtMDc6MDB8MjAyNC0wMy0xMyAxMjowMDowMCAtMDc6MDA="
                }
            ];
      return [newdata, 'no error'];
    }catch (error) {
      const errorDetails = "Failed fetching available review dates: " + buildErrorMessage(error);
      console.error(errorDetails);
      return [[], errorDetails];
    }
  }
  
export const postReviewDate = async (prohibitionNumber: string, selectedReviewDate: string, driverLastName: string | null | undefined): Promise< string | null > => {
        // let url = axiosApiClient.getUri() + '/path';
        // console.log("Post to url: ", url);
    
        var config = {
            headers: { 'Content-Type': 'text/xml' }
        };
        let xmlData = getXMLFormData(prohibitionNumber, selectedReviewDate, driverLastName);
    
        try {
            //const response = await axiosApiClient.post(url, xmlData, config);
    
            //console.debug("Post was successful with return code: " + response.status);
            return null; //response.statusText;
        } catch (error) {
            const errorDetails = "Post failed: " + buildErrorMessage(error);
            console.error(errorDetails);
            return errorDetails;
        }
    }
    function getXMLFormData(prohibitionNumber: string, selectedReviewDate: string, driverLastName: string | null | undefined): string {
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
                <prohibition-number-clean>00197582</prohibition-number-clean>
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