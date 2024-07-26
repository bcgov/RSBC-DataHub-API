/* eslint-disable react/display-name */
import React, { useState, forwardRef, useImperativeHandle } from 'react';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import dayjs from 'dayjs';
import { FormField } from './FormField';
import { Step4Data } from '../interfaces';
import { TextField, SxProps, Theme } from '@mui/material';

interface Props {
    step4DatatoSend: (data: Step4Data) => void;
}

const Step4 = forwardRef((props: Props, ref) => {

    const dateSigned = dayjs(Date.now());
    const offsetHour = '-0'+ (new Date().getTimezoneOffset())/60 + ':00';
    const [step4Data, setStep4Data] = useState<Step4Data>({
        signatureApplicantName: '',
        signedDate: dayjs(Date.now()).toISOString().substring(0, 10) + offsetHour,
        signatureApplicantErrorText: '',
    });

    const [signatureApplicantNameErrorText, setSignatureApplicantNameErrorText] = useState('');

    const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
        const value = e.currentTarget.value;
        validate(value);
        if (value === '') {
            setStep4Data({ ...step4Data, signatureApplicantName: e.currentTarget.value });
            props.step4DatatoSend(step4Data);
        }
    }

    useImperativeHandle(ref, () => ({
        validate() {
            validate(step4Data.signatureApplicantName);
        },
        clearData() {
            setStep4Data({
                signatureApplicantName: '',
                signedDate: dayjs(Date.now()).toISOString().substring(0, 10) + offsetHour,
                signatureApplicantErrorText: '',
            });
        }
    }));

    const validate = (value: string) => {
        if (value === '') {
            setSignatureApplicantNameErrorText('Please enter your name to confirm the information submitted is correct.');
            step4Data.signatureApplicantErrorText = signatureApplicantNameErrorText;
        } else {
            setSignatureApplicantNameErrorText('');
        }
        //console.log("step4Data.signedDate: ", step4Data.signedDate);
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setStep4Data({ ...step4Data, signatureApplicantName: e.currentTarget.value });
        props.step4DatatoSend(step4Data);
    };


    return (
        <div style={{ display: 'grid' }} id="page5">
            <div>
                <span style={{ fontSize: '16px', paddingLeft: '15px' }} > <strong>By typing your name below and submitting this form, you confirm the information you provide above is correct. </strong></span>
            </div>
            <FormField 
                id="signature-applicant-name"
                labelText=""
                tooltipTitle=""
                error={!!(signatureApplicantNameErrorText)}
                errorText={signatureApplicantNameErrorText}
            >
                <TextField
                    className="signature"
                    id="signature-applicant-name"
                    variant="outlined"
                    name='signatureApplicantName'
                    value={step4Data.signatureApplicantName}
                    onChange={handleChange}
                    onBlur={handleBlur}>
                </TextField>
            </FormField>

            <FormField
                id="prohibition-issued-date"
                labelText=""
                placeholder="MM/DD/YYYY"
            >
                <LocalizationProvider dateAdapter={AdapterDayjs}  >
                    <DatePicker sx={{ paddingLeft: '5px' }}
                        disableFuture
                        value={dateSigned}
                        disabled
                    />
                </LocalizationProvider>
            </FormField>

            <p style={{ paddingTop: '15px', fontSize: '16px', }}>The personal information is collected under <a href="https://www.bclaws.ca/civix/document/id/complete/statreg/96165_03#section26" rel="noopener" target="_blank">s.26 (a) and (c)</a> of the Freedom of Information and Protection of Privacy Act for the purpose of administering the Motor Vehicle Act. If you have any questions about the collection, use and disclosure of the information collected contact RoadSafetyBC at PO Box 9254 Stn Prov Govt, Victoria, BC V8W 9J2. Phone (250) 387-7747.</p>

        </div>

    );
});
export default Step4;

