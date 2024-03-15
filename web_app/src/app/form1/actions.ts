'use server'
import { buildErrorMessage, axiosMailItClient } from '../_nonRoutingAssets/lib/form.api';
import { Step1Data, Step2Data } from './../interfaces';

export const sendEmail = async (filesContent: string[], filesName: string[]): Promise<string | null> => {
    console.log("axiosMailItClient.getUri: " + axiosMailItClient.getUri());

    const encoded = Buffer.from(`${process.env.MAIL_IT_CLIENT_ID}` + ':' +
        `${process.env.MAIL_IT_SECRET}`).toString('base64');

    var config = {
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


function getXMLFormData(step1Data: Step1Data, step2Data: Step2Data): string {
    // Construct the XML string using the data from step1Data, step2Data, and step3InputProps.
    const xmlString = `
        <?xml version="1.0" encoding="UTF-8"?>
        <form xmlns:fr="http://orbeon.org/oxf/xml/form-runner" fr:data-format-version="4.0.0">
            <submitted></submitted>
            <before-you-begin-section>
                <help-text/>
            </before-you-begin-section>
            <prohibition-information>
                <control-prohibition-number>${step1Data.controlProhibitionNumber}</control-prohibition-number>
                <control-is-ul>${step1Data.controlIsUl}</control-is-ul>
                <prohibition-number-clean>${step1Data.prohibitionNumberClean}</prohibition-number-clean>
                <prohibition-no-image filename="" mediatype=""></prohibition-no-image>
                <control-is-irp>${step1Data.controlIsIrp}</control-is-irp>
                <control-is-adp>${step1Data.controlIsAdp}</control-is-adp>
                <licence-seized>${step1Data.licenseSeized}</licence-seized>
                <licence-not-surrendered/>${step1Data.licenseNoSurrendered}
                <licence-lost-or-stolen/>${step1Data.licenseLostOrStolen}
                <licence-not-issued/>${step1Data.licenseNotIssued}
                <irp-prohibition-type-length>${step1Data.irpProhibitionTypeLength}</irp-prohibition-type-length>
                <date-of-service>${step1Data.dateOfService}</date-of-service>
            </prohibition-information>
            <identification-information>
                <applicant-information-label/>
                <applicant-role-select>${step2Data.applicantRoleSelect}</applicant-role-select>
                <represented-by-lawyer>${step2Data.representedByLawyer}</represented-by-lawyer>
                <applicant-role>${step2Data.applicantRoleSelect}</applicant-role>
                <control-4/>
                <consent-upload filename="" mediatype="" size=""/>
                <lawyer-information-label/>
                <control-2/>
                <first-name-applicant>${step2Data.applicantFirstName}</first-name-applicant>
                <last-name-applicant>${step2Data.applicantLastName}</last-name-applicant>
                <applicant-phone-number>${step2Data.applicantPhoneNumber}</applicant-phone-number>
                <control-3/>
                <applicant-email-address>${step2Data.applicantEmailAddress}</applicant-email-address>
                <appeals-registry-email>${process.env.APPEALS_REGISTRY_EMAIL}</appeals-registry-email>
                <email-bcc>${process.env.EMAIL_BCC}</email-bcc>
                <applicant-email-confirm>${step2Data.applicantEmailConfirm}</applicant-email-confirm>
                <do-not-reply-address>${process.env.DO_NOT_REPLY_ADDRESS}</do-not-reply-address>
                <driver-information-label/>
                <driver-first-name/>
                <driver-last-name/>
                <driver-bcdl/>
                <address-label/>
                <street-address>${step2Data.streetAddress}</street-address>
                <control-driver-city-town>${step2Data.controlDriverCityTown}</control-driver-city-town>
                <control-driver-province>${step2Data.controlDriverProvince}</control-driver-province>
                <control-driver-postal-code>${step2Data.controlDriverPostalCode}</control-driver-postal-code>
            </identification-information>
            <review-information>
                <ul-burden-of-proof-text/>
                <ul-grounds/>
                <irp-burden-of-proof-text/>
                <irp-grounds-list></irp-grounds-list>
                <adp-burden-of-proof-text/>
                <adp-grounds-alcohol/>
                <adp-grounds-drugs/>
                <adp-grounds-alcohol-drugs/>
                <adp-grounds-drug-expert/>
                <adp-grounds-refusal/>
                <control-6></control-6>
                <preparing-for-your-review/>
                <preparing-for-review-irp-text/>
                <preparing-for-review-ul-text/>
                <hearing-request-type></hearing-request-type>
                <wirtten-review-information/>
                <oral-review-instructions/>
            </review-information>
            <consent-and-submission>
                <signature-applicant-name></signature-applicant-name>
                <date-signed></date-signed>
                <control-5/>
                <form-submit-text/>
            </consent-and-submission>
        </form>                     
        `;
    return xmlString;
}

function getEmailTemplate(files: string[], names: string[]) {
    if(files && names) {
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
