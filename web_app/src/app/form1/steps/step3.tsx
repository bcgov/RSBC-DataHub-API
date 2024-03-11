import React from 'react';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import { Step3InputProps } from '../../interfaces';
import { Checkbox, TextField, RadioGroup, Radio, Grid } from '@mui/material';
import { FormField } from '../../components/FormField';

const Step3: React.FC<Step3InputProps> = ({ controlIsUl, controlIsIrp, controlIsAdp, licenseSeized, step3DatatoSend }) => {  

    return (
        <div className="step3Div" style={{ display: 'grid', marginTop: '20px', pointerEvents: (licenseSeized ? '' : 'none') as React.CSSProperties["pointerEvents"], }}>      
            <Grid item xs={4} sx={{ padding: "1px" }}>
            <div className="step3Div"  id="reviewInfo">
                {controlIsUl &&
                        <div className="step3Div" id="ul-burden-of-proof-text">
                        <p style={{ marginBottom: '20px', }}>This review is available if you have been served with a Notice of Prohibition under <a href="https://www.bclaws.ca/civix/document/id/complete/statreg/96318_12" rel="noopener" target="_blank">s.251(1)</a> of the Motor Vehicle Act, and are prohibited from driving under <a href="https://www.bclaws.ca/civix/document/id/complete/statreg/96318_12" rel="noopener" target="_blank">s.251(4)</a>. This driving prohibition will be terminated without a review if ICBC issues you a BC driver&apos;s licence.
                        </p>
                        <p style={{ marginBottom: '20px', }}>The information you&apos;ll provide should address the grounds you choose below. Hardship is not a consideration in a review.</p>
                        <p style={{ marginBottom: '20px', }}>These are the only grounds for review under <a href="https://www.bclaws.ca/civix/document/id/complete/statreg/96318_12" rel="noopener" target="_blank">s.261</a> of the Motor Vehicle Act. They have been simplified for readability.</p>
                        <p style={{ marginBottom: '20px', }}>You must select at least 1 ground:</p>
                    </div>
                }
                {controlIsIrp &&
                        <div className="step3Div" id="irp-burden-of-proof-text">
                        <p>The information you will provide should address the grounds you choose below. The burden of proof is on the applicant in a review. Hardship is not a consideration in a review.</p>
                        <p>These are the only grounds for review under <a href="https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/96318_07">s.215.5</a> of the Motor Vehicle Act. They have been simplified for readability.</p>
                        <p>You must select at least 1 ground:</p>
                    </div>
                }
                {controlIsAdp &&
                        <div className="step3Div" id="adp-burden-of-proof-text ">
                        <p>The information you will provide should address the grounds you choose below. The burden of proof is on the applicant in a review. Hardship is not a consideration in a review.</p>
                        <p>These are the only grounds for review under <a href="https://www.bclaws.ca/civix/document/id/complete/statreg/96318_02#section94.6" rel="noopener" target="_blank">s.94.6</a> of the Motor Vehicle Act. They have been simplified for readability.</p>
                        <p>Check grounds for the type of ADP that was served on you. You must select at least 1 ground:</p>
                    </div>
                }
                </div>
            </Grid>
            <Grid item xs={8} sx={{ padding: "1px" }}>
            <div className="step3Div"  id="dataInfo">
                {controlIsUl &&
                    <div className="step3Div"  id="ul-grounds-block">
                            <FormGroup className="step3Div" id="ul-grounds">
                                <FormControlLabel control={<Checkbox value={0} />} label="I am exempt from the requirement to hold a BC driver's licence." />
                            <FormControlLabel control={<Checkbox value={1} />} label="I have become exempt from the requirement to hold a BC driver's licence since the notice of prohibition was served." />
                            <FormControlLabel control={<Checkbox value={2} />} label="My driving record should not have identified me as an unlicensed driver. " />                           
                        </FormGroup>
                    </div>
                }
                {controlIsIrp &&
                    <div className="step3Div"  id="dataInfoIrp">
                        <FormGroup className="step3Div"  id="irp-grounds">
                            <FormControlLabel control={<Checkbox />} label="I was not the driver or in care or control of the motor vehicle." />
                            <FormControlLabel control={<Checkbox />} label="I was not advised of my right to a second breath test on an approved screening device." />
                            <FormControlLabel control={<Checkbox />} label="I requested a second test but the officer did not perform it." />
                            <FormControlLabel control={<Checkbox />} label="My second test was not performed on a different approved screening device." />
                            <FormControlLabel control={<Checkbox />} label="The prohibition was not served based on the lower approved screening device result." />
                            <FormControlLabel control={<Checkbox />} label="The result of the approved screening device is not reliable." />
                            <FormControlLabel control={<Checkbox />} label="The approved screening device that was the basis for my prohibition did not register a warn." />
                            <FormControlLabel control={<Checkbox />} label="The approved screening device registered a warn, but my blood alcohol content was less than 0.05 (50 milligrams of alcohol in 100 millilitres of blood)." />
                            <FormControlLabel control={<Checkbox />} label="The approved screening device that was the basis for my prohibition did not register a fail." />
                            <FormControlLabel control={<Checkbox />} label="The approved screening device registered a fail, but my blood alcohol content was less than 0.08 (80 milligrams of alcohol in 100 millilitres of blood)." />
                            <FormControlLabel control={<Checkbox />} label="My 7-day or 30-day prohibition should be reduced because I did not have the prescribed number of prior warn range prohibitions." />
                            <FormControlLabel control={<Checkbox />} label="I did not refuse or fail to comply with a demand for a breath sample." />
                            <FormControlLabel control={<Checkbox />} label="I had a reasonable excuse for refusing or failing to comply with a demand." />
                        </FormGroup>
                    </div>
                }
                {controlIsAdp &&
                    <div className="step3Div"  id="dataInfoAdp">
                        <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>SECTION 94.1(1)(a) - Blood Alcohol Concentration</span></strong></div>
                        <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>(optional)</span></strong></div>
                        <FormGroup className="step3Div"  id="adp-grounds-alochol">
                            <FormControlLabel control={<Checkbox />} label="I did not operate a motor vehicle." />
                            <FormControlLabel control={<Checkbox />} label="I did not have, within 2 hours after ceasing to operate a motor vehicle, a blood alcohol concentration equal to or exceeding 80 milligrams (mg) of alcohol in 100 millilitres (mL) of blood." />
                            <FormControlLabel control={<Checkbox />} label="All of the following apply: " />
                            <ul>
                                <li>I consumed alcohol after ceasing to operate the motor vehicle;</li>
                                <li>After ceasing to operate the motor vehicle, I had no reasonable expectation that I would be required to provide a sample of breath or blood;&nbsp;<strong>and</strong></li>
                                <li>My alcohol consumption was consistent with my blood alcohol concentration as determined by the analysis of my breath or blood and with my having had, at the time when I was operating the motor vehicle, a blood alcohol concentration that was less than 80 mg of alcohol in 100 mL of blood.</li>
                            </ul>
                        </FormGroup>
                        <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>SECTION 94.1(1)(a.1) - Blood Drug Concentration</span></strong></div>
                        <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>(optional)</span></strong></div>
                        <FormGroup className="step3Div"  id="adp-grounds-drug">
                            <FormControlLabel control={<Checkbox />} label="I did not operate a motor vehicle." />
                            <FormControlLabel control={<Checkbox />} label="I did not have, within 2 hours after ceasing to operate a motor vehicle, a blood drug concentration equal to or exceeding the blood drug concentration for the drug that is prescribed for this section." />
                            <FormControlLabel control={<Checkbox />} label="Both of the following apply: " />
                            <ul>
                                <li>I consumed the drug after ceasing to operate the motor vehicle; <strong>and</strong></li>
                                <li>After ceasing to operate the motor vehicle, I had no reasonable expectation that I would be required to provide a sample of blood.</li>
                            </ul>
                        </FormGroup>
                        <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>SECTION 94.1(1)(a.2) - Blood Alcohol and Drug Concentration</span></strong></div>
                        <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>(optional)</span></strong></div>
                        <FormGroup className="step3Div"  id="adp-grounds-alcohol-and-drug">
                            <FormControlLabel control={<Checkbox />} label="I did not operate a motor vehicle." />
                            <FormControlLabel control={<Checkbox />} label="I did not have, within 2 hours after ceasing to operate a motor vehicle, a blood drug concentration and a blood alcohol concentration equal to or exceeding the amounts prescribed for this section." />
                            <FormControlLabel control={<Checkbox />} label="All of the following apply: " />
                            <ul>
                                <li>I consumed alcohol or the drug, or both, after ceasing to operate the motor vehicle;</li>
                                <li>After ceasing to operate the motor vehicle, I had no reasonable expectation that I would be required to provide a sample of breath or blood, or both; <strong>and</strong></li>
                                <li>My alcohol consumption was consistent with my blood alcohol concentration as determined by the analysis of my breath or blood and with my having had, at the time when I was operating the motor vehicle, a blood alcohol concentration that was less than the blood alcohol concentration that is prescribed for the purposes of this section.</li>
                            </ul>
                        </FormGroup>
                        <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>SECTION 94.1(1)(a.3) - Drug Recognition Expert Evaluation</span></strong></div>
                        <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>(optional)</span></strong></div>
                        <FormGroup className="step3Div"  id="adp-grounds-drug-expert">
                            <FormControlLabel control={<Checkbox />} label="I did not operate a motor vehicle." />
                            <FormControlLabel control={<Checkbox />} label="My evaluation was not conducted by an evaluating officer." />
                            <FormControlLabel control={<Checkbox />} label="The evaluating officer did not comply with the requirements that are prescribed for the purposes of this section." />
                            <FormControlLabel control={<Checkbox />} label="The analysis of my bodily substance did not confirm the presence in my body of one or more of the types of drugs identified by the evaluating officer as impairing my ability to operate a motor vehicle." />
                            <FormControlLabel control={<Checkbox />} label={<p><span>My ability to operate a motor vehicle was not impaired to any degree by a drug or by a combination of alcohol and a drug at the time of the evaluation, </span><strong>and</strong> <span>the results of the evaluation were due to a medical condition.</span></p> }/>
                            <FormControlLabel control={<Checkbox />} label="Both of the following apply:" />
                            <ul>
                                <li>I consumed one or more of the types of drugs identified by the evaluating officer as impairing my ability to operate a motor vehicle after ceasing to operate the motor vehicle; <strong>and</strong></li>
                                <li>After ceasing to operate the motor vehicle, I had no reasonable expectation that I would be required to provide a sample of a bodily substance.</li>
                            </ul>
                        </FormGroup>
                        <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>SECTION 94.1(1)(b) - Refusal or Failure to Comply</span></strong></div>
                        <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>(optional)</span></strong></div>
                        <FormGroup className="step3Div"  id="adp-grounds-refusal">
                            <FormControlLabel control={<Checkbox />} label="I did not operate a motor vehicle." />
                            <FormControlLabel control={<Checkbox />} label={<p><span>I did not refuse or fail to comply with a demand made under <a href="https://laws-lois.justice.gc.ca/eng/acts/c-46/page-71.html#docCont" rel="noopener" target="_blank">s.320.27</a> or <a href="https://laws-lois.justice.gc.ca/eng/acts/c-46/page-71.html#docCont" rel="noopener" target="_blank">s.320.28</a> of the Criminal Code.</span></p> } />
                            <FormControlLabel control={<Checkbox />} label={<span>I had a reasonable excuse for refusing to comply with the demand made under <a href="https://laws-lois.justice.gc.ca/eng/acts/c-46/page-71.html#docCont" rel="noopener" target="_blank">s.320.27</a> or <a href="https://laws-lois.justice.gc.ca/eng/acts/c-46/page-71.html#docCont" rel="noopener" target="_blank">s.320.28</a> of the Criminal Code.</span> } />
                            
                        </FormGroup> 
                        <div className="step3Div" >
                            <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>Grounds checked</span></strong></div>
                            <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>(optional)</span></strong></div>                            
                                <TextField id="grounds-checked-field" style={{ paddingLeft: '5px' }}
                                    variant="outlined" name='groundsChecked' disabled>
                                </TextField>
                        </div>
                        
                    </div>

                }
                </div>
            </Grid>
            <Grid item xs={8} sx={{ padding: "1px" }}>
            <div className="step3Div"  id="prepareForReviewUl">
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
            <Grid item xs={8} sx={{ padding: "1px" }}>
                {controlIsAdp &&
                    <FormField
                        id="review-type"
                        labelText="Please select a review type:"
                        tooltipTitle="Please select a review type:"
                        tooltipContent={<p>In a written review you won&apos;t be able to talk to the adjudicator. Oral reviews are 30 minutes long and conducted by phone only.</p>}
                    >
                        <RadioGroup id="review-type"
                            aria-labelledby="demo-radio-buttons-group-label"
                            name="reviewType"
                        >
                            <FormControlLabel value="yes" control={<Radio sx={{
                                '&.Mui-checked': {
                                    color: 'rgb(49,49,50)',
                                },
                            }} />} label="Written review ($100)" />
                            <FormControlLabel value="no" control={<Radio sx={{
                                '&.Mui-checked': {
                                    color: 'rgb(49,49,50)',
                                },
                            }} />} label="Oral review ($200)" />
                        </RadioGroup>
                    </FormField>
                }
                </Grid>
            <Grid item xs={8} sx={{ padding: "1px" }}>
                           
                {controlIsUl &&
                    <div className="step3Div"  id="additionalInfoUl"> 
                        <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>Additional Information:</span></strong></div>
                        <ul>
                            <li>If you are claiming that you are exempt from the requirement to hold a BC driver&apos;s licence, you will need to submit evidence that supports your application.</li>
                            <li>If you believe that you should not have been identified as an unlicensed driver, you will need to explain why you held that belief.</li>
                            <li>The adjudicator will also consider your driving record in the review; you can <a href="https://www.icbc.com/driver-licensing/getting-licensed/Pages/Your-driving-record.aspx" rel="noopener" target="_blank">get a copy from ICBC</a>.</li>
                        </ul>
                    </div>
                }
            </Grid>
            <Grid item xs={8} sx={{ padding: "1px" }}>
                {controlIsIrp &&
                    <div className="step3Div"  id="additionalInfoIrp">
                        <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>Additional Information:</span></strong></div>
                        <ul>
                            <li><a href="https://www2.gov.bc.ca/gov/content/transportation/driving-and-cycling/roadsafetybc/prohibitions/apply-online/certificates" rel="noopener" target="_blank">Technical materials</a> the adjudicator may rely on in the review.</li>
                        </ul>
                    </div>
                }
            </Grid><Grid item xs={8} sx={{ padding: "1px" }}>
                {controlIsUl &&
                    <div className="step3Div"  id="writtenReviewInfoUl"> 
                        <div className="step3Div" ><strong><span style={{ fontSize: '16px' }}>Written Review Information:</span></strong></div>
                        <ul>
                            <li>You can provide a written statement and evidence that address the grounds you selected in this application.</li>
                            <li>In a written review you won&apos;t be able to talk to the adjudicator.</li>
                        </ul>
                    </div>
                }   
                </Grid>
        </div>
    );
};
export default Step3;

