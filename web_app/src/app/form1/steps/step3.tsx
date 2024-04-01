/* eslint-disable react/display-name */
import React, { useState, forwardRef, useImperativeHandle } from 'react';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import { Step3InputProps, Step3Data } from '../../interfaces';
import { Checkbox, TextField, RadioGroup, Radio, Grid } from '@mui/material';
import { FormField } from '../../components/FormField';

const Step3 = forwardRef((props: Step3InputProps, ref) => {

    const [step3Data, setStep3Data] = useState<Step3Data>({
        ulGrounds: [],
        irpGroundsList:[],
        adpGroundsAlcohol:[],
        adpGroundsDrugs:[],
        adpGroundsAlcoholDrugs:[],
        adpGroundsDrugExpert:[],
        adpGroundsRefusal: [],
        control6: 0,
        hearingRequest:'',
        hasError: false,
    });

    useImperativeHandle(ref, () => ({
        clearData() {
            setStep3Data({
                ulGrounds: [],
                irpGroundsList: [],
                adpGroundsAlcohol: [],
                adpGroundsDrugs: [],
                adpGroundsAlcoholDrugs: [],
                adpGroundsDrugExpert: [],
                adpGroundsRefusal: [],
                control6: 0,
                hearingRequest: '',
                hasError: false,
            });
        }
    }));

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        const checked = e.target.checked;
        const name = e.target.name;

        const val = Number(value);

        if (name === 'ulGrounds')
            checked ? step3Data.ulGrounds.push(val) : step3Data.ulGrounds.splice(step3Data.ulGrounds.indexOf(val), 1);
        else if (name === 'irpGrounds')
            checked ? step3Data.irpGroundsList.push(val) : step3Data.irpGroundsList.splice(step3Data.irpGroundsList.indexOf(val), 1);
        else {
            setAdpGrounds(name, val, checked);              
        }        
                
        props.step3DatatoSend(step3Data);
    }

    const setAdpGrounds = (name: string, val: number, checked: boolean) => {
        if (name === 'adpGroundsAlcohol')
            checked ? step3Data.adpGroundsAlcohol.push(val) : step3Data.adpGroundsAlcohol.splice(step3Data.adpGroundsAlcohol.indexOf(val), 1);
        else if (name === 'adpGroundsDrugs')
            checked ? step3Data.adpGroundsDrugs.push(val) : step3Data.adpGroundsDrugs.splice(step3Data.adpGroundsDrugs.indexOf(val), 1);
        else if (name === 'adpGroundsAlcoholDrugs')
            checked ? step3Data.adpGroundsAlcoholDrugs.push(val) : step3Data.adpGroundsAlcoholDrugs.splice(step3Data.adpGroundsAlcoholDrugs.indexOf(val), 1);
        else if (name === 'adpGroundsDrugExpert')
            checked ? step3Data.adpGroundsDrugExpert.push(val) : step3Data.adpGroundsDrugExpert.splice(step3Data.adpGroundsDrugExpert.indexOf(val), 1);
        else if (name === 'adpGroundsRefusal')
            checked ? step3Data.adpGroundsRefusal.push(val) : step3Data.adpGroundsRefusal.splice(step3Data.adpGroundsRefusal.indexOf(val), 1);
        setStep3Data({
            ...step3Data, control6: step3Data.adpGroundsAlcohol.length +
                step3Data.adpGroundsDrugs.length +
                step3Data.adpGroundsAlcoholDrugs.length +
                step3Data.adpGroundsDrugExpert.length +
                step3Data.adpGroundsRefusal.length
        });
    }

       

    const hearingRequestChanged = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setStep3Data({
            ...step3Data,
            hearingRequest: value,
        });      
        props.step3DatatoSend(step3Data);
    };

    const PrepareForeReview = () => {
        return (
            <Grid item xs={8} sx={{ padding: "1px" }}>
                <div className="step3Div" id="prepareForReviewUl">
                    <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>Preparing for your review:</span></strong></div>
                    <ul style={{ marginLeft: '20px' }}>
                        <li>Before your review, we&apos;ll send you the police evidence.</li>
                        <li>You can use the evidence to prepare for your review.</li>
                        <li>The adjudicator will use it with the information you submit to make a decision about your prohibition.</li>
                        <li>A lawyer may represent you in your review.&nbsp;</li>
                        <li>Review decisions are sent by regular mail.</li>
                    </ul>
                </div>
            </Grid> 
        )
    }

    return (
        <div className="step3Div" style={{ display: 'grid', marginTop: '20px',marginRight:'150px',  pointerEvents: (props.isEnabled ? '' : 'none') as React.CSSProperties["pointerEvents"], }} >      
            <Grid item xs={12}  md={8} sm={10} lg={12} sx={{ padding: "1px" }}>
            <div className="step3Div"  id="ulControlBlock">
                    {props.controlIsUl &&
                    <div id="ul-step3">
                        <div className="step3Div" id="ul-burden-of-proof-text">
                        <span style={{ marginBottom: '20px', }}>This review is available if you have been served with a Notice of Prohibition under <a href="https://www.bclaws.ca/civix/document/id/complete/statreg/96318_12" rel="noopener" target="_blank">s.251(1)</a> of the Motor Vehicle Act, and are prohibited from driving under <a href="https://www.bclaws.ca/civix/document/id/complete/statreg/96318_12" rel="noopener" target="_blank">s.251(4)</a>. This driving prohibition will be terminated without a review if ICBC issues you a BC driver&apos;s licence.
                        </span>
                        <span style={{ marginBottom: '20px', }}>The information you&apos;ll provide should address the grounds you choose below. Hardship is not a consideration in a review.</span>
                        <span style={{ marginBottom: '20px', }}>These are the only grounds for review under <a href="https://www.bclaws.ca/civix/document/id/complete/statreg/96318_12" rel="noopener" target="_blank">s.261</a> of the Motor Vehicle Act. They have been simplified for readability.</span>
                        <span style={{ marginBottom: '20px', }}>You must select at least 1 ground:</span>
                        </div>
                     <div className="step3Div"  id="ul-grounds-block">
                            <FormGroup className="step3Div" id="ul-grounds" >
                                <FormControlLabel control={<Checkbox value={0} onChange={handleChange} name="ulGrounds" />} label="I am exempt from the requirement to hold a BC driver's licence." />
                                <FormControlLabel control={<Checkbox value={1} onChange={handleChange} name="ulGrounds" />} label="I have become exempt from the requirement to hold a BC driver's licence since the notice of prohibition was served." />
                                <FormControlLabel control={<Checkbox value={2} onChange={handleChange} name="ulGrounds" />} label="My driving record should not have identified me as an unlicensed driver. " />                           
                        </FormGroup>
                            </div>
                           <PrepareForeReview />
                            <div className="step3Div" id="additionalInfoUl">
                                <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>Additional Information:</span></strong></div>
                                <ul>
                                    <li>If you are claiming that you are exempt from the requirement to hold a BC driver&apos;s licence, you will need to submit evidence that supports your application.</li>
                                    <li>If you believe that you should not have been identified as an unlicensed driver, you will need to explain why you held that belief.</li>
                                    <li>The adjudicator will also consider your driving record in the review; you can <a href="https://www.icbc.com/driver-licensing/getting-licensed/Pages/Your-driving-record.aspx" rel="noopener" target="_blank">get a copy from ICBC</a>.</li>
                                </ul>
                            </div>
                            <div className="step3Div" id="writtenReviewInfoUl">
                                <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>Written Review Information:</span></strong></div>
                                <ul>
                                    <li>You can provide a written statement and evidence that address the grounds you selected in this application.</li>
                                    <li>In a written review you won&apos;t be able to talk to the adjudicator.</li>
                                </ul>
                            </div>
                    </div>
                    }
                    </div>
                    <div className="step3Div" id="irpControlBlock">
                        {props.controlIsIrp &&
                            <div id="irp-step3">
                        <div className="step3Div" id="irp-burden-of-proof-text">
                        <span>The information you will provide should address the grounds you choose below. The burden of proof is on the applicant in a review. Hardship is not a consideration in a review.</span>
                        <span>These are the only grounds for review under <a href="https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/96318_07">s.215.5</a> of the Motor Vehicle Act. They have been simplified for readability.</span>
                        <span>You must select at least 1 ground:</span>
                            </div>
                    <div className="step3Div"  id="dataInfoIrp">
                                <FormGroup className="step3Div" id="irp-grounds" >
                                <FormControlLabel control={<Checkbox onChange={handleChange} value={0} name="irpGrounds" />} label="I was not the driver or in care or control of the motor vehicle." />
                                <FormControlLabel control={<Checkbox onChange={handleChange} value={1} name="irpGrounds" />} label="I was not advised of my right to a second breath test on an approved screening device." />
                                <FormControlLabel control={<Checkbox onChange={handleChange} value={2} name="irpGrounds" />} label="I requested a second test but the officer did not perform it." />
                                <FormControlLabel control={<Checkbox onChange={handleChange} value={3} name="irpGrounds" />} label="My second test was not performed on a different approved screening device." />
                                <FormControlLabel control={<Checkbox onChange={handleChange} value={4} name="irpGrounds" />} label="The prohibition was not served based on the lower approved screening device result." />
                                <FormControlLabel control={<Checkbox onChange={handleChange} value={5} name="irpGrounds" />} label="The result of the approved screening device is not reliable." />
                                <FormControlLabel control={<Checkbox onChange={handleChange} value={6} name="irpGrounds" />} label="The approved screening device that was the basis for my prohibition did not register a warn." />
                                <FormControlLabel control={<Checkbox onChange={handleChange} value={7} name="irpGrounds" />} label="The approved screening device registered a warn, but my blood alcohol content was less than 0.05 (50 milligrams of alcohol in 100 millilitres of blood)." />
                                <FormControlLabel control={<Checkbox onChange={handleChange} value={8} name="irpGrounds" />} label="The approved screening device that was the basis for my prohibition did not register a fail." />
                                <FormControlLabel control={<Checkbox onChange={handleChange} value={9} name="irpGrounds" />} label="The approved screening device registered a fail, but my blood alcohol content was less than 0.08 (80 milligrams of alcohol in 100 millilitres of blood)." />
                                <FormControlLabel control={<Checkbox onChange={handleChange} value={10} name="irpGrounds" />} label="My 7-day or 30-day prohibition should be reduced because I did not have the prescribed number of prior warn range prohibitions." />
                                <FormControlLabel control={<Checkbox onChange={handleChange} value={11} name="irpGrounds" />} label="I did not refuse or fail to comply with a demand for a breath sample." />
                                <FormControlLabel control={<Checkbox onChange={handleChange} value={12} name="irpGrounds" />} label="I had a reasonable excuse for refusing or failing to comply with a demand." />
                        </FormGroup>
                            </div>
                            <PrepareForeReview />

                    </div>
                }
                </div>
                <div className="step3Div" id="adpControlBlock">
                    {props.controlIsAdp &&
                        <div id="adp-step3">
                        <div className="step3Div" id="adp-burden-of-proof-text">
                        <span>The information you will provide should address the grounds you choose below. The burden of proof is on the applicant in a review. Hardship is not a consideration in a review.</span>
                        <span>These are the only grounds for review under <a href="https://www.bclaws.ca/civix/document/id/complete/statreg/96318_02#section94.6" rel="noopener" target="_blank">s.94.6</a> of the Motor Vehicle Act. They have been simplified for readability.</span>
                        <span>Check grounds for the type of ADP that was served on you. You must select at least 1 ground:</span>
                            </div>
                            <div className="step3Div" id="dataInfoAdp">
                                <div id='page5img1'>
                                <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>SECTION 94.1(1)(a) - Blood Alcohol Concentration</span></strong></div>
                                <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>(optional)</span></strong></div>
                                <FormGroup className="step3Div" id="adp-grounds-alochol">
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={0} name="adpGroundsAlcohol" />} label="I did not operate a motor vehicle." />
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={1} name="adpGroundsAlcohol" />} label="I did not have, within 2 hours after ceasing to operate a motor vehicle, a blood alcohol concentration equal to or exceeding 80 milligrams (mg) of alcohol in 100 millilitres (mL) of blood." />
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={2} name="adpGroundsAlcohol" />} label="All of the following apply: " />
                                    <ul>
                                        <li>I consumed alcohol after ceasing to operate the motor vehicle;</li>
                                        <li>After ceasing to operate the motor vehicle, I had no reasonable expectation that I would be required to provide a sample of breath or blood;&nbsp;<strong>and</strong></li>
                                        <li>My alcohol consumption was consistent with my blood alcohol concentration as determined by the analysis of my breath or blood and with my having had, at the time when I was operating the motor vehicle, a blood alcohol concentration that was less than 80 mg of alcohol in 100 mL of blood.</li>
                                    </ul>
                                </FormGroup>
                                <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>SECTION 94.1(1)(a.1) - Blood Drug Concentration</span></strong></div>
                                <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>(optional)</span></strong></div>
                                <FormGroup className="step3Div" id="adp-grounds-drugs">
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={0} name="adpGroundsDrugs" />} label="I did not operate a motor vehicle." />
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={1} name="adpGroundsDrugs" />} label="I did not have, within 2 hours after ceasing to operate a motor vehicle, a blood drug concentration equal to or exceeding the blood drug concentration for the drug that is prescribed for this section." />
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={2} name="adpGroundsDrugs" />} label="Both of the following apply: " />
                                    <ul>
                                        <li>I consumed the drug after ceasing to operate the motor vehicle; <strong>and</strong></li>
                                        <li>After ceasing to operate the motor vehicle, I had no reasonable expectation that I would be required to provide a sample of blood.</li>
                                    </ul>
                                </FormGroup>
                                <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>SECTION 94.1(1)(a.2) - Blood Alcohol and Drug Concentration</span></strong></div>
                                <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>(optional)</span></strong></div>
                                <FormGroup className="step3Div" id="adp-grounds-alcohol-and-drugs">
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={0} name="adpGroundsAlcoholDrugs" />} label="I did not operate a motor vehicle." />
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={1} name="adpGroundsAlcoholDrugs" />} label="I did not have, within 2 hours after ceasing to operate a motor vehicle, a blood drug concentration and a blood alcohol concentration equal to or exceeding the amounts prescribed for this section." />
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={2} name="adpGroundsAlcoholDrugs" />} label="All of the following apply: " />
                                    <ul>
                                        <li>I consumed alcohol or the drug, or both, after ceasing to operate the motor vehicle;</li>
                                        <li>After ceasing to operate the motor vehicle, I had no reasonable expectation that I would be required to provide a sample of breath or blood, or both; <strong>and</strong></li>
                                        <li>My alcohol consumption was consistent with my blood alcohol concentration as determined by the analysis of my breath or blood and with my having had, at the time when I was operating the motor vehicle, a blood alcohol concentration that was less than the blood alcohol concentration that is prescribed for the purposes of this section.</li>
                                    </ul>
                                    </FormGroup>
                                </div>
                                <div id='page5img2'>
                                <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>SECTION 94.1(1)(a.3) - Drug Recognition Expert Evaluation</span></strong></div>
                                <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>(optional)</span></strong></div>
                                <FormGroup className="step3Div" id="adp-grounds-drug-expert">
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={0} name="adpGroundsDrugExpert" />} label="I did not operate a motor vehicle." />
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={1} name="adpGroundsDrugExpert" />} label="My evaluation was not conducted by an evaluating officer." />
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={2} name="adpGroundsDrugExpert" />} label="The evaluating officer did not comply with the requirements that are prescribed for the purposes of this section." />
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={3} name="adpGroundsDrugExpert" />} label="The analysis of my bodily substance did not confirm the presence in my body of one or more of the types of drugs identified by the evaluating officer as impairing my ability to operate a motor vehicle." />
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={4} name="adpGroundsDrugExpert" />} label={<span><span>My ability to operate a motor vehicle was not impaired to any degree by a drug or by a combination of alcohol and a drug at the time of the evaluation, </span><strong>and</strong> <span>the results of the evaluation were due to a medical condition.</span></span>} />
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={5} name="adpGroundsDrugExpert" />} label="Both of the following apply:" />
                                    <ul>
                                        <li>I consumed one or more of the types of drugs identified by the evaluating officer as impairing my ability to operate a motor vehicle after ceasing to operate the motor vehicle; <strong>and</strong></li>
                                        <li>After ceasing to operate the motor vehicle, I had no reasonable expectation that I would be required to provide a sample of a bodily substance.</li>
                                    </ul>
                                </FormGroup>
                                <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>SECTION 94.1(1)(b) - Refusal or Failure to Comply</span></strong></div>
                                <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>(optional)</span></strong></div>
                                <FormGroup className="step3Div" id="adp-grounds-refusal">
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={0} name="adpGroundsRefusal" />} label="I did not operate a motor vehicle." />
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={1} name="adpGroundsRefusal" />} label={<span><span>I did not refuse or fail to comply with a demand made under <a href="https://laws-lois.justice.gc.ca/eng/acts/c-46/page-71.html#docCont" rel="noopener" target="_blank">s.320.27</a> or <a href="https://laws-lois.justice.gc.ca/eng/acts/c-46/page-71.html#docCont" rel="noopener" target="_blank">s.320.28</a> of the Criminal Code.</span></span>} />
                                        <FormControlLabel control={<Checkbox onChange={handleChange} value={2} name="adpGroundsRefusal" />} label={<span>I had a reasonable excuse for refusing to comply with the demand made under <a href="https://laws-lois.justice.gc.ca/eng/acts/c-46/page-71.html#docCont" rel="noopener" target="_blank">s.320.27</a> or <a href="https://laws-lois.justice.gc.ca/eng/acts/c-46/page-71.html#docCont" rel="noopener" target="_blank">s.320.28</a> of the Criminal Code.</span>} />

                                </FormGroup>
                                {(step3Data.control6 === 0) &&
                                    <div className="step3Div" >
                                        <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>Grounds checked</span></strong></div>
                                        <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>(optional)</span></strong></div>
                                        <TextField id="grounds-checked-field" style={{ paddingLeft: '5px' }}
                                            variant="outlined" name='groundsChecked' disabled>
                                        </TextField>
                                    </div>
                                }

                            </div>
                                <PrepareForeReview />
                            </div>
                            <div id='page6img1'>
                            <FormField
                                id="review-type"
                                labelText="Please select a review type:"
                                tooltipTitle="Please select a review type:"
                                tooltipContent={<span>In a written review you won&apos;t be able to talk to the adjudicator. Oral reviews are 30 minutes long and conducted by phone only.</span>}
                            >
                                <RadioGroup id="review-type"
                                    aria-labelledby="demo-radio-buttons-group-label"
                                    name="hearingRequest" value={step3Data.hearingRequest} onChange={hearingRequestChanged}
                                >
                                    <FormControlLabel value="written" control={<Radio sx={{
                                        '&.Mui-checked': {
                                            color: 'rgb(49,49,50)',
                                        },
                                    }} />} label="Written review ($100)" />
                                    <FormControlLabel value="oral" control={<Radio sx={{
                                        '&.Mui-checked': {
                                            color: 'rgb(49,49,50)',
                                        },
                                    }} />} label="Oral review ($200)" />
                                </RadioGroup>
                                </FormField>
                            </div>
                    </div>
                }
                </div>
            </Grid>    
           
            
           
        </div>
    );
});
export default Step3;

