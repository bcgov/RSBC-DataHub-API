'use client'

import { Button, FormControl, FormControlLabel, FormLabel, Grid, Radio, RadioGroup, TextField, Typography } from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';
import { useEffect, useState } from "react";
import ProhibitionNumber from '../components/ProhibitionNumber';
import { ArrowForward } from "@mui/icons-material";
import { AvailableReviewDates } from "../interfaces";
import { getAvailableReviewDates } from "./actions";


export default function Page() {
    const [driverLastName, setDriverLastName] = useState('');
    const [stepData, setStepData] = useState({ controlProhibitionNumber: '', validProhibitionNumber: false });
    const [requestAvailDates, setRequestAvailDates] = useState(false);
    const [reviewDates, setReviewDates] = useState<AvailableReviewDates[]>([]);
    const [selectedReviewDate, setSelectedReviewDate] = useState('');

    useEffect(() => {
        getAvailableReviewDates().then(([dates]) => {
            setReviewDates(dates);
        });
    }, []);

    const handleProhibitionNumberChange = (data: { controlProhibitionNumber: string, validProhibitionNumber: boolean }) => {
        setStepData({
            controlProhibitionNumber: data.controlProhibitionNumber,
            validProhibitionNumber: data.validProhibitionNumber
        });
        console.log("handleProhibitionNumberChange: ", data.controlProhibitionNumber,
            data.validProhibitionNumber);

    };

    const submitData = () => {
        console.log(stepData);
        console.log(driverLastName);
        console.log(selectedReviewDate);
    }

    return (
        <>
            <h1>Form 2 </h1>
            <Grid container spacing={2} >
                <Grid item xs={8} sx={{ padding: "1px" }}>
                    <div style={{ display: 'grid', marginTop: '20px' }}>
                        <div style={{ marginTop: '-30px', marginBottom: '30px' }}>
                            <Typography sx={{ color: '#313132', fontSize: '16px', fontWeight: '700', mt: '10px', ml: '10px', paddingBottom: '10px' }}>
                                (optional)</Typography>
                            <ProhibitionNumber onProhibitionDataChange={handleProhibitionNumberChange} ></ProhibitionNumber>
                        </div>
                    </div>
                </Grid>
                <Grid item xs={8} sx={{ padding: "1px" }}>
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
                    {stepData.validProhibitionNumber &&
                        <Button onClick={e => {
                            console.log("Event: ", ProhibitionNumber, driverLastName);
                            setRequestAvailDates(true);
                        }}
                            variant="contained"
                            sx={{ borderColor: '#003366', backgroundColor: '#003366', color: 'white', marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }}
                            startIcon={<ArrowForward sx={{ fontWeight: 'bold' }} />}>
                            Search for a review date
                        </Button>}
                    {!stepData.validProhibitionNumber &&
                        <Button disabled
                            sx={{ marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }}
                            startIcon={<ArrowForward sx={{ fontWeight: 'bold' }} />}>
                            Search for a review date
                        </Button>}

                </Grid>
                {stepData.validProhibitionNumber && requestAvailDates &&
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
                    <Button variant="outlined" sx={{ cursor: 'pointer', color: '#003366', borderColor: '#003366', marginRight: '20px', fontWeight: '700', fontSize: '16px', minWidth: '9.5em' }}
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