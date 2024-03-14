import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import dayjs from 'dayjs';
import { FormField } from '../../components/FormField';
import { Step4Data } from '../../interfaces';

interface Props {
    step4DatatoSend: (data: Step4Data) => void;
}

const Step4: React.FC<Props> = ({ step4DatatoSend }) => {

    const dateSigned = dayjs(Date.now());

    const [step4Data, setStep4Data] = useState<Step4Data>({
        signatureApplicantName: '',
        signedDate: dayjs(Date.now()).toDate(),
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {

        setStep4Data({ ...step4Data, signatureApplicantName: e.target.value });
        step4DatatoSend(step4Data);
    };

    return (
        <div style={{ display: 'grid' }} id="page5">
            <div>
                <span style={{ fontSize: '16px', paddingLeft:'15px' }} > <strong>By typing your name below and submitting this form, you confirm the information you provide above is correct. </strong></span>
            </div>
            <FormField
                id="signature-applicant-name"
            >
                <TextField className="signature" id="signature-applicant-name" 
                    variant="outlined" name='signatureApplicantName' value={step4Data.signatureApplicantName} onChange={handleChange}>
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
            {/*<LocalizationProvider dateAdapter={AdapterDayjs}  >*/}
            {/*    <DatePicker disabled value={dateSigned} />*/}
            {/*</LocalizationProvider>*/}
            <p style={{ paddingTop: '15px' }}>The personal information is collected under <a href="https://www.bclaws.ca/civix/document/id/complete/statreg/96165_03#section26" rel="noopener" target="_blank">s.26 (a) and (c)</a> of the Freedom of Information and Protection of Privacy Act for the purpose of administering the Motor Vehicle Act. If you have any questions about the collection, use and disclosure of the information collected contact RoadSafetyBC at PO Box 9254 Stn Prov Govt, Victoria, BC V8W 9J2. Phone (250) 387-7747.</p>
            <div style={{paddingTop:'30px'} }><strong><span style={{ fontSize: '16px'}} >Submit only 1 online application for your prohibition review.</span></strong></div>
        </div>

    );
};
export default Step4;

