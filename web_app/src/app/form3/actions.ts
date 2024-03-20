'use server'
import axios from 'axios';
import { buildErrorMessage, axiosMailItClient } from '../_nonRoutingAssets/lib/form.api';

interface AxiosResponse {
    status: number;
    data: any;
}

export const submitToAPI = async (xml: string): Promise<AxiosResponse> => {
    try {
        const url = "https://rsbc-dh-ingestor-test.apps.silver.devops.gov.bc.ca/v1/publish/event/form?form=Document_submission";
      
        const response = await axios.post(url, xml, {
            headers: {
                'Content-Type': 'application/xml',
            },
        });
        return {
            status: response.status,
            data:response.data,
        };
    }
    catch (error) {
        if (axios.isAxiosError(error)) {
            return {
                status: error.response?.status ?? 500,
                data: error.response?.statusText ?? 'An error occured',
            };
        }
        return {
            status: 500,
            data: error,
        };
    }
};

interface EnvData {
    appeals_Registry_Email: string,
    email_BCC:string,
    do_Not_Reply_Address:string,
}

export const getEnvData = (): EnvData => {

    let envData: EnvData = {
        appeals_Registry_Email: '',
        email_BCC: '',
        do_Not_Reply_Address:'',
    };

    envData.appeals_Registry_Email = process.env.APPEALS_REGISTRY_EMAIL as string;
    envData.email_BCC = process.env.EMAIL_BCC as string;
        envData.do_Not_Reply_Address = process.env.DO_NOT_REPLY_ADDRESS as string;

    return envData;
}

export const postFormData = async (formData: FormData,): Promise<AxiosResponse> => {
    try {
        const url = "https://rsbc-dh-ingestor-test.apps.silver.devops.gov.bc.ca/evidence";
        const username = 'orbeon-rsbc-api-user';
        const password = 'EA8204491121B5676D1E97B41BE3163729F37C08';
        const response = await axios.post(url, formData, {
            headers: {
                'Content-Type': 'text/html',
            },
            auth: {
                username: username,
                password: password,
            },
        });
        return {
            status: response.status,
            data: response.data,
        };
    }
    catch (error) {
        if (axios.isAxiosError(error)) {
            return {
                status: error.response?.status ?? 500,
                data: error.response?.data || 'An error occured',
            };
        }
        return {
            status: 500,
            data: 'An unknown error occured',
        };
    }
};



export const sendEmail = async (filesContent: string[], filesName: string[]): Promise<string | null> => {
    console.log("axiosMailItClient.getUri: " + axiosMailItClient.getUri());

    const encoded = Buffer.from(`${process.env.MAIL_IT_CLIENT_ID}` + ':' +
        `${process.env.MAIL_IT_SECRET}`).toString('base64');

    let config = {
        headers: {
            'Authorization': 'Basic ' + encoded,
            'Content-Type': 'application/json'
        }
    };

    let email = getEmailTemplate(filesContent, filesName);
    console.log("email: ", email);
    try {
        const data = await axiosMailItClient.post(axiosMailItClient.getUri() + '/mail/send', email, config);

        console.debug("Email sent successfully with return code: " + data.status);
        return null;
    } catch (error) {
        console.error("Error: ", error);
        const errorDetails = "Failed sending email: " + buildErrorMessage(error);
        console.error(errorDetails);
        return errorDetails;
    }
}

function getEmailTemplate(files: string[], names: string[]) {
    if (files && names) {
        const attachments = files.map((file, index) => ({
            "filename": names[index],
            "filecontents": file
        }));

        return {
            "from": {
                "email": "peiman.abdi@gov.bc.ca"
            },
            "to": [{
                "email": "peiman.abdi@gov.bc.ca"
            }, {
                "email": "pabdi1@gmail.com"
            }],
            "subject": "Test from jag-mail-it",
            "content": {
                "type": "text/plain",
                "value": "This is some content"
            },
            "attachment": attachments
        };
    }
}

