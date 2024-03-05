import Image from 'next/image';
import { FormField } from './FormField';
import TextField from '@mui/material/TextField';
import { Typography, } from '@mui/material';
import React, { useState, } from 'react';
import { isProhibitionNumberValid } from "../_nonRoutingAssets/lib/util";

interface Props {
    onProhibitionDataChange: (data: { 
        controlProhibitionNumber: string; 
        controlIsUl: boolean; 
        controlIsIrp: boolean; 
        controlIsAdp: boolean; 
        prohibitionNumberClean: string;
        validProhibitionNumber: boolean;
    }) => void;
}


const ProhibitionNumber: React.FC<Props> = ({ onProhibitionDataChange }) => {
    const [controlProhibitionNumber, setControlProhibitionNumber] = useState('');
    const [controlIsUl, setControlIsUl] = useState(false);
    const [controlIsIrp, setControlIsIrp] = useState(false);
    const [controlIsAdp, setControlIsAdp] = useState(false);
    const [prohibitionNumberClean, setProhibitionNumberClean] = useState('');    

    const [validProhibitionNumber, setValidProhibitionNumber] = useState(false);
    const [prohibitionNumberErrorText, setProhibitionNumberErrorText] = useState('');

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setControlProhibitionNumber(value);
    }

    const validateField = () => {      
        let isProhNumberValid = false;  
        if (isProhibitionNumberValid(controlProhibitionNumber)) {
            isProhNumberValid = true;
            setControlIsUl(controlProhibitionNumber.startsWith('30'));
            setControlIsIrp((controlProhibitionNumber.startsWith('21') || controlProhibitionNumber.startsWith('40')));
            setControlIsAdp(controlProhibitionNumber.startsWith('00'));
            setProhibitionNumberClean(controlProhibitionNumber.replace('-', ''));
        } else {
            setProhibitionNumberErrorText(controlProhibitionNumber ? "Enter first 8 numbers with the dash. Don't enter the digit in the grey box. Prohibition numbers start with 00, 21, 30 or 40." : "Enter prohibition number found on the notice.");
            setControlIsUl(false);
            setControlIsIrp(false);
            setControlIsAdp(false);
            setProhibitionNumberClean('');
        }
        console.log("validateField: ", controlProhibitionNumber, isProhNumberValid);
        setValidProhibitionNumber(isProhNumberValid);
        onProhibitionDataChange({
            controlProhibitionNumber: controlProhibitionNumber,
            controlIsUl: controlIsUl,
            controlIsIrp: controlIsIrp,
            controlIsAdp: controlIsAdp,
            prohibitionNumberClean: prohibitionNumberClean,
            validProhibitionNumber: isProhNumberValid
        });
    }; 

    return (
        <div>
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
                    <TextField key="key1" id="control-prohibition-number-field"  style={{ paddingLeft: '5px' }}
                        variant="outlined"
                        value={controlProhibitionNumber} onChange={handleChange} onBlur={validateField}>
                    </TextField></FormField>
                <div style={{ marginTop: '-30px', marginBottom: '30px' }}>
                    <Typography sx={{ color: '#313132', fontSize: '16px', fontWeight: '700', mt: '10px', ml: '10px', paddingBottom: '10px' }}>(optional)</Typography>

                    <Image src="/./././assets/images/Combo prohibition no.png" width={280}
                        height={180}
                        alt="Info" style={{ marginLeft: "10px", marginBottom: '20px', height: 'auto', width: 'auto' }}
                    />
                </div>
        </div>
    )
}
export default ProhibitionNumber;