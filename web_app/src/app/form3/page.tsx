'use client'
import React, { useState, useRef, useEffect } from 'react';
import Image from 'next/image';
import CustomAccordion from '../components/Accordion';
import { Button, Grid, TextField, Typography, RadioGroup, FormControlLabel, Radio, IconButton } from '@mui/material';
import { generatePDF } from '../components/GeneratePDF';
import { FormField } from '../components/FormField';
import { postValidateFormData, sendForm3Email, submitToApi } from "./actions";
import CloseIcon from '@mui/icons-material/Close';
import DeleteIcon from '@mui/icons-material/Delete';
import ArrowForward from '@mui/icons-material/ArrowForward';
import { Print } from '@mui/icons-material';
import Step4 from '../components/step4';
import { checkVirusScanner } from '@/app/_nonRoutingAssets/lib/virusScanApi';
import { file2Base64 } from '@/app/_nonRoutingAssets/lib/util';
import { Form3Data, Step4Data } from '../interfaces';

export default function Page() {

    const [applicantInfo, setApplicantInfo] = useState<Form3Data>({
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

    const [message, setMessage] = useState('');
    const step4Ref = useRef<{ clearData: () => void, validate: () => void }>(null);
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
    const [filesContent, setFilesContent] = useState<string[]>([]);
    const [filesNames, setFilesNames] = useState<string[]>([]);
    const [fileNamesMessage, setFileNamesMessage] = useState('');
    const [isExpanded, setIsExpanded] = useState<boolean>(false);
    const [isValidForm, setIsValidForm] = useState<boolean>(true);
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
        setApplicantInfo({ ...applicantInfo, controlDriverLastName: e.target.value });
    }
    const handleBlurDriverName = (e: React.FocusEvent<HTMLInputElement>) => {
        validateDriverLastName(e.target.value);
    }

    const validateDriverLastName = (value: string) => {
        if (value === '') {
            setValidDriverLastName(false);
            setDriverLastNameErrorText("Please enter the driver's last name.");
        }
        else {
            setValidDriverLastName(true);
            setDriverLastNameErrorText('');
        }
    }

    async function submitData() {
        let message = "There was an error.";
        let formSubmitted = false;
        if (validateData()) {
            try {
                console.log("before submission:");
                const result = await submitToApi(applicantInfo);
                console.log("result after submission:");
                console.log(result);
                formSubmitted = result.data.is_success;
                message = result.data.error;
            } catch (error) { }
            try {
                console.log("file names before email call: ", filesNames);
                const emailResult = await sendForm3Email(filesContent, filesNames, applicantInfo);

                if (formSubmitted && emailResult.data.is_success)
                    message = "Your documents are sent. Please check your email. If you would like a copy of this form, click the PDF button.";
                else
                    message += emailResult.data?.error;
            } catch (error) { }
        }
        setIsFormSubmitted(formSubmitted);
        setMessage(message);
    }

    useEffect(() => {
        console.log(isFormSubmitted, message, fileNamesMessage);
    }, [isFormSubmitted, message, fileNamesMessage]);

    const generatePdfAction = () => {
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
                pdf?.save('Statement and Evidence Submission');
            }, 500);
        }
    }

    const validateData = () => {
        let isApplicantValid = true;
        if (applicantInfo.applicantRoleSelect === '') {
            isApplicantValid = false;
            setApplicantRoleErrorText('Please select an applicant role');
        }
        if (applicantInfo.signatureApplicantName === '') {
            setSignatureApplicantNameErrorText('Please enter your name to confirm the information submitted is correct.');
            isApplicantValid = false;
        }

        console.log("valid?", isApplicantValid, prohibitionNumberErrorText, driverLastNameErrorText,
            emailAddressErrorText, confirmEmailErrorText, fileUploadErrorText, isValidComboErrorText);

        if (!isApplicantValid || prohibitionNumberErrorText || driverLastNameErrorText ||
            emailAddressErrorText || confirmEmailErrorText || fileUploadErrorText || isValidComboErrorText)
            isApplicantValid = false;

        setIsValidForm(isApplicantValid);
        console.log("validation is finished", isApplicantValid);
        return isApplicantValid;
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
        setIsValidData(false);
        setMessage('');
        setFileNamesMessage('');
        setFilesContent([]);
        setFilesNames([]);
    }

    const callValidateFormData = async () => {

        try {
            const result = await postValidateFormData(applicantInfo);
            console.log("callValidateFormData:", result.data, result.data.is_success, result);
            setIsValidData(result.data.is_success);

            setApplicantInfo({ ...applicantInfo, isProhibitionNumberValid: result.data.is_success });

            if (!result.data.is_success)
                setIsValidComboErrorText("Error: " + result.data.error);
            console.log("finished...")
        } catch (error) {
            setIsValidData(false);
            setIsValidComboErrorText("Error: System failed to process your request.");

        }
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.currentTarget;
        console.log("name/value: ", name, value);
        setApplicantInfo({ ...applicantInfo, [name]: value });
    }

    const handleBlurEmailAddress = (e: React.FocusEvent<HTMLInputElement>) => {
        const { name, value } = e.currentTarget;
        console.log("blur name/value: ", name, value);
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

    const handleStep4Data = (step4Data: Step4Data) => {
        console.log("set signiture: ", step4Data.signatureApplicantName);
        if (!step4Data.signatureApplicantName)
            setSignatureApplicantNameErrorText('Please enter your name to confirm the information submitted is correct.');
        else
            setApplicantInfo({ ...applicantInfo, signatureApplicantName: step4Data.signatureApplicantName });
    }

    const fileUploadRef = useRef<HTMLInputElement | null>(null);

    const handleCleanFileUpload = () => {
        setFilesNames([]);
        setFilesContent([]);
        setFileNamesMessage('');
        if (fileUploadRef.current) {
            console.log("calling ref", fileUploadRef, fileUploadRef.current);
            fileUploadRef.current.value = "";
            fileUploadRef.current.type = "text";
            fileUploadRef.current.type = "file";
        }
        setMessage("Upload files removed.")
        console.log("handleCleanFileUpload", filesContent.length, filesNames);
    }

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        // Remove elements from filesContent
        if (e.target.files?.length) {

            let files = e.target.files;
            let allFilesValid = true;

            allFilesValid = validateFiles(files);

            if (allFilesValid) {
                setMessage("Upload Complete");
            }

        }
    }

    const validateFiles = (files: FileList): boolean => {
        let allFilesValid = true;

        if (files && files.length > 0) {
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                console.log("evidenceFile: ", file.name);
                let reader = new FileReader();
                reader.onload = async function (event) {
                    // The file's text will be printed here
                    let fileContent: string = await file2Base64(file);
                    console.log("calling checkVirusScanner: ");
                    //add the file here
                    if (await checkVirusScanner(fileContent)) {
                        if (!filesNames.some(name => name === file.name)) {
                            filesContent.push(fileContent);
                            filesNames.push(file.name);
                            setFilesContent(filesContent);
                            setFilesNames(filesNames);
                        }
                    } else {
                        setFileUploadErrorText('There is problem with a document. Please recheck the documents');
                        allFilesValid = false;
                    }
                    console.log("file names after: ", filesNames);
                };
                reader.readAsDataURL(file);
            }
            setFileNamesMessage(filesNames.join(', '));

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
                            <ol style={{ paddingLeft: '30px' }}>
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
                                tooltipTitle="Prohibition No."
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

                                <img src="/./././assets/images/Combo_prohibition_no.png" width={280}
                                    height={180}
                                    alt="Info" />
                            </div>
                            <FormField
                                id="driver-last-name"
                                labelText="Driver's Last Name"
                                tooltipTitle="Driver's Last Name"
                                tooltipContent={<p>Enter the driver&apos;s last name exactly as it appears on the driver&apos;s licence.</p>}
                                error={validDriverLastName}
                                errorText={driverLastNameErrorText}

                            >
                                <TextField id="driver-last-name-field" style={{ paddingLeft: '5px' }}
                                    variant="outlined" name='driverLastName'
                                    value={applicantInfo.controlDriverLastName} onChange={driverLastNameChanged} onBlur={handleBlurDriverName} >
                                </TextField>
                            </FormField>
                        </div>
                        <Grid item xs={4} sx={{ padding: "1px" }}>
                            <Button variant="outlined" sx={{ cursor: 'pointer', color: '#003366', borderColor: '#003366', marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }}
                                onClick={callValidateFormData}>
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
                                        <div style={{ paddingBottom: '10px' }}>
                                            <strong style={{ fontSize: '16px', paddingLeft: '10px' }}> Applicant Contact Information:</strong>
                                        </div>

                                        <Grid container spacing={2} sx={{ paddingTop: '10px' }} >
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
                                                                    <strong> If you haven&apos;t submitted a signed consent from the driver authorizing you to send and receive documents on their behalf. </strong>
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
                                                value={applicantInfo.applicantEmailAddress} onChange={handleChange} onBlur={handleBlurEmailAddress}>
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
                                                value={applicantInfo.applicantEmailConfirm} onChange={handleChange} onBlur={handleBlurEmailAddress}>
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
                                    <ul style={{ fontSize: "16px", paddingLeft: '20px', paddingBottom: '20px', paddingTop: '10px' }}>
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
                                        <FormField id="attach-evidence"
                                            labelText="Attach statements and evidence from driver"
                                            tooltipTitle="Attach statements and evidence from driver"
                                            tooltipContent={<p>Please upload statements and evidences.</p>}
                                            error={!!fileUploadErrorText}
                                            errorText={fileUploadErrorText}
                                        >
                                            <TextField
                                                id="outlined-basic"
                                                variant="outlined"
                                                type="file"
                                                inputRef={fileUploadRef}
                                                inputProps={{
                                                    multiple: true
                                                }}
                                                onChange={handleFileUpload}
                                            />
                                            <IconButton aria-label="delete" size="small" onClick={handleCleanFileUpload}>
                                                <DeleteIcon fontSize="inherit" />
                                            </IconButton>
                                        </FormField>
                                        {fileNamesMessage &&
                                            <div id="messageDiv">
                                                Attached: {fileNamesMessage}
                                            </div>
                                        }
                                    </Grid>
                                </div>
                                } />

                            <CustomAccordion title="Step 4: Consent and Submit" id="step4" isExpanded={isExpanded}
                                content={<Step4 step4DatatoSend={handleStep4Data} ref={step4Ref} />} />
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
                    <Typography variant="caption" sx={{ color: '#D8292F', fontWeight: '700', padding: '4px 10px 20px 30px', ml: '4px', fontSize: '16px', display: 'block', boxSizing: 'border-box' }}>
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
                        <Button disabled={!isFormSubmitted} onClick={generatePdfAction} variant="outlined" sx={{ cursor: 'pointer', color: '#003366', borderColor: '#003366', marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }} startIcon={<Print sx={{ fontWeight: 'bold' }} />}>
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


