import Image from 'next/image';
import { FormField } from '../../components/FormField';
import { Radio, RadioGroup, FormControlLabel, Grid } from '@mui/material';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs, { Dayjs } from 'dayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import React, { useEffect, useState, } from 'react';
import { Step1Data, } from '../../interfaces';
import ProhibitionNumber from '../../components/ProhibitionNumber';

interface Props {
    step1DatatoSend: (data: Step1Data) => void;
}


const Step1: React.FC<Props> = ({ step1DatatoSend }) => {

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

    const [dateOfService, setDateOfService] = useState<Dayjs | null>(dayjs(Date.now()));
    const [validLicenseSeized, setValidLicenseSeized] = useState(true);
    const [showNoLicenseDiv, setShowNoLicenseDiv] = useState(false);    

    const handleProhibitionNumberChange = (data: { controlProhibitionNumber: string, controlIsUl: boolean, controlIsIrp: boolean, controlIsAdp: boolean, prohibitionNumberClean: string }) => {
        setStep1Data({
            ...step1Data,
            controlProhibitionNumber: data.controlProhibitionNumber,
            controlIsUl: data.controlIsUl,
            controlIsIrp: data.controlIsIrp,
            controlIsAdp: data.controlIsAdp,
            prohibitionNumberClean: data.prohibitionNumberClean,
        });
    };    

    useEffect(() => {
        step1DatatoSend(step1Data);
    });

    const licenseSeizedChanged = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        const isLicenseSeized = value === 'licenseSeized';
        setStep1Data({
            ...step1Data,
            licenseSeized: value,
            licenseNoSurrendered: value === 'licenseNoSurrendered',
            licenseLostOrStolen: value === 'licenseLostOrStolen',
            licenseNotIssued: value === 'licenseNotIssued' || value === 'licenseOutOfProvince',
        });
        setValidLicenseSeized(isLicenseSeized);
        setShowNoLicenseDiv(!isLicenseSeized);
        step1DatatoSend(step1Data);
    };

    const irpProhibitionTypeLengthChanged = (e: React.ChangeEvent<HTMLInputElement>) => {
        setStep1Data({ ...step1Data, irpProhibitionTypeLength: e.target.value });
        step1DatatoSend(step1Data);
    };

    const dateOfServiceChanged = (val: Dayjs) => {
        setDateOfService(val);
        step1DatatoSend(step1Data);
    };

    return (
        <div style={{ display: 'grid', marginTop: '20px' }}>
            <ProhibitionNumber onProhibitionDataChange={handleProhibitionNumberChange} ></ProhibitionNumber>
            <Grid container spacing={2} >
                <Grid item xs={5} sx={{ padding: "1px" }}>
                    {(step1Data.controlIsIrp === true || step1Data.controlIsAdp === true) &&
                        <FormField
                            id="license-seized"
                            labelText="Did the police take your driver's license?"
                            tooltipTitle="Did the police take your driver's license?"
                            tooltipContent={
                                <Image src="/./././assets/images/License Seized.png"
                                    width={1104}
                                    height={424}
                                    alt="Info"
                                    layout="responsive" style={{ marginLeft: "10px", marginBottom: '20px', height: 'auto', width: 'auto' }} />
                            }
                            error={!validLicenseSeized}
                            errorText="To use this form, the police must have taken your licence."
                        >
                            <RadioGroup id="license-seized-field"
                                aria-labelledby="demo-radio-buttons-group-label"
                                name="radio-buttons-group" value={step1Data.licenseSeized} onChange={licenseSeizedChanged}
                            >
                                <FormControlLabel value="licenseSeized" control={<Radio sx={{
                                    '&.Mui-checked': {
                                        color: 'rgb(49,49,50)',
                                    },
                                }} />} label="Yes" />
                                <FormControlLabel value="licenseNoSurrendered" control={<Radio sx={{
                                    '&.Mui-checked': {
                                        color: 'rgb(49,49,50)',
                                    },
                                }} />} label="No" />
                                <FormControlLabel value="licenseLostOrStolen" control={<Radio sx={{
                                    '&.Mui-checked': {
                                        color: 'rgb(49,49,50)',
                                    },
                                }} />} label="My Licence is lost or stolen" />
                                <FormControlLabel value="licenseNotIssued" control={<Radio sx={{
                                    '&.Mui-checked': {
                                        color: 'rgb(49,49,50)',
                                    },
                                }} />} label="I do not have a valid BC driver's license" />
                                <FormControlLabel value="outOfProvinceLicense" control={<Radio sx={{
                                    '&.Mui-checked': {
                                        color: 'rgb(49,49,50)',
                                    },
                                }} />} label="I have an out-of-province licence" />
                            </RadioGroup>
                        </FormField>
                    }
                </Grid>
                <Grid item xs={7} sx={{ padding: "1px" }}>
                    {
                        (step1Data.controlIsIrp === true || step1Data.controlIsAdp === true) && showNoLicenseDiv === true &&
                        <div className="noLicense" >
                            <div>
                                <div style={{ display: 'inline-grid' }}>
                                    <span style={{ fontSize: '14px' }} >
                                        <strong> You&apos;re ineligible to apply online because your licence wasn&apos;t surrendered to the police.</strong>
                                    </span>
                                    <span style={{ fontSize: '14px' }} >
                                        <strong>Apply in person for a review by:</strong>
                                    </span>
                                </div>

                                <ol style={{
                                    padding: 0, marginBottom: '10px', marginLeft: '25px', marginRight: '0px', marginTop: '20px'
                                }}>
                                    <li style={{ fontSize: '16px' }}><span style={{ fontSize: '14px' }} > <strong>Visiting&nbsp;<a href="https://www.icbc.com/driver-licensing/visit-dl-office/Pages/Book-a-knowledge-test-and-other-services.aspx" rel="noopener" target="_blank">ICBC,</a> select<a href="https://appointments.servicebc.gov.bc.ca/appointment" rel="noopener" target="_blank"> ServiceBC</a>&nbsp;centres, or an appointed agent within 7 days from the date the prohibition was issued.</strong></span></li>
                                    <li style={{ fontSize: '16px' }}><span style={{ fontSize: '14px' }} > <strong> Taking your notice with you.</strong></span></li>
                                    <li style={{ fontSize: '16px' }}><span style={{ fontSize: '14px' }}><strong>Surrendering your licence.</strong></span></li>
                                    <li style={{ fontSize: '16px' }}><span style={{ fontSize: '14px' }}> <strong>Completing an Application for a Review of a Driving Prohibition. </strong></span></li>
                                </ol>
                            </div>
                        </div>

                    }
                </Grid>
            </Grid>

            {(step1Data.controlIsIrp === true && step1Data.licenseSeized === "licenseSeized") &&
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
                    errorText=""

                >
                    <RadioGroup id="irp-prohibition-type-length-field"
                        name="radio-buttons-group" value={step1Data.irpProhibitionTypeLength} onChange={irpProhibitionTypeLengthChanged}
                    >
                        <FormControlLabel value="3-days-warn" control={<Radio sx={{
                            '&, &.Mui-checked': {
                                color: 'rgb(49,49,50)',
                            },
                        }} />} label="3 days WARN" />
                        <FormControlLabel value="7-days-warn" control={<Radio sx={{
                            '&, &.Mui-checked': {
                                color: 'rgb(49,49,50)',
                            },
                        }} />} label="7 days WARN" />
                        <FormControlLabel value="30-days-warn" control={<Radio sx={{
                            '&, &.Mui-checked': {
                                color: 'rgb(49,49,50)',
                            },
                        }} />} label="30 days WARN" />
                        <FormControlLabel value="90-days-fail" control={<Radio sx={{
                            '&, &.Mui-checked': {
                                color: 'rgb(49,49,50)',
                            },
                        }} />} label="90 days FAIL" />
                        <FormControlLabel value="90-days-refusal" control={<Radio sx={{
                            '&, &.Mui-checked': {
                                color: 'rgb(49,49,50)',
                            },
                        }} />} label="90 days REFUSAL" />
                    </RadioGroup>
                </FormField>
            }
            {((step1Data.controlIsIrp === true && step1Data.licenseSeized === "licenseSeized" && (step1Data.irpProhibitionTypeLength === '3-days-warn' ||
                step1Data.irpProhibitionTypeLength === '7-days-warn' ||
                step1Data.irpProhibitionTypeLength === '30-days-warn' ||
                step1Data.irpProhibitionTypeLength === '90-days-fail' ||
                step1Data.irpProhibitionTypeLength === '90-days-refusal')) || (step1Data.controlIsAdp === true && step1Data.licenseSeized === "licenseSeized") ||
                (step1Data.controlIsUl === true)) &&
                <FormField
                    id="prohibition-issued-date"
                    labelText="When was the prohibition issued?"
                    placeholder="MM/DD/YYYY"
                    tooltipTitle="Did the police take your driver's license?"
                    tooltipContent={<p>Enter first 8 numbers with the dash.Don&apos;t enter the digit in the grey box. Prohibition numbers start with 00, 21, 30 or 40.</p>}
                    error={true}
                    errorText=""
                    helperText="Click calendar button and select date"
                >
                    <LocalizationProvider dateAdapter={AdapterDayjs} >
                        <DatePicker
                            disableFuture
                            value={dateOfService}
                            onChange={(newValue) => dateOfServiceChanged(newValue as Dayjs)}

                        />
                    </LocalizationProvider>
                </FormField>
            }

        </div>

    );
};
export default Step1;

