'use client'
import React, { useRef, useState } from 'react';
import Image from 'next/image';
import CustomAccordion from '../components/Accordion';
import Step1 from './steps/step1';
import Step2 from './steps/step2';
import Step3 from './steps/step3';
import Step4 from '../components/step4';
import { Button, Grid, Typography } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import ArrowForward from '@mui/icons-material/ArrowForward';
import { Step1Data, Step2Data, Step3Data, Step4Data } from '../interfaces';
import { generatePDF } from '../components/GeneratePDF';
import { postForm1, sendEmail } from './actions';
import dayjs from 'dayjs';
import { useRouter } from 'next/navigation';

export default function Page() {

    const router = useRouter();

    const step1Ref = useRef<{ clearData: () => void, validate: () => boolean }>(null);
    const step2Ref = useRef<{ clearData: () => void, validate: () => boolean }>(null);
    const step3Ref = useRef<{ clearData: () => void, validate: () => boolean }>(null);
    const step4Ref = useRef<{ clearData: () => void, validate: () => void }>(null);

    const [isExpanded, setIsExpanded] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState(false);
    const [message, setMessage] = useState('');

    const combineError = (errorMsg: string, newError: string) => {
        if (errorMsg.startsWith("There are error in"))
            return errorMsg + ", " + newError;
        else
            return "There are error in " + newError;
    }
    
    const submitData = () => {
        let errorMsg = ""; 
        if (!step4Data.signatureApplicantName) {
            step4Ref.current?.validate();
            errorMsg = combineError(errorMsg, "Step 4");
        }
        step3Data.hasError = step3Ref.current?.validate() || false;
        if (step3Data.hasError) {           
            errorMsg = combineError(errorMsg, "Step 3");
        }
    
        if (step2Ref.current?.validate()) {
            errorMsg = combineError(errorMsg, "Step 2");
        }

        if (step1Data.hasError || !step1Ref.current?.validate()) {
            errorMsg = combineError(errorMsg, "Step 1");
        }

        setMessage(errorMsg);

        if(errorMsg === "")
            submitDataAfterValidation();
    }

    const submitDataAfterValidation = async () => {
        let form1SubmitOk = false;
        setIsLoading(true);
        setIsExpanded(true);
        try {
            let response = await postForm1(step1Data, step2Data, step3Data, step4Data);
            if (!response.data.is_success) {
                setMessage(response.data.error);
                return;//stop going further?
            } else {
                form1SubmitOk = true;
            }
            console.log("posting xml done!! ");
        } catch (error) { }
        console.log("after posting xml");

        let pdfList = [
            { id: 'page1img1', pageNumber: 1 },// Before You Begin display block
            { id: 'summarystep1', pageNumber: 1 }, // Step 1 header
            { id: 'page1img2', pageNumber: 1 }, //Step 1 Info Part 1
            { id: 'page2img1', pageNumber: 2 }, //Step 1 Info Part 2
            { id: 'summarystep2', pageNumber: 2 },// Step 2 Header
            { id: 'page2img2', pageNumber: 2 },//Step 2 Info Part 1
            { id: 'page3img1', pageNumber: 3 },//Step 2 Info Part 2
            { id: 'page3img2', pageNumber: 3 },//Step 2 Info Part 3
            { id: 'page4img1', pageNumber: 4 }, //Step 2 Info Part 4
            { id: 'summarystep3', pageNumber: 5 }, // Step 3 Header
        ];

        if (step1Data.controlIsUl)
            pdfList.push({ id: 'ulControlBlock', pageNumber: 5 }, { id: 'step4', pageNumber: 6 });
        else if (step1Data.controlIsIrp)
            pdfList.push({ id: 'irpControlBlock', pageNumber: 5 }, { id: 'revOption', pageNumber: 6 }, { id: 'step4', pageNumber: 7 });
        else if (step1Data.controlIsAdp) {
            pdfList.push({ id: 'adp-burden-of-proof-text', pageNumber: 5 });
            pdfList.push({ id: 'page5img1', pageNumber: 5 });
            pdfList.push({ id: 'page5img2', pageNumber: 6 });
            pdfList.push({ id: 'page5img3', pageNumber: 7 });
            pdfList.push({ id: "page5img4", pageNumber: 8 });
            pdfList.push({ id: 'step4', pageNumber: 8 });
        }
        // setTimeout(async () => {
        //     const pdf = await generatePDF(pdfList, 'Notice of Driving Prohibition Application for Review');
        //     pdf?.save('Notice of Driving Prohibition Application for Review.pdf');
        // }, 500);

        let fileContent = '';
        const pdf = await generatePDF(pdfList, 'Notice of Driving Prohibition Application for Review');
        const file = pdf?.output('blob');
        console.log("pdf file gen size:", file?.size);
        let reader = new FileReader();

        reader.onload = async function (e) {
            // The file converted into text base64
            console.log("isArrayBuffer ", reader.result instanceof ArrayBuffer);
            console.log("reader.result", reader.result?.toString().slice(0, 50));
            fileContent = reader.result?.toString().split('base64,')[1] || '';
            let result = await sendEmail(step2Data.consentFile, step2Data.consentFileName, fileContent, step1Data, step2Data);
            console.log("email sent and form1SubmitOK? ", result, form1SubmitOk);
            if (result === 202 && form1SubmitOk) {
                router.push('/form1/acknowledgement');
            } else {
                setIsLoading(false);
            }
        };
        // callback to reader.onload
        if (file || file !== undefined)
            reader.readAsDataURL(file);
    }

    const clearData = (event: React.MouseEvent<HTMLButtonElement>) => {
        step1Ref.current?.clearData();
        step2Ref.current?.clearData();
        step3Ref.current?.clearData();
        step4Ref.current?.clearData();
        step4Data.signatureApplicantErrorText = '';
        setIsExpanded(false);
        setIsLoading(false);
        setMessage('');
    }

    const [step1Data, setStep1Data] = useState<Step1Data>({
        controlProhibitionNumber: '',
        controlIsUl: false,
        controlIsIrp: false,
        controlIsAdp: false,
        prohibitionNumberClean: '',
        licenseSeized: '',
        licenseNoSurrendered: false,
        licenseLostOrStolen: false,
        licenseNotIssued: false,
        irpProhibitionTypeLength: '',
        hasError: false,
        dateOfService: dayjs(Date.now()).toDate(),
    });

    const [step2Data, setStep2Data] = useState<Step2Data>({
        applicantRoleSelect: '',
        representedByLawyer: '',
        applicantFirstName: '',
        applicantLastName: '',
        applicantPhoneNumber: '',
        applicantEmailAddress: '',
        applicantEmailConfirm: '',
        driverFirstName: '',
        driverLastName: '',
        driverBcdl: '',
        bcDriverLicenseNo: '',
        streetAddress: '',
        controlDriverCityTown: '',
        controlDriverProvince: '',
        controlDriverPostalCode: '',
        consentFile: null,
        consentFileName: null,
        hasError: false,
    });

    const [step3Data, setStep3Data] = useState<Step3Data>({
        ulGrounds: [],
        irpGroundsList: [],
        adpGroundsAlcohol: [],
        adpGroundsDrugs: [],
        adpGroundsAlcoholDrugs: [],
        adpGroundsDrugExpert: [],
        adpGroundsRefusal: [],
        control6: 0,
        hearingRequest: '',
        hasError: false,
    });

    const [step4Data, setStep4Data] = useState<Step4Data>({
        signatureApplicantName: '',
        signatureApplicantErrorText: '',
    });

    const handleStep1Data = (step1Data: Step1Data) => {
        setStep1Data(step1Data);
    };

    const handleStep2Data = (step2Data: Step2Data) => {
        setStep2Data(step2Data);
    };

    const handleStep3Data = (step3Data: Step3Data) => {
        setStep3Data(step3Data);
    };

    const handleStep4Data = (step4Data: Step4Data) => {
        setStep4Data(step4Data);
    };

    const hasSubmitError = () => {
        return step1Data.hasError || step2Data.hasError || step4Data.signatureApplicantErrorText;
    }

        return (

        <div className="formContent">

            <div id="formContent" >
                <div id="page1img1">
                    <h1 className="header1" id="hed">Notice of Driving Prohibition Application for Review</h1>
                    <CustomAccordion title="Before You Begin:" id="step0" isExpanded={isExpanded}
                        content={<div style={{ fontSize: "16px", fontFamily: "'BC Sans', 'Noto Sans',  Arial, sans-serif", paddingLeft: '10px', lineHeight: '2.5' }}><p>When you see this symbol <Image
                            src="/assets/icons/info-icon.png"
                            width={15}
                            height={15}
                            alt="Info" />
                            &nbsp;click it for more information.
                        </p>
                            <p>Submit only <strong> 1 online application</strong> for your prohibition review.</p>
                            <p>You&apos;ll receive at least <strong> 2 emails</strong> when you submit the form:</p>
                            <ol style={{ paddingLeft: '30px', lineHeight: '1.5' }}>
                                <li>A copy of your completed application, and</li>
                                <li>The next step in the application process.</li>
                            </ol>
                            <p>If you don&apos;t enter anything in the form for 15 minutes, it may time out.</p> </div>} />
                </div>

                <CustomAccordion title="Step 1: Enter Prohibition Information" id="step1" isExpanded={isExpanded}
                    content={<Step1 step1DatatoSend={handleStep1Data} ref={step1Ref} hasError={false}></Step1>} />




                <CustomAccordion title="Step 2: Enter Applicant Information" id="step2" isExpanded={isExpanded}
                    content={<Step2 step2DatatoSend={handleStep2Data} isEnabled={step1Data.licenseSeized === 'licenseSeized' || step1Data.controlIsUl}
                        ref={step2Ref} hasError={false} ></Step2>} />

                <CustomAccordion title="Step 3: Complete Review Information" id="step3" isExpanded={isExpanded}
                    content={<Step3 controlIsUl={step1Data.controlIsUl}
                        controlIsIrp={step1Data.controlIsIrp} controlIsAdp={step1Data.controlIsAdp}
                        ref={step3Ref}
                        step3DatatoSend={handleStep3Data} isEnabled={step1Data.licenseSeized === 'licenseSeized' || step1Data.controlIsUl}
                        hasError={false} irpProhibitionTypeLength={step1Data.irpProhibitionTypeLength} />
                    } />


                <CustomAccordion title="Step 4: Consent and Submit" id="step4" isExpanded={isExpanded}
                    content={<div>
                        <Step4 step4DatatoSend={handleStep4Data} ref={step4Ref} />
                        <div style={{ paddingTop: '30px' }}><strong><span style={{ fontSize: '16px' }} >Submit only 1 online application for your prohibition review.</span></strong></div>
                    </div>} />


            </div>
            {hasSubmitError() &&
                <div id="errorText">
                    <Typography variant="caption" sx={{ color: '#D8292F', fontWeight: '700', padding: '4px 10px 20px 30px', ml: '4px', fontSize: '16px', display: 'block' }}>

                        Your form contains errors. Please correct them to proceed.
                    </Typography>

                </div>
            }
            {message &&
                <div id="messageDiv">
                    <Typography variant="caption" sx={{ color: '#D8292F', fontWeight: '700', padding: '4px 10px 20px 30px', ml: '4px', fontSize: '16px', display: 'block', boxSizing: 'border-box' }}>
                        {message}
                    </Typography>

                </div>
            }
            <div style={{ paddingBottom: '40px' }}>
                <Grid container spacing={2} >
                    <Grid item xs={8} sx={{ padding: "1px" }}></Grid>
                    <Grid item xs={4} sx={{ padding: "1px" }}>
                        <Button onClick={clearData} variant="outlined" sx={{ cursor: 'pointer', color: '#003366', borderColor: '#003366', marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }} startIcon={<CloseIcon sx={{ fontWeight: 'bold' }} />}>
                            Clear
                        </Button>
                        <Button
                            disabled={isLoading}
                            onClick={submitData}
                            variant="contained"
                            sx={{ borderColor: '#003366', backgroundColor: '#003366', color: 'white', marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }}
                            startIcon={<ArrowForward sx={{ fontWeight: 'bold' }} />}>
                            Send
                        </Button>
                    </Grid>
                </Grid>
            </div>
        </div>
    )

}
