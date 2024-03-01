import React from 'react';
import { Step3InputProps } from '../../interfaces';

const Step3: React.FC<Step3InputProps> = ({ controlIsUl, controlIsIrp, controlIsAdp }) => {  

    return (
        <div style={{ display: 'grid', fontSize:'16px' }}>                    
            <div id="reviewInfo">
                {controlIsUl &&
                    <div id="reviewTextUl">
                        <p style={{ marginBottom: '20px', }}>This review is available if you have been served with a Notice of Prohibition under <a href="https://www.bclaws.ca/civix/document/id/complete/statreg/96318_12" rel="noopener" target="_blank">s.251(1)</a> of the Motor Vehicle Act, and are prohibited from driving under <a href="https://www.bclaws.ca/civix/document/id/complete/statreg/96318_12" rel="noopener" target="_blank">s.251(4)</a>. This driving prohibition will be terminated without a review if ICBC issues you a BC driver&apos;s licence.
                        </p>
                        <p style={{ marginBottom: '20px', }}>The information you&apos;ll provide should address the grounds you choose below. Hardship is not a consideration in a review.</p>
                        <p style={{ marginBottom: '20px', }}>These are the only grounds for review under <a href="https://www.bclaws.ca/civix/document/id/complete/statreg/96318_12" rel="noopener" target="_blank">s.261</a> of the Motor Vehicle Act. They have been simplified for readability.</p>
                        <p style={{ marginBottom: '20px', }}>You must select at least 1 ground:</p>
                    </div>
                }
                {controlIsIrp &&
                    <div id="reviewTextIrp">
                        <p>The information you will provide should address the grounds you choose below. The burden of proof is on the applicant in a review. Hardship is not a consideration in a review.</p>
                        <p>These are the only grounds for review under <a href="https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/96318_07">s.215.5</a> of the Motor Vehicle Act. They have been simplified for readability.</p>
                        <p>You must select at least 1 ground:</p>
                    </div>
                }
                {controlIsAdp &&
                    <div id="reviewTextAdp">
                        <p>The information you will provide should address the grounds you choose below. The burden of proof is on the applicant in a review. Hardship is not a consideration in a review.</p>
                        <p>These are the only grounds for review under <a href="https://www.bclaws.ca/civix/document/id/complete/statreg/96318_02#section94.6" rel="noopener" target="_blank">s.94.6</a> of the Motor Vehicle Act. They have been simplified for readability.</p>
                        <p>Check grounds for the type of ADP that was served on you. You must select at least 1 ground:</p>
                    </div>
                }
            </div>
            <div id="prepareForReviewUl">
                <div><strong><span style={{ fontSize: '16px' }}>Preparing for your review:</span></strong></div>
                <ul style={{ marginLeft: '20px' }}>
                    <li>Before your review, we&apos;ll send you the police evidence.</li>
                    <li>You can use the evidence to prepare for your review.</li>
                    <li>The adjudicator will use it with the information you submit to make a decision about your prohibition.</li>
                    <li>A lawyer may represent you in your review.&nbsp;</li>
                    <li>Review decisions are sent by regular mail.</li>
                </ul>
            </div>
            <div id="additionalInfo">                
                {controlIsUl &&
                    <div id="additionalInfoUl"> 
                        <div><strong><span style={{ fontSize: '16px' }}>Additional Information:</span></strong></div>
                        <ul>
                            <li>If you are claiming that you are exempt from the requirement to hold a BC driver&apos;s licence, you will need to submit evidence that supports your application.</li>
                            <li>If you believe that you should not have been identified as an unlicensed driver, you will need to explain why you held that belief.</li>
                            <li>The adjudicator will also consider your driving record in the review; you can <a href="https://www.icbc.com/driver-licensing/getting-licensed/Pages/Your-driving-record.aspx" rel="noopener" target="_blank">get a copy from ICBC</a>.</li>
                        </ul>
                    </div>
                }
                {controlIsIrp &&
                    <div id="additionalInfoIrp">
                        <div><strong><span style={{ fontSize: '16px' }}>Additional Information:</span></strong></div>
                        <ul>
                            <li><a href="https://www2.gov.bc.ca/gov/content/transportation/driving-and-cycling/roadsafetybc/prohibitions/apply-online/certificates" rel="noopener" target="_blank">Technical materials</a> the adjudicator may rely on in the review.</li>
                        </ul>
                    </div>
                }
                {controlIsAdp &&
                    <div id="additionalInfoAdp"></div>
                }
            </div>
            <div id="writtenReviewInfo">                
                {controlIsUl &&
                    <div id="writtenReviewInfoUl"> 
                        <div><strong><span style={{ fontSize: '16px' }}>Written Review Information:</span></strong></div>
                        <ul>
                            <li>You can provide a written statement and evidence that address the grounds you selected in this application.</li>
                            <li>In a written review you won&apos;t be able to talk to the adjudicator.</li>
                        </ul>
                    </div>
                }               
            </div>
        </div>
    );
};
export default Step3;

