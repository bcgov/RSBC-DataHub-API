'use server'
import { buildErrorMessage, axiosMailItClient, axiosApiClient } from '../_nonRoutingAssets/lib/form.api';
import { Form3Data } from '../interfaces';
import dayjs from 'dayjs';

interface AxiosResponse {
    status: number;
    data: any;
}

export const submitToAPI = async (applicantInfo: Form3Data): Promise<AxiosResponse> => {
    try {
        const xml = getXMLData(applicantInfo);
        console.log(xml);

        const url = axiosApiClient.getUri() + "/v1/publish/event/form?form=Document_submission";
        const response = await axiosApiClient.post(url, xml, {
            headers: {
                'Content-Type': 'application/xml',
            },
        });
        return {
            status: response.status,
            data: response.data,
        };
    }
    catch (error) {
        console.log("Error: ", error);
        return {
            status: 500,
            data: error,
        };
    }
};

export const postValidateFormData = async (applicantInfo: Form3Data,): Promise<AxiosResponse> => {
    try {
        const formData = new FormData();
        formData.append('prohibition_number', applicantInfo.prohibitionNumberClean);
        formData.append('last_name', applicantInfo.controlDriverLastName);

        const url = axiosApiClient.getUri() + "/evidence";
        const encoded = Buffer.from(`${process.env.API_USER}` + ':' +
        `${process.env.API_PASS}`).toString('base64');

        const response = await axiosApiClient.post(url, formData, {
            headers: {
                'Authorization': 'Basic ' + encoded,
                'Content-Type': 'text/html',
            },
        });
        return response;
    } catch (error) {
        console.log("Error:", error );
        return {
            status: 500,
            data: 'An unknown error occurred',
        };
    }
};



export const sendEmail = async (filesContent: string[], filesName: string[], applicantInfo: Form3Data): Promise<string | null> => {
    console.log("axiosMailItClient.getUri: " + axiosMailItClient.getUri());

    const encoded = Buffer.from(`${process.env.MAIL_IT_CLIENT_ID}` + ':' +
        `${process.env.MAIL_IT_SECRET}`).toString('base64');

    let config = {
        headers: {
            'Authorization': 'Basic ' + encoded,
            'Content-Type': 'application/json'
        }
    };

    let email = getEmailTemplate(filesContent, filesName, applicantInfo);
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

function getEmailTemplate(files: string[], names: string[], applicantInfo: Form3Data) {
    if (files && names) {
        const attachments = files.map((file, index) => ({
            "filename": names[index],
            "filecontents": file
        }));

        return {
            "from": {
                "email": `${process.env.DO_NOT_REPLY_ADDRESS}`
            },
            "to": [{
                "email": `${process.env.APPEALS_REGISTRY_EMAIL}`
            }],
            "subject": "Evidence Attached - Driving Prohibition Review " + `${applicantInfo.controlProhibitionNumber}`,
            "content": {
                "type": "text/plain",
                "value": `	 
                    Attached is the evidence as submitted by the applicants.                        
                `
            },
            "attachment": attachments
        };
    }
}


const getXMLData = (form3Data: Form3Data): string => {
    const xmlString = `<?xml version="1.0" encoding="UTF-8"?>
<form xmlns:fr="http://orbeon.org/oxf/xml/form-runner" fr:data-format-version="4.0.0">
    <submitted>false</submitted>
    <before-you-begin-section>
        <help-text/>
        <appeals-registry-email-address>${process.env.APPEALS_REGISTRY_EMAIL}</appeals-registry-email-address>
        <rsi-email-address>${process.env.email_BCC}</rsi-email-address>
        <do-not-reply-address>${process.env.DO_NOT_REPLY_ADDRESS}</do-not-reply-address>
    </before-you-begin-section>
    <applicant-information-section>
        <prohibition-information-label/>
        <control-prohibition-number>${form3Data.controlProhibitionNumber}</control-prohibition-number>
        <control-11/>
        <control-is-adp>${form3Data.controlIsAdp}</control-is-adp>
        <control-is-irp>${form3Data.controlIsIrp}</control-is-irp>
        <control-is-ul>${form3Data.controlIsUl}</control-is-ul>
        <prohibition-number-clean>${form3Data.prohibitionNumberClean}</prohibition-number-clean>
        <prohibition-no-image filename="Combo prohibition no.png" mediatype="image/png">/fr/service/persistence/crud/gov-pssg/Document_submission/form/e91a38b43ecc3155b9696521176bb1636200847f.bin</prohibition-no-image>
        <control-driver-last-name>${form3Data.controlDriverLastName}</control-driver-last-name>
        <validate-prohibition/>
        <is-prohibition-valid>${form3Data.isProhibitionNumberValid}</is-prohibition-valid>
        <prohibtion-status/>
        <applicant-contact-information-label/>
        <applicant-role> ${form3Data.applicantRoleSelect}</applicant-role>
        <signed-consent-message/>
        <applicant-email-address>${form3Data.applicantEmailAddress}</applicant-email-address>
        <applicant-email-confirm>${form3Data.applicantEmailConfirm}</applicant-email-confirm>
    </applicant-information-section>
    <guidelines-grounds-section>
        <ul-grounds-text/>
        <providing-information/>
    </guidelines-grounds-section>
    <evidence-section>
        <attachment-type-text/>
        <file-upload>
            <_ filename="test.pdf" mediatype="application/pdf" size="7125">file:/tmp/xforms_upload_11769073452736458578.tmp?filename=test.pdf&amp;mediatype=application%2Fpdf&amp;size=7125&amp;mac=b278a0c9fc444f51119590c9e3cf17d53e8e363a</_>
        </file-upload>
    </evidence-section>
    <consent-section>
        <control-applicant-name>${form3Data.signatureApplicantName}</control-applicant-name>
        <date-signed>${dayjs(Date.now())}</date-signed>
        <control-5/>
    </consent-section>
</form>
            `;
    return xmlString;
}