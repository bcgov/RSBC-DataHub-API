/* eslint-disable react/display-name */
import Image from 'next/image';
import { FormField } from '../../components/FormField';
import TextField from '@mui/material/TextField';
import { Radio, RadioGroup, FormControlLabel, Grid, MenuItem, Select, InputAdornment, Input, IconButton, } from '@mui/material';
import CallIcon from '@mui/icons-material/Call';
import DeleteIcon from '@mui/icons-material/Delete';
import React, { useEffect, useState, forwardRef, useImperativeHandle, useRef } from 'react';
import { Step2Data, Step2DataErrors } from '../../interfaces';
import { checkVirusScanner } from '@/app/_nonRoutingAssets/lib/virusScanApi';
import { file2Base64 } from '@/app/_nonRoutingAssets/lib/util';

interface Props {
    step2DatatoSend: (data: Step2Data) => void;
    isEnabled: boolean;
    hasError: boolean;
}

const Step2 = forwardRef((props: Props, ref) => {

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
        consentFile: '',
        consentFileName: '',
        hasError: false,
    });

    const [step2DataErrors, setStep2DataErrors] = useState<Step2DataErrors>({});
    const [consentFile, setFile] = useState<File | null>();
    const [fileUploadMessage, setFileUploadMessage] = useState('');

    useImperativeHandle(ref, () => ({
        validate() {
            let hasErrors = 0;
            hasErrors = validate('applicantRoleSelect', step2Data.applicantRoleSelect);
            if (step2Data.applicantRoleSelect !== 'driver') {
                hasErrors += validate('driverLastName', step2Data.driverLastName);
                hasErrors += validate('driverFirstName', step2Data.driverFirstName);
                hasErrors += validate('consentFile', consentFile?.name ?? '');
            }
           return hasErrors > 0;
        },
        clearData() {
            setFile(null);
            setFileUploadMessage('');
            setStep2DataErrors({});
            setStep2Data({
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
                consentFile: '',
                consentFileName: '',
                hasError: false,
            });
        }
    }));

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setStep2Data({ ...step2Data, [name]: value });
        props.step2DatatoSend(step2Data);
    }

    const handleProvinceChange = (value: string) => {
        setStep2Data({ ...step2Data, controlDriverProvince: value });
        props.step2DatatoSend(step2Data);
    }

    const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        validate(name, value);
    }

    const fileUploadRef = useRef<HTMLInputElement | null>(null);

    const handleCleanFileUpload = () => {
        setFile(null);
        setStep2Data({ ...step2Data, consentFile: '', consentFileName: '' });
        if (fileUploadRef.current) {
            //console.log("calling ref", fileUploadRef, fileUploadRef.current);
            fileUploadRef.current.value = "";
            fileUploadRef.current.type = "text";
            fileUploadRef.current.type = "file";
        }
        setFileUploadMessage("Upload file removed.")
        //console.log("handleCleanFileUpload", step2Data.consentFileName);
    }

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files?.length) {
            var file = e.target.files[0];
            var fileContent: string = await file2Base64(file);
            //console.log("calling checkVirusScanner: ", fileContent.length);
            if (await checkVirusScanner(fileContent)) {
                setStep2Data({ ...step2Data, consentFile: fileContent, consentFileName: file.name });
                setFile(file);
                setFileUploadMessage("Upload Complete");
                setStep2DataErrors({...setStep2DataErrors, 'fileUploadErrorText': '',});
                setStep2Data({ ...step2Data, hasError: false });
            } else {
                setFileUploadMessage('');
                setStep2DataErrors({...setStep2DataErrors, 'fileUploadErrorText':'There is a problem with the uploaded document. Please recheck the documents'});
                setStep2Data({ ...step2Data, hasError: true });
            }
            props.step2DatatoSend(step2Data);
        }
    }

    const validateApplicantName = (value: string, errors: Step2DataErrors, field: 'applicantFirstName'
        | 'applicantLastName'
        | 'driverFirstName'
        | 'driverLastName'
        | 'streetAddress'
        | 'controlDriverCityTown'
        | 'controlDriverProvince'
        | 'applicantRoleSelect') => {
        errors[field] = value ? '' : `${getErrorMessage(field)}.`;
        if((field === 'applicantFirstName' || field ==='driverFirstName')
            && step2Data.applicantRoleSelect === '' ) {
                errors['applicantRoleSelect'] = getErrorMessage('applicantRoleSelect');
        }
        if( field === 'applicantRoleSelect') {
            errors.applicantRoleSelect = '';
            errors.fileUploadErrorText = '';
            errors.driverFirstName = '';
            errors.driverLastName = '';
        }
        if (field === 'applicantRoleSelect' && value !== 'driver') {
            if (step2Data.driverFirstName === '')
                errors.driverFirstName = getErrorMessage('driverFirstName');
            if (step2Data.driverLastName === '')
                errors.driverLastName = getErrorMessage('driverLastName');
        }
        console.log("errors: ", errors );
    };

    const getErrorMessage = (field: string) => {
        switch (field) {
            case 'applicantFirstName': return "Please enter the applicant's first name";
            case 'applicantLastName': return "Please enter the applicant's last name";
            case 'driverFirstName': return "Please enter the driver's first name";
            case 'driverLastName': return "Please enter the driver's last name";
            case 'streetAddress': return "Please enter the street address";
            case 'controlDriverCityTown': return "Please enter the name of the city";
            case 'controlDriverProvince': return "Please select a province";
            case 'applicantRoleSelect': return "Please select a role"
        }
    }

    const validatePhoneNumber = (value: string, errors: Step2DataErrors) => {
        const phNumberRegex = /^(?:\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$/;
        if (value) {
            errors.applicantPhoneNumber = phNumberRegex.exec(value) ? '' : 'Missing or incorrect value';
        }
        else
            errors.applicantPhoneNumber = 'Please provide an area code and phone number.';
    };

    const validateEmailAddress = (value: string, errors: Step2DataErrors, field: 'applicantEmailAddress' | 'applicantEmailConfirm') => {
        const emailAddressRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (field === 'applicantEmailAddress') {
            if (value)
                errors.applicantEmailAddress = emailAddressRegex.exec(value) ? '' : 'Incorrect email format, enter in format name@example.com';
            else
                errors.applicantEmailAddress = 'Please enter a valid email address.';
        } else if (value)
            errors.applicantEmailConfirm = value && value === step2Data.applicantEmailAddress ? '' : 'Missing or incorrect value';
        else
            errors.applicantEmailConfirm = "Please enter the email again to confirm it's the same as the one above.";
    };

    const validatePostalCode = (value: string, errors: Step2DataErrors) => {
        const postalCodeRegex1 = /^[ABCEGHJ-NPRSTVXYabceghj-nprstvxy]\d[ABCEGHJ-NPRSTV-Zabceghj-nprstv-z] \d[ABCEGHJ-NPRSTV-Zabceghj-nprstv-z]\d$/;
        const postalCodeRegex2 = /^[ABCEGHJ-NPRSTVXYabceghj-nprstvxy]\d[ABCEGHJ-NPRSTV-Zabceghj-nprstv-z]\d[ABCEGHJ-NPRSTV-Zabceghj-nprstv-z]\d$/;
        if (value)
            errors.controlDriverPostalCode = (postalCodeRegex1.exec(value.trimEnd()) || postalCodeRegex2.exec(value.trimEnd())) ? '' : 'Enter in format A1A 1A1.';
        else
            errors.controlDriverPostalCode = 'Please enter a postal code.';
    };

    const validateConsentFile  = (value: string, errors: Step2DataErrors) => {
        if (step2Data.applicantRoleSelect !== 'driver' && value === '' ){
            errors.fileUploadErrorText = 'A consent file must be uploaded.';
        } else {
            errors.fileUploadErrorText = '';
        }
    }

    const validate = (fieldName: string, value: string) => {
        let errors: Step2DataErrors = { ...step2DataErrors };

        switch (fieldName) {
            case 'applicantFirstName':
            case 'applicantLastName':
            case 'driverFirstName':
            case 'driverLastName':
            case 'streetAddress':
            case 'controlDriverCityTown':
            case 'controlDriverProvince':
            case 'applicantRoleSelect':
                validateApplicantName(value, errors, fieldName);
                break;
            case 'applicantPhoneNumber':
                validatePhoneNumber(value, errors);
                break;
            case 'applicantEmailAddress':
            case 'applicantEmailConfirm':
                validateEmailAddress(value, errors, fieldName);
                break;
            case 'controlDriverPostalCode':
                validatePostalCode(value, errors);
                break;
            case 'consentFile':
                validateConsentFile(value, errors);
                break;
            default:
                break;
        }

        setStep2DataErrors(errors);
        props.step2DatatoSend(step2Data);
        if (Object.values(errors).every(value => value === null || value === '')) {
            setStep2Data({ ...step2Data, hasError: false });              
            return 0;
        } else {
            setStep2Data({ ...step2Data, hasError: true });
            return 1;
        }
    };

    const handleChangePhoneNumber = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newInput = event.target.value.replace(/\D/g, '');
        const newValueArr = [
          newInput.slice(0, 3),
          newInput.slice(3, 6),
          newInput.slice(6, 10)
        ].filter(x => x);
    
        const newValue = newValueArr.join('-');
        const { name } = event.target;
        setStep2Data({ ...step2Data, [name]: newValue });
        props.step2DatatoSend(step2Data);    
    };

    return (
        <div style={{ display: 'grid', marginTop: '20px', pointerEvents: (props.isEnabled ? '' : 'none') as React.CSSProperties["pointerEvents"], }} >
            <div id="page2img2">
                <Grid item xs={6} md={8} sm={10} lg={12} sx={{ padding: "1px", paddingBottom: '20px' }}>
                    <strong style={{ fontSize: '16px', paddingBottom: '20px', paddingLeft: '10px' }}> Applicant Information:</strong>
                </Grid>
                <Grid item xs={8} sx={{ padding: "1px" }}>
                    <FormField
                        id="applicant-role-select"
                        labelText="Applicant's Role:"
                        tooltipTitle="Applicant's Role:"
                        tooltipContent={<p>You can submit your application, or a lawyer or person you authorize can do it on your behalf.</p>}
                        error={!!step2DataErrors.applicantRoleSelect}
                        errorText={step2DataErrors.applicantRoleSelect}        
                >
                        <RadioGroup id="applicant-role-select-field"
                            name="applicantRoleSelect" value={step2Data.applicantRoleSelect} onChange={handleChange} onBlur={handleBlur}
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
                {step2Data.applicantRoleSelect === 'driver' &&
                    <Grid item xs={8} sx={{ padding: "1px" }}>
                        <FormField
                            id="represented-by-lawyer"
                            labelText="Are you represented by a lawyer?"
                            tooltipTitle="Applicant's Role:"
                            tooltipContent={<p>You can submit your application, or a lawyer or person you authorize can do it on your behalf.</p>}
                        >
                            <RadioGroup id="represented-by-lawyer-field"
                                aria-labelledby="demo-radio-buttons-group-label"
                                name="representedByLawyer" value={step2Data.representedByLawyer} onChange={handleChange} onBlur={handleBlur}
                            >
                                <FormControlLabel value="yes" control={<Radio sx={{
                                    '&.Mui-checked': {
                                        color: 'rgb(49,49,50)',
                                    },
                                }} />} label="Yes" />
                                <FormControlLabel value="no" control={<Radio sx={{
                                    '&.Mui-checked': {
                                        color: 'rgb(49,49,50)',
                                    },
                                }} />} label="No" />
                            </RadioGroup>
                        </FormField>
                    </Grid>
                }
                {
                    (step2Data.applicantRoleSelect === 'lawyer' || step2Data.applicantRoleSelect === 'advocate') &&
                    <div id="attachConsentDiv" style={{ marginTop: '-20px', paddingLeft: '10px' }}>
                        <Grid container spacing={2} >
                            <Grid item xs={7} sx={{ padding: "1px" }}>
                                <div className="attachConsent" >
                                    <div style={{ lineHeight: '1' }}><strong style={{ fontSize: '14px', lineHeight: '1.25' }}> Before the review you must provide a signed consent from the driver authorizing you to send and receive documents on their behalf.&nbsp;</strong></div>
                                    <div style={{ lineHeight: '1' }}><strong style={{ fontSize: '14px' }}>Upload the signed consent below or on the evidence submission form. You&apos;ll have access to the evidence form after you pay and schedule the review. </strong></div></div>
                            </Grid>
                            <Grid item xs={5} sx={{ padding: "1px" }}>
                            </Grid>
                        </Grid>
                        <Grid container spacing={2} style={{ paddingTop: '30px' }} >
                            <Grid item xs={7} sx={{ padding: "1px" }}>
                                <FormField id="attach-consent"
                                    labelText="Attach signed consent from driver"
                                    tooltipTitle="Attach signed consent from driver"
                                    tooltipContent={<p>Please upload signed consent from the driver, authorizing you to send and receive documents on their behalf.</p>}
                                    error={!!step2DataErrors.fileUploadErrorText}
                                    errorText={step2DataErrors.fileUploadErrorText}>
                                    <TextField
                                        id="outlined-basic"
                                        variant="outlined"
                                        type="file"
                                        inputRef={fileUploadRef}
                                        onChange={handleFileUpload} />
                                    <IconButton aria-label="delete" size="small"  onClick={handleCleanFileUpload}>
                                        <DeleteIcon fontSize="inherit" />
                                    </IconButton>
                                </FormField>
                            </Grid>
                            <Grid item xs={5} sx={{ padding: "1px" }}>
                            </Grid>
                        </Grid>
                    </div>
                }
                {(step2Data.applicantRoleSelect === 'lawyer' || (step2Data.applicantRoleSelect === 'driver' && step2Data.representedByLawyer === 'yes')) && <strong style={{ fontSize: '16px', paddingBottom: '20px', paddingLeft: '10px' }}> Lawyer Information:</strong>}
                {step2Data.applicantRoleSelect === 'advocate' && <strong style={{ fontSize: '16px', paddingBottom: '20px', paddingLeft: '10px' }}> Authorized person Information:</strong>}
                <FormField
                    id="first-name"
                    labelText="First Name"
                    tooltipTitle="First Name"
                    tooltipContent={<p>Please enter your first name.</p>}
                    error={!!step2DataErrors.applicantFirstName}
                    errorText={step2DataErrors.applicantFirstName}
                >
                    <TextField id="first-name-field" style={{ paddingLeft: '5px' }} inputProps={{ maxLength: '35' }}
                        variant="outlined" name='applicantFirstName'
                        value={step2Data.applicantFirstName} onChange={handleChange} onBlur={handleBlur}>
                    </TextField>
                </FormField>
                <FormField
                    id="last-name"
                    labelText="Last Name"
                    tooltipTitle="Last Name"
                    tooltipContent={<p>If you&apos;re the driver, enter your last name exactly as it is on your licence.</p>}
                    error={!!step2DataErrors.applicantLastName}
                    errorText={step2DataErrors.applicantLastName}
                >
                    <TextField id="last-name-field" style={{ paddingLeft: '5px' }}
                        variant="outlined" name='applicantLastName'
                        value={step2Data.applicantLastName} onChange={handleChange} onBlur={handleBlur} >
                    </TextField>
                </FormField>
            </div>
            <div id="page3img1">
                <FormField
                    id="ph-number"
                    labelText="Phone Number"
                    tooltipTitle="Phone Number"
                    tooltipContent={<p>Please provide an area code and phone number where RoadSafetyBC can contact you.</p>}
                    error={!!step2DataErrors.applicantPhoneNumber}
                    errorText={step2DataErrors.applicantPhoneNumber}
                >
                    <TextField id="ph-number-field" 
                        style={{ paddingLeft: '5px' }} 
                        placeholder="(555) 555-5555"
                        variant="outlined" 
                        name='applicantPhoneNumber'
                        value={step2Data.applicantPhoneNumber} 
                        onChange={ handleChangePhoneNumber}
                        onBlur={handleBlur} 
                        InputProps={{
                            endAdornment: (
                                <InputAdornment position="end">
                                    <CallIcon />
                                </InputAdornment>
                            )
                        }} >
                    </TextField>
                </FormField>
                {((step2Data.applicantRoleSelect === 'driver' && step2Data.representedByLawyer === 'yes'))
                    && <strong style={{ fontSize: '16px', paddingBottom: '20px', paddingLeft: '10px' }}> Driver Contact Information:</strong>}
                <FormField
                    id="email-address"
                    labelText="Email Address"
                    tooltipTitle="Email Address"
                    tooltipContent={<p>Please enter a valid email address to receive emails with your next steps.</p>}
                    error={!!step2DataErrors.applicantEmailAddress}
                    errorText={step2DataErrors.applicantEmailAddress}
                >
                    <TextField id="email-address-field" style={{ paddingLeft: '5px' }}
                        variant="outlined" name='applicantEmailAddress'
                        value={step2Data.applicantEmailAddress} onChange={handleChange} onBlur={handleBlur}>
                    </TextField>
                </FormField>
                <FormField
                    id="cnf-email-address"
                    labelText="Confirm Email Address"
                    tooltipTitle="Confirm Email Address"
                    tooltipContent={<p>Please confirm the email address entered above.</p>}
                    error={!!step2DataErrors.applicantEmailConfirm}
                    errorText={step2DataErrors.applicantEmailConfirm}
                >
                    <TextField id="cnf-email-address-field" style={{ paddingLeft: '5px' }}
                        variant="outlined" name='applicantEmailConfirm'
                        value={step2Data.applicantEmailConfirm} onChange={handleChange} onBlur={handleBlur}>
                    </TextField>
                </FormField>
            </div>
            <div id="page3img2">
                {((step2Data.applicantRoleSelect === 'driver' && step2Data.representedByLawyer === 'yes') ||
                    step2Data.applicantRoleSelect === 'lawyer' ||
                    step2Data.applicantRoleSelect === 'advocate') &&
                    <strong style={{ fontSize: '16px', paddingBottom: '20px', paddingLeft: '10px' }}> Driver Information:</strong>
                }
                {((step2Data.applicantRoleSelect === 'driver' && step2Data.representedByLawyer === 'yes') ||
                    step2Data.applicantRoleSelect === 'lawyer' ||
                    step2Data.applicantRoleSelect === 'advocate') &&
                    <div>
                        <FormField
                            id="driver-first-name"
                            labelText="Driver's First Name"
                            tooltipTitle="Driver's First Name"
                            tooltipContent={<p>Please enter the driver&apos;s first name.</p>}
                            error={!!step2DataErrors.driverFirstName}
                            errorText={step2DataErrors.driverFirstName}
                        >
                            <TextField id="driver-first-name-field" style={{ paddingLeft: '5px' }} inputProps={{ maxLength: '35' }}
                                variant="outlined" name='driverFirstName'
                                value={step2Data.driverFirstName} onChange={handleChange} onBlur={handleBlur}>
                            </TextField>
                        </FormField>
                        <FormField
                            id="driver-last-name"
                            labelText="Driver's Last Name"
                            tooltipTitle="Driver's Last Name"
                            tooltipContent={<p>Enter the driver&apos;s last name exactly as it appears on the driver&apos;s licence.</p>}
                            error={!!step2DataErrors.driverLastName}
                            errorText={step2DataErrors.driverLastName}
                        >
                            <TextField id="driver-last-name-field" style={{ paddingLeft: '5px' }}
                                variant="outlined" name='driverLastName'
                                value={step2Data.driverLastName} onChange={handleChange} onBlur={handleBlur} >
                            </TextField>
                        </FormField>
                    </div>
                }
                <FormField
                    id="bc-driver-license-no"
                    labelText="BC Driver License No. (optional)"
                    helperText="Optional"
                    tooltipTitle="BC Driver License No."
                    tooltipContent={<Image src="/assets/images/BC Driver License Number.png" width={280}
                        height={180}
                        alt="Info" style={{ marginLeft: "10px", marginBottom: '20px', height: 'auto', width: 'auto' }}
                    />}
                    error={!!step2DataErrors.driverBcdl}
                    errorText={step2DataErrors.driverBcdl}
                >
                    <TextField id="bc-driver-license-no-field" style={{ paddingLeft: '5px' }}
                        variant="outlined" name='driverBcdl'
                        value={step2Data.driverBcdl} onChange={handleChange} onBlur={handleBlur}>
                    </TextField>
                </FormField>
                <strong style={{ fontSize: '16px', paddingBottom: '30px', paddingLeft: '10px' }}>Address where you want the decision mailed:</strong>
                <FormField
                    id="address"
                    labelText="Address"
                    helperText="Example: 1234 Main Street"
                    tooltipTitle="Address"
                    tooltipContent={<p>Please enter a street address.</p>}
                    error={!!step2DataErrors.streetAddress}
                    errorText={step2DataErrors.streetAddress}
                >
                    <TextField id="address-field" style={{ paddingLeft: '5px', minWidth: '400px' }}
                        variant="outlined" name='streetAddress'
                        value={step2Data.streetAddress} onChange={handleChange} onBlur={handleBlur}>
                    </TextField>
                </FormField>
                <FormField
                    id="city"
                    labelText="City/Town"
                    tooltipTitle="City/Town"
                    tooltipContent={<p>Please enter the city.</p>}
                    error={!!step2DataErrors.controlDriverCityTown}
                    errorText={step2DataErrors.controlDriverCityTown}
                >
                    <TextField id="city-field" style={{ paddingLeft: '5px' }}
                        variant="outlined" name='controlDriverCityTown'
                        value={step2Data.controlDriverCityTown} onChange={handleChange} onBlur={handleBlur}>
                    </TextField>
                </FormField>
            </div>
            <div id="page4img1">
                <FormField
                    id="province"
                    labelText="Province"
                    tooltipTitle="Province"
                    tooltipContent={<p>Please select a province</p>}
                    error={!!step2DataErrors.controlDriverProvince}
                    errorText={step2DataErrors.controlDriverProvince}
                >
                    <Select labelId="province" id="province-field" name="controlDriverProvince" value={step2Data.controlDriverProvince}
                        onChange={event => handleProvinceChange(event.target.value)} onBlur={handleBlur}
                        style={{ minWidth: '300px' }}  >
                        <MenuItem value="british-columbia"> British Columbia</MenuItem>
                        <MenuItem value="alberta">Alberta</MenuItem>
                        <MenuItem value="saskatchewan"> Saskatchewan </MenuItem>
                        <MenuItem value="manitoba"> Manitoba </MenuItem>
                        <MenuItem value="ontario"> Ontario </MenuItem>
                        <MenuItem value="quebec"> Quebec </MenuItem>
                        <MenuItem value="new-brunswick"> New Brunswick </MenuItem>
                        <MenuItem value="nova-scotia"> Nova Scotia </MenuItem>
                        <MenuItem value="prince-edward-island"> Prince Edward Island </MenuItem>
                        <MenuItem value="newfoundland-and-labrador"> Newfoundland and Labrador </MenuItem>
                        <MenuItem value="yukon"> Yukon </MenuItem>
                        <MenuItem value="northwest-territories"> Northwest Territories </MenuItem>
                        <MenuItem value="nunavut"> Nunavut </MenuItem>
                    </Select>
                </FormField>
                <FormField
                    id="postal-code"
                    labelText="Postal Code"
                    helperText="Example: A1A1A1"
                    tooltipTitle="Postal Code"
                    tooltipContent={<p>Please enter a valid postal code in either format A1A 1A1 or A1A1A1.</p>}
                    error={!!step2DataErrors.controlDriverPostalCode}
                    errorText={step2DataErrors.controlDriverPostalCode}
                >
                    <TextField id="postal-code-field" style={{ paddingLeft: '5px' }}
                        variant="outlined" name='controlDriverPostalCode'
                        value={step2Data.controlDriverPostalCode} onChange={handleChange} onBlur={handleBlur}>
                    </TextField>
                </FormField>
            </div>
        </div>

    );
});
export default Step2;

