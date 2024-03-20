'use client'
import React, { useState, useRef } from 'react';
import Image from 'next/image';
import CustomAccordion from '../components/Accordion';
import { Button, Grid, TextField, Typography, RadioGroup, FormControlLabel, Radio } from '@mui/material';
import { generatePDF } from '../components/GeneratePDF';
import { FormField } from '../components/FormField';
import { postFormData, submitToAPI, getEnvData } from "./actions";
import CloseIcon from '@mui/icons-material/Close';
import ArrowForward from '@mui/icons-material/ArrowForward';
import {  Print } from '@mui/icons-material';
import Step4 from '../components/step4';
import { checkVirusScanner } from '@/app/_nonRoutingAssets/lib/virusScanApi';
import { file2Base64 } from '@/app/_nonRoutingAssets/lib/util';
import { Form3Data, Step4Data } from '../interfaces';
import dayjs from 'dayjs';

export default function Page() {   

   
    const [applicantInfo, setApplicantInfo] = useState<Form3Data>({
        controlProhibitionNumber: '',
        isProhibitionNumberValid:false,
        controlIsUl: false,
        controlIsIrp: false,
        controlIsAdp: false,
        prohibitionNumberClean: '',
        controlDriverLastName: '',
        applicantRoleSelect: '',
        applicantEmailAddress: '',
        applicantEmailConfirm: '',
        signatureApplicantName:'',
    });

    const [message, setMessage] = useState('');

    const step4Ref = useRef<{ clearData: () => void, validate:() => void }>(null);

    const [validProhibitionNumber, setValidProhibitionNumber] = useState(false);
    const [prohibitionNumberErrorText, setProhibitionNumberErrorText] = useState('');

    const [validDriverLastName, setValidDriverLastName] = useState(false);
    const [driverLastNameErrorText, setDriverLastNameErrorText] = useState('');

    const [applicantRoleErrorText, setApplicantRoleErrorText] = useState('');

    const [signatureApplicantNameErrorText, setSignatureApplicantNameErrorText] = useState('');

    const [emailAddressErrorText, setEmailAddressErrorText] = useState('');

    const [confirmEmailErrorText, setConfirmEmailErrorText] = useState('');

    const [fileUploadErrorText, setFileUploadErrorText] = useState('');

    const [isValidData, setIsValidData] = useState(false);

    const [isValidComboErrorText, setIsValidComboErrorText] = useState('');

    const [isFormSubmitted, setIsFormSubmitted] = useState(false);
    
    const prohibitionNumberRegex = /^(00|21|30|40)-\d{6}$/;

    const prohibitionNumberChanged = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setApplicantInfo({ ...applicantInfo, controlProhibitionNumber: value });       
    };

    const validateField = () => {
        if (prohibitionNumberRegex.exec(applicantInfo.controlProhibitionNumber)) {
            setValidProhibitionNumber(true);
            setApplicantInfo({
                ...applicantInfo,
                controlIsUl: applicantInfo.controlProhibitionNumber.startsWith('30'),
                controlIsIrp: applicantInfo.controlProhibitionNumber.startsWith('21') || applicantInfo.controlProhibitionNumber.startsWith('40'),
                controlIsAdp: applicantInfo.controlProhibitionNumber.startsWith('00'),
                prohibitionNumberClean: applicantInfo.controlProhibitionNumber.replace('-', ''),
            });
        } else {
            setProhibitionNumberErrorText(applicantInfo.controlProhibitionNumber ? "Enter first 8 numbers with the dash. Don't enter the digit in the grey box. Prohibition numbers start with 00, 21, 30 or 40." : "Enter prohibition number found on the notice.");
            setValidProhibitionNumber(false);
            setApplicantInfo({ ...applicantInfo, controlIsUl: false });
            setApplicantInfo({ ...applicantInfo, controlIsIrp: false });
            setApplicantInfo({ ...applicantInfo, controlIsAdp: false });
        }
        
    };

      const driverLastNameChanged = (e: React.ChangeEvent<HTMLInputElement>) => {
          const value = e.target.value;
          setApplicantInfo({ ...applicantInfo, controlDriverLastName: value });    
    }
    const handleBlurDriverName = (e: React.FocusEvent<HTMLInputElement>) => {
        const  value  = e.target.value;

        validateDriverLastName(value);

    }

  

    const getXMLData = (form3Data: Form3Data): string => {
        let envData = getEnvData();
        console.log(envData);
        const xmlString = `<?xml version="1.0" encoding="UTF-8"?>
    <form xmlns:fr="http://orbeon.org/oxf/xml/form-runner" fr:data-format-version="4.0.0">
    	<submitted>false</submitted>
    	<before-you-begin-section>
    		<help-text/>
    		<appeals-registry-email-address>${envData.appeals_Registry_Email}</appeals-registry-email-address>
    		<rsi-email-address>${envData.email_BCC}</rsi-email-address>
    		<do-not-reply-address>${envData.do_Not_Reply_Address}</do-not-reply-address>
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

    const validateDriverLastName = (value:string) => {
        if (value === '') {
            setValidDriverLastName(false);
            setDriverLastNameErrorText("Please enter the driver's last name.");
        }
        else {
            setValidDriverLastName(true);
            setDriverLastNameErrorText('');
        }
    }

    const [isExpanded, setIsExpanded] = useState<boolean>(false);
    const [isValidForm, setIsValidForm] = useState<boolean>(true);

    const submitData = async () => {       
        validateData();
        const xml = getXMLData(applicantInfo);
        console.log(xml);

        if (isValidForm) {
            const result = await submitToAPI(xml);
            console.log("result after submission:");
            console.log(result);

            setIsFormSubmitted(result?.data?.success);
            setMessage("Your documents are sent. Please check your email. If you would like a copy of this form, click the PDF button.");
        }
        else {
            setIsFormSubmitted(false);
            setMessage("");
        }
    }

    const generatepdf = () => {
        if (isFormSubmitted) {
            setIsExpanded(true);

            let pdfList = [
                { id: 'page1img1', pageNumber: 1 },
                { id: 'summarystep1', pageNumber: 1 },
                { id: 'page1img2', pageNumber: 1 },
                { id: 'page1img3', pageNumber: 1 },
                { id: 'page2img1', pageNumber: 2 },
                { id: 'page2', pageNumber: 2 },
            ];

            setTimeout(async () => {
                const pdf = await generatePDF(pdfList, 'Statement and Evidence Submission');
               // pdf?.output('dataurlnewwindow', { filename: 'Statement and Evidence Submission' });
                pdf?.save('Statement and Evidence Submission');

                //pdf?.setProperties({
                //    title: "Statement and Evidence Submission"
                //});
                //pdf?.output('dataurlnewwindow');
            }, 500);
        }
    }

    const validateData = () => {
        let isValidForm = true;

        validateField();
        validateDriverLastName(applicantInfo.controlDriverLastName);
        validateEmailAddress(applicantInfo.applicantEmailAddress, "applicantEmailAddress");
        validateEmailAddress(applicantInfo.applicantEmailConfirm, "applicantEmailConfirm");
        validateFiles(applicantInfo.evidenceDocuments as FileList);
        getData();

        if (applicantInfo.applicantRoleSelect === '')
            setApplicantRoleErrorText('Please select an applicant role');
        else
            setApplicantRoleErrorText('');

        if (applicantInfo.signatureApplicantName === '')
            setSignatureApplicantNameErrorText('Please enter your name to confirm the information submitted is correct.');


        if (prohibitionNumberErrorText || driverLastNameErrorText || applicantRoleErrorText ||
            emailAddressErrorText || confirmEmailErrorText || fileUploadErrorText || signatureApplicantNameErrorText || isValidComboErrorText)
            setIsValidForm(false);
        else
            setIsValidForm(true);

    }

    const clearData = () => {
        setApplicantInfo({
            controlProhibitionNumber: '',
            isProhibitionNumberValid: false,
            controlIsUl: false,
            controlIsIrp: false,
            controlIsAdp: false,
            prohibitionNumberClean: '',
            controlDriverLastName: '',
            applicantRoleSelect: '',
            applicantEmailAddress: '',
            applicantEmailConfirm: '',
            signatureApplicantName: '',
        });
       
    }

    const getData =async () => {

       
        const formData = new FormData();
        formData.append('prohibition_number', applicantInfo.prohibitionNumberClean);
        formData.append('last_name', applicantInfo.controlDriverLastName);      

        const result = await postFormData(formData);

        setIsValidData(result?.data?.data?.is_valid);

        setApplicantInfo({ ...applicantInfo, isProhibitionNumberValid: result?.data?.data?.is_valid });    

        if (!result?.data?.data?.is_valid)
            setIsValidComboErrorText(result?.data?.data?.error);

    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setApplicantInfo({ ...applicantInfo, [name]: value });
    }    

    const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        validateEmailAddress(value, name);
    }


    const validateEmailAddress = (value: string, field: string) => {
            const emailAddressRegex = /^[^@]*@[a-zA-Z0-9-]{2,20}\.[a-zA-Z-.]{2,20}[a-zA-Z]$/;
            if (field === 'applicantEmailAddress') {
                if (value)
                    emailAddressRegex.exec(value) ? setEmailAddressErrorText('') : setEmailAddressErrorText('Incorrect email format, enter in format name@example.com');
                else
                    setEmailAddressErrorText('Please enter a valid email address.');
            } else if (value)
                value && value === applicantInfo.applicantEmailAddress ? setConfirmEmailErrorText('') : setConfirmEmailErrorText('Missing or incorrect value');
            else
                setConfirmEmailErrorText("Please enter the email again to confirm it's the same as the one above.");
    };

    


    const handleStep4Data = (step4Data:Step4Data) => {
        if (!step4Data.signatureApplicantErrorText)
            setApplicantInfo({ ...applicantInfo, signatureApplicantName: step4Data.signatureApplicantName });
        else
            setSignatureApplicantNameErrorText(step4Data.signatureApplicantErrorText);

    }

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files?.length) {

            let files = e.target.files;
            let allFilesValid = true;

            allFilesValid = validateFiles(files);
           
            if (allFilesValid) {
                setApplicantInfo({ ...applicantInfo, evidenceDocuments: files });
                setMessage("Upload Complete");
            }
            
        }
    }

    const validateFiles = (files :FileList): boolean => {
        let allFilesValid = true;

        if (files && files.length > 0) {

            [].forEach.call(files, file => {
                console.log("form3data.evidenceFile: ", applicantInfo.evidenceDocuments);

                let reader = new FileReader();
                reader.onload = async function (event) {
                    // The file's text will be printed here
                    let fileContent = await file2Base64(file);
                    console.log("size after: ", fileContent.length);

                    console.log("calling checkVirusScanner: ");
                    let isValidFile = await checkVirusScanner(fileContent.slice(fileContent.indexOf('base64,') + 7));

                    //add the file here
                    if (!isValidFile) {
                        setFileUploadErrorText('There is problem with a document. Please recheck the documents');
                        allFilesValid = false;
                    }
                };
            }
            );
            if (allFilesValid)
                setFileUploadErrorText('');
            return allFilesValid;
        }
        else {
            setFileUploadErrorText('Please attach your file(s).');
            return false;
        }

    }

   
    return (

        <div className="formContent">

            <div id="formContent" >
                <div id="page1img1">
                    <h1 className="header1" id="hed">Upload Evidence and Statement</h1>
                    <CustomAccordion title="Before You Begin:" id="step0" isExpanded={isExpanded}
                        content={<div style={{ fontSize: "16px", fontFamily: "'BC Sans', 'Noto Sans',  Arial, sans-serif", paddingLeft: '10px', lineHeight: '2.5' }}><p>When you see this symbol <Image
                            src="/./././assets/icons/info-icon.png"
                            width={15}
                            height={15}
                            alt="Info" />
                            &nbsp;click it for more information.
                        </p>
                            <p style={{ fontSize: '16px' }}>To complete the form:</p>
                            <ol style={{ paddingLeft:'30px' }}>
                                <li><strong><span style={{ fontSize: '16px' }}>Enter the prohibition number and last name from the notice</span></strong></li>
                                <li><strong><span style={{ fontSize: '16px' }}>Click the &apos;Next&apos; button</span></strong></li>
                                <li><span style={{ fontSize: '16px' }}>Read the guidelines</span></li><li><span style={{ fontSize: '16px' }}>Attach your file(s)</span></li>
                                <li><span style={{ fontSize: '16px' }}>Click Send</span></li>
                            </ol>
                           
                            <div><span style={{ fontSize: '16px' }}>You&apos;ll receive a confirmation email if you attached your file(s).&nbsp;</span></div>
                            <div><span style={{ fontSize: '16px' }}>If you don&apos;t enter anything in the form for 15 minutes, it may time out.</span></div>
                        </div>} />
                  </div>           

                <CustomAccordion title="Step 1: Confirm Applicant Information" id="step1" isExpanded={isExpanded}
                    content={<div style={{ display: 'grid', marginTop: '20px' }}>
                    <div id="page1img2">
                        <FormField
                            id="control-prohibition-number"
                            labelText="Prohibition No."
                            placeholder="Enter Prohibition No."
                            helperText="Format XX-XXXXXX"
                            tooltipTitle="Prohition No."
                            error={!validProhibitionNumber}
                            errorText={prohibitionNumberErrorText}
                            tooltipContent={<p>Enter first 8 numbers with the dash.Don&apos;t enter the digit in the grey box. Prohibition numbers start with 00, 21, 30 or 40.</p>}
                        >
                            <TextField key="key1" id="control-prohibition-number-field" style={{ paddingLeft: '5px' }}
                                variant="outlined"
                                value={applicantInfo.controlProhibitionNumber} onChange={prohibitionNumberChanged} onBlur={validateField}>
                            </TextField></FormField>
                        <div style={{ marginTop: '-30px', marginBottom: '30px' }}>
                            <Typography sx={{ color: '#313132', fontSize: '16px', fontWeight: '700', mt: '10px', ml: '10px', paddingBottom: '10px' }}>(optional)</Typography>

                            <Image src="/./././assets/images/Combo prohibition no.png" width={280}
                                height={180}
                                alt="Info" style={{ marginLeft: "10px", marginBottom: '20px', height: 'auto', width: 'auto' }}
                            />
                        </div>
                        <FormField
                            id="driver-last-name"
                            labelText="Driver's Last Name"
                            tooltipTitle="Driver's Last Name"
                            tooltipContent={<p>Enter the driver&apos;s last name exactly as it appears on the driver&apos;s licence.</p>}
                            error={validDriverLastName}
                            errorText={driverLastNameErrorText }

                        >
                            <TextField id="driver-last-name-field" style={{ paddingLeft: '5px' }}
                                variant="outlined" name='driverLastName'
                                value={applicantInfo.controlDriverLastName} onChange={driverLastNameChanged} onBlur={handleBlurDriverName} >
                            </TextField>
                        </FormField>
                        </div>
                        <Grid item xs={4} sx={{ padding: "1px" }}>
                            <Button variant="outlined" sx={{ cursor: 'pointer', color: '#003366', borderColor: '#003366', marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }}
                                onClick={getData}>
                                Next
                            </Button>
                        </Grid>
                        {!isValidData &&
                            <div>
                                <Typography variant="caption" sx={{ color: '#D8292F', fontWeight: '700', padding: '4px 0px 2px 0px', ml: '4px', fontSize: '16px', display: 'block' }}>

                                    {isValidComboErrorText}
                                </Typography>
                            </div>
                        }

                        {isValidData &&
                            <div>
                            <div id="page1img3">
                                    <Grid item xs={6} md={8} sm={10} lg={12} sx={{ padding: "1px", paddingBottom: '20px', paddingTop: '20px' }}>
                                        <div style={{ paddingBottom:'10px' }}>
                                        <strong style={{ fontSize: '16px', paddingLeft: '10px' }}> Applicant Contact Information:</strong>
                            </div>

                                        <Grid container spacing={2} sx={{ paddingTop:'10px' }} >
                                    <Grid item xs={5} sx={{ padding: "1px" }}>
                                        <FormField
                                            id="applicant-role-select"
                                            labelText="Applicant's Role:"
                                            tooltipTitle="Applicant's Role:"
                                            tooltipContent={<p>You can submit your evidence, or a lawyer or person you authorize can do it on your behalf.</p>}
                                            error={!!applicantRoleErrorText}
                                            errorText={applicantRoleErrorText}

                            >
                                <RadioGroup id="applicant-role-select-field"
                                    name="applicantRoleSelect" value={applicantInfo.applicantRoleSelect} onChange={handleChange} 
                                >
                                    <FormControlLabel value="driver" control={<Radio sx={{
                                        '&.Mui-checked': {
                                            color: 'rgb(49,49,50)',
                                        },
                                    }} />} label="Driver" />
                                    <FormControlLabel value="lawyer" control={<Radio sx={{
                                        '&.Mui-checked': {
                                            color: 'rgb(49,49,50)',
                                        },
                                    }} />} label="Law Office" />
                                    <FormControlLabel value="advocate" control={<Radio sx={{
                                        '&.Mui-checked': {
                                            color: 'rgb(49,49,50)',
                                        },
                                    }} />} label="Authorized Person" />
                                </RadioGroup>
                                        </FormField>
                                    </Grid>
                                    <Grid item xs={7} sx={{ padding: "1px" }}>
                                        {
                                            (applicantInfo.applicantRoleSelect === 'lawyer' || applicantInfo.applicantRoleSelect === 'advocate') &&
                                            <div className="noLicense" >
                                                <div>
                                                    <div style={{ display: 'inline-grid' }}>
                                                        <span style={{ fontSize: '14px' }} >
                                                            <strong> If you haven&apos;t submitted a signed consent from the driver authorizing you to send and receive documents on their behalf, you must upload it below. </strong>
                                                        </span>

                                                    </div>
                                                </div>
                                            </div>

                                        }
                                            </Grid>
                                        </Grid>
                                    </Grid> 
                                    </div>
                                    <div id="page2img1">
                                     <Grid item xs={5} sx={{ padding: "1px" }}>
                                    <FormField
                                        id="email-address"
                                        labelText="Email address to send your confirmation:"
                                        tooltipTitle="Email address to send your confirmation:"
                                        tooltipContent={<p>Please enter an email address for communication with RoadSafetyBC.</p>}
                                        error={!!emailAddressErrorText}
                                        errorText={emailAddressErrorText}
                                    >
                                        <TextField id="email-address-field" style={{ paddingLeft: '5px' }}
                                            variant="outlined" name='applicantEmailAddress'
                                            value={applicantInfo.applicantEmailAddress} onChange={handleChange} onBlur={handleBlur}>
                                        </TextField>
                                    </FormField>
                                    <FormField
                                        id="cnf-email-address"
                                        labelText="Confirm Email Address"
                                        tooltipTitle="Confirm Email Address"
                                        tooltipContent={<p>Please confirm the email address entered above.</p>}
                                        error={!!confirmEmailErrorText}
                                        errorText={confirmEmailErrorText}
                                    >
                                        <TextField id="cnf-email-address-field" style={{ paddingLeft: '5px' }}
                                            variant="outlined" name='applicantEmailConfirm'
                                            value={applicantInfo.applicantEmailConfirm} onChange={handleChange} onBlur={handleBlur}>
                                        </TextField>
                                    </FormField>
                                    </Grid>
                                   
                                    </div>
                                    </div>
                        }
                    </div>} />
                        <div id="page2">
                {isValidData &&
                    <div>
                <CustomAccordion title="Step 2: Read the Guidelines" id="step2" isExpanded={isExpanded}
                    content={<div style={{ fontSize: "16px", fontFamily: "'BC Sans', 'Noto Sans',  Arial, sans-serif", paddingLeft: '10px', lineHeight: '2.5' }}>
                        <div><span style={{ fontSize: "16px", }} > <strong>Providing Information</strong></span></div>
                        <ul style={{ fontSize: "16px", paddingLeft: '20px', paddingBottom: '20px', paddingTop:'10px' }}>
                            <li>You must provide the information you want considered <strong>2 days</strong> before your scheduled review.</li>
                            <li>The information you&apos;ll provide should address the grounds you chose on your application.</li>
                            <li>The adjudicator won&apos;t consider evidence you submit after the scheduled review date.</li>
                            <li>Hardship is not a consideration in a review.</li>
                        </ul>
                    </div>} />

                <CustomAccordion title="Step 3: Attach Statement and Evidence" id="step3" isExpanded={isExpanded}
                    content={<div style={{ fontSize: "16px", fontFamily: "'BC Sans', 'Noto Sans',  Arial, sans-serif", paddingLeft: '10px', lineHeight: '2.5' }}>
                        <div><span style={{ fontSize: "16px", }} > <strong>Things you should know</strong></span></div>
                        <div>
                        <ul style={{ fontSize: "16px", paddingLeft: '20px', paddingBottom: '20px', paddingTop: '10px' }}>
                            <li>If you have a slow Internet connection, it will take longer to upload your files. </li>
                            <li>You can upload as many files as you need, but the maximum size for a single file is 25MB.</li>
                            <li>The maximum total size for all the files in a single upload is 50MB.</li>
                            <li>You can return to this form to upload more files until 2 days before your review.</li>
                        </ul>
                        </div>
                        <div>
                            <div><span style={{ fontSize: '16px', }} > <strong>Accepted file types: </strong></span></div>
                            <ul style={{ fontSize: "16px", paddingLeft: '20px', paddingBottom: '20px', paddingTop: '10px' }}>
                                <li>.pdf, .doc, .docx, and .txt files</li>
                                <li>.xls, and .xlsx files</li>
                                <li>.png, .jpg and .gif files</li>
                            </ul>
                            <div> We will not accept cloud or Google docs for evidence. </div>
                        </div>
                        <Grid item xs={7} sx={{ padding: "1px" }}>
                            <FormField id="attach-consent"
                                labelText="Attach signed consent from driver"
                                tooltipTitle="Attach signed consent from driver"
                                tooltipContent={<p>Please upload signed consent from the driver, authorizing you to send and receive documents on their behalf.</p>}
                                error={!!fileUploadErrorText }
                                errorText={fileUploadErrorText }
                            >
                                <TextField
                                    id="outlined-basic"
                                    variant="outlined"
                                    type="file"
                                    inputProps={{
                                        multiple: true
                                    }}
                                    onChange={handleFileUpload }
                                />
                            </FormField>
                        </Grid>
                    </div>
                    } />

                            <CustomAccordion title="Step 4: Consent and Submit" id="step4" isExpanded={isExpanded}
                                content={<Step4 step4DatatoSend={handleStep4Data} errorText="" ref={step4Ref} />} />
                    </div>
                    }
                </div>

            </div>
            {!isValidForm &&
                <div id="errorText">
                    <Typography variant="caption" sx={{ color: '#D8292F', fontWeight: '700', padding: '4px 10px 20px 30px', ml: '4px', fontSize: '16px', display: 'block' }}>

                        Your form containes errors. Please correct them to proceed.
                    </Typography>

                </div>
            }
            {message &&
                <div id="messageDiv">
                    <Typography variant="caption" sx={{ color: '#555', fontWeight: '700', padding: '4px 10px 20px 30px', ml: '4px', fontSize: '16px', display: 'block', boxSizing: 'border-box' }}>
                        {message}
                    </Typography>

                </div>
            }

                <div style={{ paddingBottom: '40px' }}>
                    <Grid container spacing={2} >
                        <Grid item xs={6} sx={{ padding: "1px" }}></Grid>                  <Grid item xs={6} sx={{ padding: "1px" }}>
                            <Button onClick={clearData} variant="outlined" sx={{ cursor: 'pointer', color: '#003366', borderColor: '#003366', marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }} startIcon={<CloseIcon sx={{ fontWeight: 'bold' }} />}>
                                Clear
                        </Button>
                        <Button disabled={!isFormSubmitted} onClick={generatepdf} variant="outlined" sx={{ cursor: 'pointer', color: '#003366', borderColor: '#003366', marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }} startIcon={<Print sx={{ fontWeight: 'bold' }} />}>
                                PDF
                            </Button>
                        <Button onClick={submitData} variant="contained" disabled={isFormSubmitted} sx={{ borderColor: '#003366', backgroundColor: '#003366', color: 'white', marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }} startIcon={<ArrowForward sx={{ fontWeight: 'bold' }} />}>
                                Send
                            </Button>
                        </Grid>
                    </Grid>
                </div>


             
           
        </div>
    )

}


