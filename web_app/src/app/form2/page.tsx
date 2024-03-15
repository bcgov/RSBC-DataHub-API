'use client'

import Image from 'next/image';
import { Button, FormControl, FormControlLabel, FormLabel, Grid, Radio, RadioGroup, TextField, Typography } from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';
import { useEffect, useState } from "react";
import { ArrowForward } from "@mui/icons-material";
import { AvailableReviewDates } from "../interfaces";
import { getAvailableReviewDates, postReviewDate } from "./actions";
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
    const [driverLastNameErrorText, setDriverLastNameErrorText] = useState('Required');
    const [validDriverLastName, setValidDriverLastName] = useState(true);


    useEffect(() => {
        if (validProhibitionNumber)
            getAvailableReviewDates(controlProhibitionNumber, driverLastName).then(([dates, error]) => {
                setReviewDates(dates);
                console.log('error: ', error, controlProhibitionNumber);
            });
    }, [controlProhibitionNumber, validProhibitionNumber]);

    const validateProhibitionNumber = () => {
        if (isProhibitionNumberValid(controlProhibitionNumber)) {
            setValidProhibitionNumber(true);
        } else {
            setValidProhibitionNumber(false);
            setProhibitionNumberErrorText(controlProhibitionNumber ? "Enter first 8 numbers with the dash. Don't enter the digit in the grey box. Prohibition numbers start with 00, 21, 30 or 40." : "Enter prohibition number found on the notice.");
        }
    };


    const submitData = () => {
        console.log(controlProhibitionNumber);
        console.log(driverLastName);
        console.log(selectedReviewDate);
        postReviewDate(controlProhibitionNumber, selectedReviewDate, driverLastName);
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
            <div id="formContent" >
                <div id="page1img1">
                    <h1 className="header1" id="hed">Schedule a Driving Prohibition Review</h1>
                    <div style={{ fontSize: "16px", fontFamily: "'BC Sans', 'Noto Sans',  Arial, sans-serif", paddingLeft: '10px', lineHeight: '2.5' }}>
                        <p>When you see this symbol <Image
                            src="/./././assets/icons/info-icon.png"
                            width={15}
                            height={15}
                            alt="Info" />
                            &nbsp;click it for more information.
                        </p>
                        <p><strong>You must have paid the application review fee at <a href="https://pay.gov.bc.ca/" target="_blank" rel="noopener noreferrer">PayBC</a> before you can schedule.</strong></p>
                        <p>You&apos;ll receive <strong> 2 emails</strong> when you submit the form:</p>
                        <ol style={{ paddingLeft: '30px', lineHeight: '1.5' }}>
                            <li>A confirmation of the date and time of your review, and </li>
                            <li>The next step in the application process.</li>
                        </ol>
                        <p>If you don&apos;t enter anything in the form for 15 minutes, it may time out.</p> </div>
                </div>
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
                                value={controlProhibitionNumber} onChange={e => { setControlProhibitionNumber(e.target.value) }} onBlur={validateProhibitionNumber}>
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
                        </Typography>
                        <FormField
                            id="driver-lastname-number"
                            labelText="Driver's last name"
                            placeholder="Enter driver's last name."
                            tooltipTitle="Driver's last name"
                            error={!validDriverLastName}
                            errorText={driverLastNameErrorText}
                            tooltipContent={<p>Enter the last name on your driver&apos;s prohibition number form.</p>}
                        >
                            <TextField key="key2"
                                id="driverLastNameId"
                                style={{ paddingLeft: '5px' }}
                                variant="outlined"
                                value={driverLastName}
                                onChange={e => {
                                    setDriverLastName(e.currentTarget.value);
                                    if (driverLastName) {
                                        setValidDriverLastName(true);
                                        //setDriverLastNameErrorText('');
                                    }
                                }}
                                onBlur={e=> {
                                    if (!driverLastName) {
                                        setValidDriverLastName(false);
                                        //setDriverLastNameErrorText('Required');
                                    } else {
                                        setValidDriverLastName(true);
                                    }
                                }}
                                >
                            </TextField>
                        </FormField>
                    </Grid>
                    <Grid item xs={8} sx={{ padding: "1px" }}>
                        {validProhibitionNumber && validDriverLastName &&
                            <Button onClick={e => {
                                setRequestAvailDates(true);
                            }}
                                variant="contained"
                                sx={{ borderColor: '#003366', backgroundColor: '#003366', color: 'white', marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }}
                                startIcon={<ArrowForward sx={{ fontWeight: 'bold' }} />}>
                                Search for a review date
                            </Button>}
                        {(!validProhibitionNumber || !validDriverLastName) &&
                            <Button disabled
                                sx={{ marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }}
                                startIcon={<ArrowForward sx={{ fontWeight: 'bold' }} />}>
                                Search for a review date
                            </Button>}

                    </Grid>
                    {validProhibitionNumber && validDriverLastName && requestAvailDates &&
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
            </div>
        </>
    );
}