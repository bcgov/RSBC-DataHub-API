'use client'
import React, { FormEvent, useRef, useState } from 'react';
import Image from 'next/image';
import CustomAccordion from '../components/Accordion';
import Step1 from './steps/step1';
import Step2 from './steps/step2';
import Step3 from './steps/step3';
import Step4 from './steps/step4';
import { Button, Grid } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import ArrowForward from '@mui/icons-material/ArrowForward';
import { Step1Data, Step2Data, } from '../interfaces'; 
import { generatePdf, } from '../components/GeneratePDF';

export default function Page() {

    const contentRef = useRef<HTMLDivElement>(null);



    const [isExpanded, setIsExpanded] = useState<boolean>(false);
    const submitData = () => {
        console.log(step1Data);
        console.log(step2Data);
        setIsExpanded(true);
        setTimeout(async () => {
            const pdf = await generatePdf('formContent');
            if (pdf) {
                pdf.save('download.pdf');
            }
          
        }, 500);       

    }
    

    function onClear(event: FormEvent<HTMLFormElement>) {

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
    });

    const handleStep1Data = (step1Data: Step1Data) => {
        console.log(step1Data);
        setStep1Data(step1Data);
    };

    const handleStep2Data = (step2Data: Step2Data) => {        
        setStep2Data(step2Data);
        console.log(step2Data);
    };

    const handleStep3Data = (step3Data: Step2Data) => {
       
    };
    

    return (<div id="formContent" ref={contentRef }>
        <h1 className="header1">Notice of Driving Prohibition Application for Review</h1>
        <div className="formContent" >
            <CustomAccordion title="Before You Begin:" id="step0" isExpanded={isExpanded}
                content={<div style={{ fontSize: "16px", fontFamily: "'BC Sans', 'Noto Sans',  Arial, sans-serif", paddingLeft: '10px', lineHeight: '2.5' }}><p>When you see this symbol <Image
                    src="/./././assets/icons/info-icon.png"
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


            <CustomAccordion title="Step 1: Enter Prohibition Information" id="step1" isExpanded={isExpanded}
                content={<Step1 step1DatatoSend={handleStep1Data}></Step1>} />

            <CustomAccordion title="Step 2: Enter Applicant Information" id="step2" isExpanded={isExpanded}
                content={<Step2 step2DatatoSend={handleStep2Data} licenseSeized={ step1Data.licenseSeized === 'licenseSeized' }></Step2>} />

            <CustomAccordion title="Step 3: Complete Review Information" id="step3" isExpanded={isExpanded}
                content={<Step3 controlIsUl={step1Data.controlIsUl} controlIsIrp={step1Data.controlIsIrp} controlIsAdp={step1Data.controlIsAdp}
                    step3DatatoSend={handleStep3Data} licenseSeized={step1Data.licenseSeized === 'licenseSeized'} />
                } />

            <CustomAccordion title="Step 4: Consent and Submit" id="step4" isExpanded={isExpanded}
                content={<Step4 />} />


        </div>
        <div style={{paddingBottom:'40px'} }>
            <Grid container spacing={2} >
                <Grid item xs={8} sx={{ padding: "1px" }}></Grid>
                <Grid item xs={4} sx={{ padding: "1px" }}>
                    <Button variant="outlined" sx={{ cursor: 'pointer', color: '#003366', borderColor: '#003366', marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }} startIcon={<CloseIcon sx={{ fontWeight: 'bold' }} />}>
                        Clear
                    </Button>
                    <Button onClick={submitData} variant="contained" sx={{ borderColor: '#003366', backgroundColor: '#003366', color: 'white', marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }} startIcon={<ArrowForward sx={{ fontWeight: 'bold' }} />}>
                        Send
                    </Button>
                </Grid>
            </Grid>
        </div>
    </div>
    )
}


