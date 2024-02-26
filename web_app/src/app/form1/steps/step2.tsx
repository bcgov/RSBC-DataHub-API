import Image from 'next/image';
import { FormField } from '../../components/FormField';
import TextField from '@mui/material/TextField';
import { Radio, RadioGroup, FormControlLabel, Grid, MenuItem, Select, InputAdornment } from '@mui/material';
import CallIcon from '@mui/icons-material/Call';
import React, { useState, } from 'react';

type InputState = {
    value: string;
    error: boolean;
    errorMessage: string;
}

const formData : Record<string, InputState> = {
    applicantRoleSelect: { value: '', error: false, errorMessage: '' },
    applicantRole: { value: '', error: false, errorMessage: '' },
    representedByLawyer: { value: '', error: false, errorMessage: '' },
    firstName: { value: '', error: false, errorMessage: '' },
    lastName: { value: '', error: false, errorMessage: '' },
    phNumber: { value: '', error: false, errorMessage: '' },
    emailAddress: { value: '', error: false, errorMessage: '' },
    cnfEmailAddress: { value: '', error: false, errorMessage: '' },
    bcDriverLicenseNo: { value: '', error: false, errorMessage: '' },
    address: { value: '', error: false, errorMessage: '' },
    city: { value: '', error: false, errorMessage: '' },
    province: { value: '', error: false, errorMessage: '' },
    postalCode: { value: '', error: false, errorMessage: '' },
    }

const Step2: React.FC = () => {

    const [stepData2, setStepData2] = useState<Record<string, InputState>>(formData);

    const [file, setFile] = useState<File>();
   

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        console.log(e.target);
        const { name, value } = e.target;
        setStepData2({
            ...stepData2,
            [name]: { ...stepData2[name], value, error: false, errorMessage: '' },
        });
    }   
        
    return (
            <div style={{ display: 'grid' }}>
               
            <FormField
                    id="applicant-role-select"
                    labelText="Applicant's Role:"
                tooltipTitle="Applicant's Role:"
                tooltipContent={<p>You can submit your application, or a lawyer or person you authorize can do it on your behalf.</p>}
            >
                <RadioGroup id="applicant-role-select-field"
                    name="radio-buttons-group" value={stepData2.applicantRole} onChange={handleChange}
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
            {stepData2.applicantRoleSelect.value === 'driver' &&
                <FormField
                    id="represented-by-lawyer"
                    labelText="Are you represented by a lawyer?"
                    tooltipTitle="Applicant's Role:"
                    tooltipContent={<p>You can submit your application, or a lawyer or person you authorize can do it on your behalf.</p>}
                >
                    <RadioGroup id="represented-by-lawyer-field"
                        aria-labelledby="demo-radio-buttons-group-label"
                        name="represented-by-lawyer" value={stepData2.representedByLawyer} onChange={handleChange}
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
            }
            {
               // (stepData2.applicantRoleSelect === 'lawOffice' || stepData2.applicantRoleSelect === 'authorizedPerson') &&
                <div id="attachConsentDiv">
                    <Grid container spacing={2} >
                        <Grid item xs={7} sx={{ padding: "1px" }}>
                        <div className="attachConsent">
                            <div><strong style={{ fontSize: '14px', lineHeight:'1.25' }}> Before the review you must provide a signed consent from the driver authorizing you to send and receive documents on their behalf.&nbsp;</strong></div>
                            <div><strong style={{ fontSize: '14px' }}>Upload the signed consent below or on the evidence submission form. You&apos;ll have access to the evidence form after you pay and schedule the review. </strong></div></div>
                        </Grid>
                        <Grid item xs={5} sx={{ padding: "1px" }}>                            
                        </Grid>
                    </Grid>
                    <Grid container spacing={2} >
                        <Grid item xs={7} sx={{ padding: "1px" }}>
                            <FormField id="attach-consent"
                                labelText="Attach signed consent from driver"
                                tooltipTitle="Attach signed consent from driver"
                                tooltipContent={<p>Please upload signed consent from the driver, authorizing you to send and receive documents on their behalf.</p>}>
                                <input type="file" name="file" onChange={(e) => { setFile(e.target.files?.[0]); console.log(file?.size) } }  />
                            </FormField>
                        </Grid>
                        <Grid item xs={5} sx={{ padding: "1px" }}>
                        </Grid>
                    </Grid>
                </div>
            }
            {stepData2.applicantRoleSelect.value === 'lawyer' && <strong> Lawyer Information:</strong>}
            {stepData2.applicantRoleSelect.value === 'advocate' && <strong> Authorized person Information:</strong>}
            <FormField
                id="first-name"
                labelText="First Name"
                tooltipTitle="First Name"
                tooltipContent={<p>Please enter your first name.</p>}
                error={stepData2.firstName.error}
                errorText={stepData2.firstName.errorMessage }
            >
                <TextField id="first-name-field" style={{ paddingLeft: '5px' }} inputProps={{maxLength:'35'} }
                    variant="outlined" name='firstName'
                    value={stepData2.firstName.value} onChange={handleChange} >
                </TextField>
            </FormField>
            <FormField
                id="last-name"
                labelText="Last Name"
                tooltipTitle="Last Name"
                tooltipContent={<p>If you&apos;re the driver, enter your last name exactly as it is on your licence.</p>}
            >
                <TextField id="last-name-field" style={{ paddingLeft: '5px' }}
                    variant="outlined" name='lastName'
                    value={stepData2.lastName.value} onChange={handleChange} >
                </TextField>
            </FormField>
            <FormField
                id="ph-number" 
                labelText="Phone Number"
                tooltipTitle="Phone Number"
                tooltipContent={<p>Please provide an area code and phone number where RoadSafetyBC can contact you.</p>}
            >
                <TextField id="ph-number-field" style={{ paddingLeft: '5px' }} placeholder="(555) 555-5555" 
                    variant="outlined" name='phNumber'
                    value={stepData2.phNumber.value} onChange={handleChange} InputProps={{
                        endAdornment: (
                            <InputAdornment position="end">
                            <CallIcon />
                            </InputAdornment>
                    ) }} >
                </TextField>
            </FormField>
            <FormField
                id="email-address"
                labelText="Email Address"
                tooltipTitle="Email Address"
                tooltipContent={<p>Please enter a valid email address to receive emails with your next steps.</p>}
            >
                <TextField id="email-address-field" style={{ paddingLeft: '5px' }} 
                    variant="outlined" name='emailAddress'
                    value={stepData2.emailAddress.value} onChange={handleChange}>
                </TextField>
            </FormField>
            <FormField
                id="cnf-email-address"
                labelText="Confirm Email Address"
                tooltipTitle="Confirm Email Address"
                tooltipContent={<p>Please confirm the email address entered above.</p>}
            >
                <TextField id="cnf-email-address-field" style={{ paddingLeft: '5px' }} 
                    variant="outlined" name='cnfEmailAddress'
                    value={stepData2.cnfEmailAddress.value} onChange={handleChange}>
                </TextField>
            </FormField>
            <FormField
                id="bc-driver-license-no"
                labelText="BC Driver License No. (optional)"
                helperText="Optional"
                tooltipTitle="BC Driver License No."
                tooltipContent={<Image src="/./././assets/images/BC Driver License Number.png" width={280}
                    height={180}
                    alt="Info" style={{ marginLeft: "10px", marginBottom: '20px', height: 'auto', width: 'auto' }}
                />}
            >
                <TextField id="bc-driver-license-no-field" style={{ paddingLeft: '5px' }} 
                    variant="outlined" name='bcDriverLicenseNo'
                    value={stepData2.bcDriverLicenseNo.value} onChange={handleChange}>
                </TextField>
            </FormField>
            <p>Address where you want the decision mailed:</p>
            <FormField
                id="address"
                labelText="Address"
                helperText="Example: 1234 Main Street"
                tooltipTitle="Address"
                tooltipContent={<p>Please enter a street address.</p>}
            >
                <TextField id="address-field" style={{ paddingLeft: '5px' }} 
                    variant="outlined" name='address'
                    value={stepData2.address.value} onChange={handleChange}>
                </TextField>
            </FormField>
            <FormField
                id="city"
                labelText="City/Town"
                tooltipTitle="City/Town"
                tooltipContent={<p>Please enter the city.</p>}
            >
                <TextField id="city-field" style={{ paddingLeft: '5px' }} 
                    variant="outlined" name='city'
                    value={stepData2.city.value} onChange={handleChange}>
                </TextField>
            </FormField>
            <FormField
                id="province"
                labelText="Province"
                tooltipTitle="Province"
                tooltipContent={<p>Please select a province</p>}
            >
                <Select labelId="province" id="province-field" name="province" value={stepData2.province.value}  >
                    <MenuItem value="BritishColumbia"> British Columbia</MenuItem>
                    <MenuItem value="Alberta">Alberts</MenuItem>
                    <MenuItem value="Saskatchewan"> Saskatchewan </MenuItem>
                    <MenuItem value="Manitoba"> Manitoba </MenuItem>
                    <MenuItem value="Ontario"> Ontario </MenuItem>
                    <MenuItem value="Quebec"> Quebec </MenuItem>
                    <MenuItem value="New Brunswick"> New Brunswick </MenuItem>
                    <MenuItem value="Nova Scotia"> Nova Scotia </MenuItem>
                    <MenuItem value="Prince Edward Island"> Prince Edward Island </MenuItem>
                    <MenuItem value="Newfoundland and Labrador"> Newfoundland and Labrador </MenuItem>
                    <MenuItem value="Yukon"> Yukon </MenuItem>
                    <MenuItem value="Northwest Territories"> Northwest Territories </MenuItem>
                    <MenuItem value="Nunavut"> Nunavut </MenuItem>
                </Select>
            </FormField>
            <FormField
                id="postal-code"
                labelText="Postal Code"
                helperText="Example: A1A1A1"
                tooltipTitle="Postal Code"
                tooltipContent={<p>Please enter a valid postal code in either format A1A 1A1 or A1A1A1.</p>}
            >
                <TextField id="postal-code-field" style={{ paddingLeft: '5px' }} 
                    variant="outlined" name='postalCode'
                    value={stepData2.postalCode.value} onChange={handleChange}>
                </TextField>
            </FormField>
            </div>
       
    );
};
export default Step2;

