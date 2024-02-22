import CustomAccordion from '../../components/Accordion';
import Image from 'next/image';
import { FormField } from '../../components/FormField';
import TextField from '@mui/material/TextField';
import { Radio, RadioGroup, FormControlLabel, Typography, Step } from '@mui/material';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs, { Dayjs } from 'dayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import React, { useState, memo, Children  } from 'react';
import { Today } from '@mui/icons-material';
import { FC } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { Unstable_NumberInput as NumberInput } from '@mui/base/Unstable_NumberInput';

interface step1Data {
    controlProhibitionNumber: string;
    controlIsUl: boolean;
    controlIsIrp: boolean;
    controlIsAdp: boolean;
    prohibitionNumberClean: string;
    licenseSiezed: string;
    licenseNoSurrendered: boolean;
    licenseLostOrStolen: boolean;
    licenseNotIssued: boolean;
    irpProhibitionTypeLength: string;
    dateOfService?: Date;
}


const Step1 = () => {
    let [controlProhibitionNumber, setControlProhibitionNumber] = useState('');
    let [controlIsUl, setControlIsUl] = useState(false);
    let [controlIsIrp, setControlIsIrp] = useState(false);
    let [controlIsAdp, setControlIsAdp] = useState(false);
    let [prohibitionNumberClean, setProhibitionNumberClean] = useState('');
    let [licenseSiezed, setLicenseSiezed] = useState('');
    let [licenseNoSurrendered, setLicenseNoSurrendered] = useState('');
    let [licenseLostOrStolen, setLicenseLostOrStolen] = useState('');
    let [licenseNotIssued, setLicenseNotIssued] = useState('');
    let [irpProhibitionTypeLength, setIrpProhibitionTypeLength] = useState('');
    let [dateOfService, setDateOfService] = React.useState<Dayjs | null>(dayjs(Date.now()));
    let [prohibitionNumberErrorText, setProhibitionNumberErrorText] = useState('');
    let [showNoLicenseDiv, setShowNoLicenseDiv] = useState(false);
    
    const prohibitionNumberChanged = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setControlProhibitionNumber(value);     
    };

    const licenseSiezedChanged = (e: React.ChangeEvent<HTMLInputElement>) => {
        setLicenseSiezed(e.target.value);
        if (licenseSiezed !== "licenseSeized")
            setShowNoLicenseDiv(true);
    };

    const irpProhibitionTypeLengthChanged = (e: React.ChangeEvent<HTMLInputElement>) => {
        setIrpProhibitionTypeLength(e.target.value);
    };

    const dateChanged = (e: React.ChangeEvent<HTMLInputElement>) => {
        //setDateOfService(e.target.value);
    };
    
    let validControlProhibitionNumber = true;

    const validateField = (event: React.FocusEvent<HTMLInputElement>) => {
        console.log("hi");
        if (controlProhibitionNumber !== "" && !controlProhibitionNumber.match("^(00|21|30|40).\d{6}$")) {
            validControlProhibitionNumber = true;
            if (controlProhibitionNumber.indexOf("30") == 0) {
                setControlIsUl(true);
                setControlIsIrp(false);
                setControlIsAdp(false);
            }
            else if (controlProhibitionNumber.indexOf("21") == 0 || controlProhibitionNumber.indexOf("40") == 0) {
                setControlIsUl(false);
                setControlIsIrp(true);
                setControlIsAdp(false);
            }
            else if (controlProhibitionNumber.indexOf("00") == 0) {
                setControlIsUl(false);
                setControlIsIrp(false);
                setControlIsAdp(true);
            }
            else {
                setControlIsUl(false);
                setControlIsIrp(false);
                setControlIsAdp(false);
            }

            setProhibitionNumberClean(controlProhibitionNumber.replace("-", ""));
            console.log(controlIsUl);
            console.log(prohibitionNumberClean);
            console.log("hi");
        }
        else {
            if (controlProhibitionNumber === "" || controlProhibitionNumber === undefined || controlProhibitionNumber === null) {
                setProhibitionNumberErrorText("Enter prohibition number found on the notice.");
            }
            else {
                setProhibitionNumberErrorText("Enter first 8 numbers with the dash. Don't enter the digit in the grey box. Prohibition numbers start with 00, 21, 30 or 40.");
            }
            console.log("error")
            validControlProhibitionNumber = false;
            setControlIsUl(false);
            setControlIsIrp(false);
            setControlIsAdp(false);
        }
    }

    let validateLicenseSeized = () => {
        return false
    }



    return (<CustomAccordion title="Step 1: Enter Prohibition Information"
        content={
            <div>                  
                <FormField
                    id="control-prohibition-number"
                    labelText="Prohibition No."
                    placeholder="Enter Prohibition No."
                    helperText="Format XX-XXXXXX"                   
                    tooltipTitle="Prohition No."
                    error={!validControlProhibitionNumber}
                    errorText={prohibitionNumberErrorText }
                    tooltipContent={<p>Enter first 8 numbers with the dash.Don&apos;t enter the digit in the grey box. Prohibition numbers start with 00, 21, 30 or 40.</p>}
                >
                    <TextField key="key1" id="control-prohibition-number-field" autoFocus style={{paddingLeft:'5px'} }
                        variant="outlined"
                        value={controlProhibitionNumber} onChange={prohibitionNumberChanged} onBlur ={validateField }>
                    </TextField></FormField>
                

                <Typography  sx={{ color: '#313132', fontSize:'16px', fontWeight:'700',  mt: '10px', ml: '10px', paddingBottom:'10px' }}>(optional)</Typography>
               
                <Image src="/./././assets/images/Combo prohibition no.png"
                    width={280}
                    height={180}
                    alt="Info" style={{marginLeft:"10px", marginBottom:'20px'} }
                    />               
            
                {(controlIsIrp === true || controlIsAdp === true) &&
                    <FormField 
                        id="license-seized"
                        labelText="Did the police take your driver's license?"
                        tooltipTitle="Did the police take your driver's license?"
                        tooltipContent={
                            <Image src="/./././assets/images/License Seized.png"
                                width={280}
                                height={180}
                                alt="Info" />
                        }
                        error={validateLicenseSeized()}
                        errorText="hi error"
                    >
                    <div className="row">
                        <RadioGroup id="license-seized-field"
                            aria-labelledby="demo-radio-buttons-group-label"
                            name="radio-buttons-group" value={licenseSiezed} onChange={licenseSiezedChanged }
                        >
                            <FormControlLabel value="licenseSeized" control={<Radio />} label="Yes" />
                            <FormControlLabel value="licenseNoSurrendered" control={<Radio />} label="No" />
                            <FormControlLabel value="licenseLostOrStolen" control={<Radio />} label="My Licence is lost or stolen" />
                            <FormControlLabel value="licenseNotIssued" control={<Radio />} label="I do not have a valid BC driver's license" />
                            <FormControlLabel value="outOfProvinceLicense" control={<Radio />} label="I have an out-of-province licence" />
                            </RadioGroup>
                            {showNoLicenseDiv === true &&
                                <div className="noLicense">
                                    <div className="xforms-output-output">
                                        <div><span style={{ fontSize: '14px' }} >
                                            <strong> You&apos;re ineligible to apply online because your licence wasn&apos;t surrendered to the police. Apply in person for a review by:</strong></span></div>
                                        <div>&nbsp;</div>
                                        <ol><li><span style={{ fontSize: '14px' }} > <strong>Visiting&nbsp;<a href="https://www.icbc.com/driver-licensing/visit-dl-office/Pages/Book-a-knowledge-test-and-other-services.aspx" rel="noopener" target="_blank">ICBC,</a> select<a href="https://appointments.servicebc.gov.bc.ca/appointment" rel="noopener" target="_blank"> ServiceBC</a>&nbsp;centres, or an appointed agent within 7 days from the date the prohibition was issued.</strong></span></li><li><span style={{ fontSize: '14px' }} > <strong> Taking your notice with you.</strong></span></li><li><span style={{ fontSize: '14px' }}><strong>Surrendering your licence.</strong></span></li><li><span style={{ fontSize: '14px' }}> <strong>Completing an Application for a Review of a Driving Prohibition. </strong></span></li></ol></div>
                                </div>
                            }
                        </div>
                    </FormField>
                }
                
                {(controlIsIrp === true && licenseSiezed === "licenseSeized") &&
                    <FormField
                        id="irp-prohibition-type-length"
                        labelText="Please select prohibition type and length"
                        tooltipTitle="Please select prohibition type and length"
                        tooltipContent={
                            <Image src="/./././assets/images/Prohibition Period and Type.png"
                                width={280}
                                height={180}
                                alt="Info" />
                        }
                        error={true}
                        errorText="hi error"
                    >
                        <RadioGroup id="irp-prohibition-type-length-field"
                            aria-labelledby="demo-radio-buttons-group-label"
                            name="radio-buttons-group" value={irpProhibitionTypeLength} onChange={irpProhibitionTypeLengthChanged}
                        >
                            <FormControlLabel value="3-days-warn" control={<Radio />} label="3 days WARN" />
                            <FormControlLabel value="7-days-warn" control={<Radio />} label="7 days WARN" />
                            <FormControlLabel value="30-days-warn" control={<Radio />} label="30 days WARN" />
                            <FormControlLabel value="90-days-fail" control={<Radio />} label="90 days FAIL" />
                            <FormControlLabel value="90-days-refusal" control={<Radio />} label="90 days REFUSAL" />
                        </RadioGroup>
                    </FormField>
                }
                {((controlIsIrp === true && licenseSiezed === "licenseSeized") || (controlIsAdp === true && licenseSiezed === "licenseSeized") || 
                (controlIsUl === true)) &&
                    <FormField
                        id="prohibition-issued-date"
                        labelText="When was the prohibition issued?"
                        placeholder="MM/DD/YYYY"
                        tooltipTitle="Did the police take your driver's license?"
                        tooltipContent={<p>Enter first 8 numbers with the dash.Don&apos;t enter the digit in the grey box. Prohibition numbers start with 00, 21, 30 or 40.</p>}
                        error={true}
                        errorText="hi error"
                    >
                        <LocalizationProvider dateAdapter={AdapterDayjs}>                               
                                <DatePicker
                                label="Controlled picker" disableFuture 
                                    value={dateOfService}
                                onChange={(newValue) => setDateOfService(newValue)}
                                />
                        </LocalizationProvider>
                    </FormField>
                }

        </div>
    } />
);
};
export default Step1;

