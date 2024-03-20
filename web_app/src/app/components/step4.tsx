/* eslint-disable react/display-name */
import React, { useState, forwardRef, useImperativeHandle } from 'react';
import TextField from '@mui/material/TextField';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import dayjs from 'dayjs';
import { FormField } from './FormField';
import { Step4Data } from '../interfaces';

interface Props {
    step4DatatoSend: (data: Step4Data) => void; 
}

const Step4 = forwardRef((props: Props, ref) => {

    const dateSigned = dayjs(Date.now());

    const [step4Data, setStep4Data] = useState<Step4Data>({
        signatureApplicantName: '',
        signedDate: dayjs(Date.now()).toDate(),
        signatureApplicantErrorText:'',
    });

    const [signatureApplicantNameErrorText, setSignatureApplicantNameErrorText] = useState('');

    const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
        const value = e.target.value;
        validate(value);

    }

    useImperativeHandle(ref, () => ({
        clearData() {
            setStep4Data({
                signatureApplicantName: '',
                signedDate: dayjs(Date.now()).toDate(),
                signatureApplicantErrorText: '',
            });
        },
        validate() {
            validate(step4Data.signatureApplicantName);
        }
    }));

    const validate = (value:string) => {
        if (value === '')
            setSignatureApplicantNameErrorText('Please enter your name to confirm the information submitted is correct.');
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {

        setStep4Data({ ...step4Data, signatureApplicantName: e.target.value });
        props.step4DatatoSend(step4Data);
    };



    return (
        <div style={{ display: 'grid' }} id="page5">
            <div>
                <span style={{ fontSize: '16px', paddingLeft:'15px' }} > <strong>By typing your name below and submitting this form, you confirm the information you provide above is correct. </strong></span>
            </div>
            <FormField
                id="signature-applicant-name"
                error={!!(signatureApplicantNameErrorText)}
                errorText={signatureApplicantNameErrorText}
            >
                <TextField className="signature" id="signature-applicant-name"
                    variant="outlined" name='signatureApplicantName' value={step4Data.signatureApplicantName} onChange={handleChange} onBlur={handleBlur }>
                </TextField>
            </FormField>
           
            <div className="step3Div" ><strong><span style={{ fontSize: '16px', paddingTop: '35px', paddingLeft:'13px' }}>(optional)</span></strong></div>
            <FormField
                id="prohibition-issued-date"
                labelText=""
                placeholder="MM/DD/YYYY" 
                
            >
                <LocalizationProvider dateAdapter={AdapterDayjs}  >
                    <DatePicker sx={{paddingLeft:'5px'} }
                        disableFuture
                        value={dateSigned}
                        disabled

                    />
                </LocalizationProvider>
            </FormField>
          
            <p style={{ paddingTop: '15px', fontSize:'16px', }}>The personal information is collected under <a href="https://www.bclaws.ca/civix/document/id/complete/statreg/96165_03#section26" rel="noopener" target="_blank">s.26 (a) and (c)</a> of the Freedom of Information and Protection of Privacy Act for the purpose of administering the Motor Vehicle Act. If you have any questions about the collection, use and disclosure of the information collected contact RoadSafetyBC at PO Box 9254 Stn Prov Govt, Victoria, BC V8W 9J2. Phone (250) 387-7747.</p>
            
        </div>

    );
});
export default Step4;

