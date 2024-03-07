'use server'
import { axiosClient, buildErrorMessage } from "@/app/_nonRoutingAssets/lib/form.api";
import { AvailableReviewDates } from "../interfaces";

//------------------------------------------
// Get available review dates 
//------------------------------------------
export const getAvailableReviewDates = async (prohibitionNumber: string, driverLastName: string | null | undefined): Promise< [Array<AvailableReviewDates>, string | null] > => {
    let url = `/fake url`;
    console.log("Get available review dates, url: " + axiosClient.getUri() + url);
    
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
  