import React from 'react';
import TextField from '@mui/material/TextField';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import dayjs from 'dayjs';

const Step4: React.FC = ( signatureApplicantName) => {

    const dateSigned = dayjs(Date.now());

    return (
        <div style={{ display: 'grid' }}>
            <div>
                <span style={{ fontSize: '16px' }} > <strong>By typing your name below and submitting this form, you confirm the information you provide above is correct. </strong></span>
            </div>
            <TextField className="signature" id="signature-applicant-name" style={{ paddingLeft: '5px' }}
                variant="outlined" name='signatureApplicantName' value={signatureApplicantName } >
            </TextField>
            <div className="step3Div" ><strong><span style={{ fontSize: '16px', paddingTop:'35px' }}>(optional)</span></strong></div>
            <LocalizationProvider dateAdapter={AdapterDayjs}  >
                <DatePicker disabled value={dateSigned} />
            </LocalizationProvider>
            <p style={{ paddingTop:'15px' }}>The personal information is collected under <a href="https://www.bclaws.ca/civix/document/id/complete/statreg/96165_03#section26" rel="noopener" target="_blank">s.26 (a) and (c)</a> of the Freedom of Information and Protection of Privacy Act for the purpose of administering the Motor Vehicle Act. If you have any questions about the collection, use and disclosure of the information collected contact RoadSafetyBC at PO Box 9254 Stn Prov Govt, Victoria, BC V8W 9J2. Phone (250) 387-7747.</p>
        </div>

    );
};
export default Step4;

