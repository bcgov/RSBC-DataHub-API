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
import { Step1Data, Step2Data, Step3Data, Step4Data } from '../interfaces'; 
import { generatePdfIds } from '../components/GeneratePDF';
export default function Page() {

      const [isExpanded, setIsExpanded] = useState<boolean>(false);
        const submitData = () => {
        console.log(step1Data);
            console.log(step2Data);
            console.log(step3Data);
            setIsExpanded(true);

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
                pdfList.push({ id: 'irpControlBlock', pageNumber: 5 }, { id: 'step4', pageNumber: 6 });
            else if (step1Data.controlIsAdp) {
                pdfList.push({ id: 'adp-burden-of-proof-text', pageNumber: 5 });
                pdfList.push({ id: 'page5img1', pageNumber: 5 });
                pdfList.push({ id: 'page5img2', pageNumber: 6 });
                pdfList.push({ id: 'page6img1', pageNumber: 6 });
                pdfList.push({ id: 'step4', pageNumber: 7 });
            }

            setTimeout(async () => {
                const pdf = await generatePdfIds(pdfList);
                pdf?.save('latest.pdf');
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
    });

    const [step4Data, setStep4Data] = useState<Step4Data>({
        signatureApplicantName: '',
    });

    const handleStep1Data = (step1Data: Step1Data) => {
        console.log(step1Data);
        setStep1Data(step1Data);
    };

    const handleStep2Data = (step2Data: Step2Data) => {        
        setStep2Data(step2Data);
        console.log(step2Data);
    };

    const handleStep3Data = (step3Data: Step3Data) => {
        setStep3Data(step3Data);
        console.log(step3Data);
    };

    const handleStep4Data = (step3Data: Step4Data) => {
        setStep4Data(step4Data);
        console.log(step4Data);
    };
    
   return (       

       <div className="formContent">  
       
                <div id="formContent" >
                  <div id="page1img1">
                        <h1 className="header1" id="hed">Notice of Driving Prohibition Application for Review</h1>
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
               </div>

            <CustomAccordion title="Step 1: Enter Prohibition Information" id="step1" isExpanded={isExpanded}
                       content={<Step1 step1DatatoSend={handleStep1Data}></Step1>} />
               

               
               
            <CustomAccordion title="Step 2: Enter Applicant Information" id="step2" isExpanded={isExpanded}
                            content={<Step2 step2DatatoSend={handleStep2Data} licenseSeized={step1Data.licenseSeized === 'licenseSeized'}></Step2>} />
                   
            <CustomAccordion title="Step 3: Complete Review Information" id="step3" isExpanded={isExpanded}
                content={<Step3 controlIsUl={step1Data.controlIsUl} controlIsIrp={step1Data.controlIsIrp} controlIsAdp={step1Data.controlIsAdp}
                    step3DatatoSend={handleStep3Data} licenseSeized={step1Data.licenseSeized === 'licenseSeized'} />
                } />
                  

               <CustomAccordion title="Step 4: Consent and Submit" id="step4" isExpanded={isExpanded}
                   content={<Step4 step4DatatoSend={handleStep4Data} />} />


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


