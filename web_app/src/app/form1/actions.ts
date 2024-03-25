'use server'
import { buildErrorMessage, axiosMailItClient, axiosApiClient } from '../_nonRoutingAssets/lib/form.api';
import { Step1Data, Step2Data, Step3Data, Step4Data } from './../interfaces';

export async function sendEmail(fileContent: string | null, fileName: string | null, pagePdf: string, step1Data: Step1Data, step2Data: Step2Data): Promise<string | null> {

    const attachments = [{
        "filename": 'prohibition document.pdf',
        "filecontents": pagePdf,
    }];

    console.log("test: ", (fileContent && fileName) )
    if (fileContent && fileName) {
        attachments.push({
            "filename": fileName,
            "filecontents": fileContent,
        })
    };


    let email = getEmailTemplate(attachments, step1Data, step2Data);
    console.log("axiosMailItClient.getUri: " + axiosMailItClient.getUri());

    const encoded = Buffer.from(`${process.env.MAIL_IT_CLIENT_ID}` + ':' +
        `${process.env.MAIL_IT_SECRET}`).toString('base64');

    var config = {
        headers: {
            'Authorization': 'Basic ' + encoded,
            'Content-Type': 'application/json'
        }
    };
    try {
        // const data = await axiosMailItClient.post(axiosMailItClient.getUri() + '/mail/send', email, config);

        // console.debug("Email sent successfully with return code: " + data.status);
        return " There was an error!!!!";
    } catch (error) {
        console.error("Error: ", error);
        const errorDetails = "Failed sending email: " + buildErrorMessage(error);
        console.error(errorDetails);
        return errorDetails;
    }
}

export async function postForm1(step1Data: Step1Data, step2Data: Step2Data, step3data: Step3Data, step4data: Step4Data): Promise<string | null> {
    let url = axiosApiClient.getUri() + "/v1/publish/event/form?form=prohibition_review";

    console.log("Post to url: ", url);

    var config = {
        headers: { 'Content-Type': 'application/xml' }
    };
    let xmlData = getXMLFormData(step1Data, step2Data, step3data, step4data).trim();
    console.log("xml body: ", xmlData);
    try {
        // const response = await axiosApiClient.post(url, xmlData, config);
        // console.debug("Post was successful with return code: " + response.status);
        return "There was an error processing your request! Please try another time!! ";
    } catch (error) {
        console.error("Post failed: ", error);
        const errorDetails = "Post failed: " + buildErrorMessage(error);
        console.error(errorDetails);
        return errorDetails;
    }

}

function getXMLFormData(step1Data: Step1Data, step2Data: Step2Data, step3data: Step3Data, step4data: Step4Data): string {
    const ulGrounds = step3data.ulGrounds && step3data.ulGrounds.length > 0 ? `<ul-grounds>${step3data.ulGrounds.join(' ')}</ul-grounds>` : '<ul-grounds/>';
    const adpGroundsAlcohol = step3data.adpGroundsAlcohol && step3data.adpGroundsAlcohol.length > 0 ? `<adp-grounds-alcohol>${step3data.adpGroundsAlcohol.join(' ')}</adp-grounds-alcohol>` : '<adp-grounds-alcohol/>';
    const adpGroundsDrugs = step3data.adpGroundsDrugs && step3data.adpGroundsDrugs.length > 0 ? `<adp-grounds-drugs>${step3data.adpGroundsDrugs.join(' ')}</adp-grounds-drugs>` : '<adp-grounds-drugs/>';
    const adpGroundsAlcoholDrugs = step3data.adpGroundsAlcoholDrugs && step3data.adpGroundsAlcoholDrugs.length > 0 ? `<adp-grounds-alcohol-drugs>${step3data.adpGroundsAlcoholDrugs.join(' ')}</adp-grounds-alcohol-drugs>` : '<adp-grounds-alcohol-drugs/>';
    const adpGroundsDrugExpert = step3data.adpGroundsDrugExpert && step3data.adpGroundsDrugExpert.length > 0 ? `<adp-grounds-drug-expert>${step3data.adpGroundsDrugExpert.join(' ')}</adp-grounds-drug-expert>` : '<adp-grounds-drug-expert/>';
    const adpGroundsRefusal = step3data.adpGroundsRefusal && step3data.adpGroundsRefusal.length > 0 ? `<adp-grounds-refusal>${step3data.adpGroundsRefusal.join(' ')}</adp-grounds-refusal>` : '<adp-grounds-refusal/>';
    const irpGroundsList = step3data.irpGroundsList && step3data.irpGroundsList.length > 0 ? `<irp-grounds-list>${step3data.irpGroundsList.join(' ')}</irp-grounds-list>` : '<irp-grounds-list/>';
    // Construct the XML string using the data from step1Data, step2Data, and step3InputProps.
    const xmlString = `
        <?xml version="1.0" encoding="UTF-8"?>
        <form xmlns:fr="http://orbeon.org/oxf/xml/form-runner" fr:data-format-version="4.0.0">
            <submitted/>
            <before-you-begin-section>
                <help-text/>
            </before-you-begin-section>
            <prohibition-information>
                <control-prohibition-number>${step1Data.controlProhibitionNumber}</control-prohibition-number>
                <control-is-ul>${step1Data.controlIsUl}</control-is-ul>
                <prohibition-number-clean>${step1Data.prohibitionNumberClean}</prohibition-number-clean>
                <prohibition-no-image filename="test" mediatype="pdf">somename</prohibition-no-image>
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
                <driver-first-name>${step2Data.driverFirstName}</driver-first-name>
                <driver-last-name>${step2Data.driverLastName}</driver-last-name>
                <driver-bcdl>${step2Data.driverBcdl}</driver-bcdl>
                <address-label/>
                <street-address>${step2Data.streetAddress}</street-address>
                <control-driver-city-town>${step2Data.controlDriverCityTown}</control-driver-city-town>
                <control-driver-province>${step2Data.controlDriverProvince}</control-driver-province>
                <control-driver-postal-code>${step2Data.controlDriverPostalCode}</control-driver-postal-code>
            </identification-information>
            <review-information>
                <ul-burden-of-proof-text/>
                ${ulGrounds}
                <irp-burden-of-proof-text/>
                <irp-grounds-list>${irpGroundsList}</irp-grounds-list>
                <adp-burden-of-proof-text/>
                ${adpGroundsAlcohol}
                ${adpGroundsDrugs}
                ${adpGroundsAlcoholDrugs}
                ${adpGroundsDrugExpert}
                ${adpGroundsRefusal}
                <control-6>${step3data.control6}</control-6>
                <preparing-for-your-review/>
                <preparing-for-review-irp-text/>
                <preparing-for-review-ul-text/>
                <hearing-request-type>${step3data.hearingRequest}</hearing-request-type>
                <wirtten-review-information/>
                <oral-review-instructions/>
            </review-information>
            <consent-and-submission>
                <signature-applicant-name>${step4data.signatureApplicantName}</signature-applicant-name>
                <date-signed>${step4data.signedDate}</date-signed>
                <control-5/>
                <form-submit-text/>
            </consent-and-submission>
        </form>                     
        `;
    return xmlString;
}

function getEmailTemplate(attachments: object, step1Data: Step1Data, step2Data: Step2Data) {
    return {
        "from": {
            "email": `${process.env.DO_NOT_REPLY_ADDRESS}`
        },
        "to": [{
            "email": `${step2Data.applicantEmailAddress}`
        }],
        "bcc": [
            { "email": `${process.env.EMAIL_BCC_1}`},
            { "email": `${process.env.EMAIL_BCC_2}`}
        ],
        "subject": "Copy of Application Form - Driving Prohibition " + `${step1Data.controlProhibitionNumber}` + " Review",
        "content": {
            "type": "text/plain",
            "value": `	 
                Dear ${step2Data.applicantFirstName} ${step2Data.applicantLastName},

                Please find attached the completed PDF of your application for review of driving prohibition 21-013009.
            
                You must not drive while your licence is prohibited. Driving while prohibited is illegal. It carries a minimum fine of $500 for a first offence, a 12-month prohibition and possible imprisonment. Imprisonment is mandatory for a second offence.
            
                Thank you,
                RoadSafetyBC
            
                Please do not respond to this email. We've sent it from account that doesn't accept responses. If you need to reach us, call 1-855-387-7747. Select option 5 to reach the Appeals Registry.
                `
        },
        "attachment": attachments
    };
}

