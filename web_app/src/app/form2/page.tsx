'use client'

import Image from 'next/image';
import { Button, FormControl, FormControlLabel, FormLabel, Grid, Radio, RadioGroup, TextField, Typography } from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';
import { useEffect, useState } from "react";
import { ArrowForward } from "@mui/icons-material";
import { AvailableReviewDates } from "../interfaces";
import { getAvailableReviewDates } from "./actions";
import React from "react";
import { FormField } from "../components/FormField";
import { isProhibitionNumberValid } from '../_nonRoutingAssets/lib/util';


export default function Page() {
    const [driverLastName, setDriverLastName] = useState('');
    const [controlProhibitionNumber, setControlProhibitionNumber] = useState('');
    const [requestAvailDates, setRequestAvailDates] = useState(false);
    const [reviewDates, setReviewDates] = useState<AvailableReviewDates[]>([]);
    const [selectedReviewDate, setSelectedReviewDate] = useState('');
    const [validProhibitionNumber, setValidProhibitionNumber] = useState(false);
    const [prohibitionNumberErrorText, setProhibitionNumberErrorText] = useState('');

    useEffect(() => {
        if (validProhibitionNumber)
            getAvailableReviewDates(controlProhibitionNumber, driverLastName).then(([dates, error]) => {
                setReviewDates(dates);
                console.log('error: ', error, controlProhibitionNumber);
            });
    }, [controlProhibitionNumber, validProhibitionNumber]);

    const validateField = () => {
        if (isProhibitionNumberValid(controlProhibitionNumber)) {
            setValidProhibitionNumber(true);
        } else {
            setValidProhibitionNumber(false);
            setProhibitionNumberErrorText(controlProhibitionNumber ? "Enter first 8 numbers with the dash. Don't enter the digit in the grey box. Prohibition numbers start with 00, 21, 30 or 40." : "Enter prohibition number found on the notice.");
        }
        console.log("handleProhibitionNumberChange: ", controlProhibitionNumber,
            validProhibitionNumber);

    };

    const submitData = () => {
        console.log(controlProhibitionNumber);
        console.log(driverLastName);
        console.log(selectedReviewDate);

    }

    const clearData = () => {
        setControlProhibitionNumber('')
        setRequestAvailDates(false);
        setDriverLastName('');
        setReviewDates([]);
        setSelectedReviewDate('');
        setProhibitionNumberErrorText('');
        setValidProhibitionNumber(false);
    }

    return (
        <>
            <h1>Form 2 </h1>
            <Grid container spacing={2} >
                <Grid item xs={8} sx={{ padding: "1px" }}>
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
                            value={controlProhibitionNumber} onChange={e => { setControlProhibitionNumber(e.target.value) }} onBlur={validateField}>
                        </TextField></FormField>
                    <div style={{ marginTop: '-30px', marginBottom: '30px' }}>
                        <Typography sx={{ color: '#313132', fontSize: '16px', fontWeight: '700', mt: '10px', ml: '10px', paddingBottom: '10px' }}>(optional)</Typography>

                        <Image src="/./././assets/images/Combo prohibition no.png" width={280}
                            height={180}
                            alt="Info" style={{ marginLeft: "10px", marginBottom: '1px', height: 'auto', width: 'auto' }}
                        />
                    </div>
                </Grid>
                <Grid item xs={8} sx={{ padding: "1px" }}>
                    <Typography sx={{ color: '#313132', fontSize: '16px', fontWeight: '700', mt: '10px', ml: '10px', paddingBottom: '10px' }}>
                        Last Name</Typography>
                    <TextField key="key2"
                        id="driverLastNameId"
                        style={{ paddingLeft: '5px' }}
                        variant="outlined"
                        value={driverLastName}
                        onChange={e => {
                            setDriverLastName(e.target.value);
                        }}>
                    </TextField>
                </Grid>
                <Grid item xs={8} sx={{ padding: "1px" }}>
                    {validProhibitionNumber &&
                        <Button onClick={e => {
                            setRequestAvailDates(true);
                        }}
                            variant="contained"
                            sx={{ borderColor: '#003366', backgroundColor: '#003366', color: 'white', marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }}
                            startIcon={<ArrowForward sx={{ fontWeight: 'bold' }} />}>
                            Search for a review date
                        </Button>}
                    {!validProhibitionNumber &&
                        <Button disabled
                            sx={{ marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }}
                            startIcon={<ArrowForward sx={{ fontWeight: 'bold' }} />}>
                            Search for a review date
                        </Button>}

                </Grid>
                {validProhibitionNumber && requestAvailDates &&
                    <Grid item xs={8} sx={{ padding: "1px" }}>
                        <div className="formContent">
                            <FormControl>
                                <FormLabel id="demo-radio-buttons-group-label">
                                    Select a review date:
                                    <p>(Do not refresh this page. It will not give you more dates.)</p>
                                    <p>(optional)</p>
                                </FormLabel>
                                <RadioGroup name="select-available-review-dates" defaultValue={''} >
                                    {reviewDates.map((date) => (
                                        <FormControlLabel key={date.value} value={date.value} label={date.label} control={<Radio sx={{
                                            '&.Mui-checked': { color: 'rgb(49,49,50)', },
                                        }} />}
                                            onChange={e => { setSelectedReviewDate(date.value) }} />
                                    ))}
                                </RadioGroup>
                            </FormControl>
                        </div>
                    </Grid>

                }
                <Grid item xs={8} sx={{ padding: "1px" }}></Grid>

                <Grid item xs={6} sx={{ padding: "1px" }}>
                    <Button onClick={clearData} variant="outlined" sx={{ cursor: 'pointer', color: '#003366', borderColor: '#003366', marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }}
                        startIcon={<CloseIcon sx={{ fontWeight: 'bold' }} />}>
                        Clear
                    </Button>
                    <Button onClick={submitData} variant="contained" sx={{ borderColor: '#003366', backgroundColor: '#003366', color: 'white', marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }} startIcon={<ArrowForward sx={{ fontWeight: 'bold' }} />}>
                        Send
                    </Button>
                </Grid>

                <Grid item xs={8} sx={{ padding: "1px" }}></Grid>
            </Grid >
        </>
    );
}