import React from 'react';
import { Step3InputProps } from '../../interfaces';

const Step3: React.FC<Step3InputProps> = ({ controlIsUl, controlIsIrp, controlIsAdp }) => {  

    return (
        <div style={{ display: 'grid', fontSize:'16px' }}>
            {
                controlIsUl &&
                <div id="reviewInfoUl">
                        <div id="reviewTextUl">
                            <p>The information you will provide should address the grounds you choose below. The burden of proof is on the applicant in a review. Hardship is not a consideration in a review.</p>
                            <p>These are the only grounds for review under <a href="https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/96318_07">s.215.5</a> of the Motor Vehicle Act. They have been simplified for readability.</p>
                        </div>
                        <div id="prepareForReviewUl" >
                            <div><strong><span style={{ fontSize: '16px' }}>Preparing for your review:</span></strong></div>
                            <ul>
                                <li>Before your review, we&apos;ll send you the police evidence.</li>
                                <li>You can use the evidence to prepare for your review.</li>
                                <li>The adjudicator will use it with the information you submit to make a decision about your prohibition.</li>
                                <li>A lawyer may represent you in your review.&nbsp;</li>
                                <li>Review decisions are sent by regular mail.</li></ul>
                        </div>
                        <div id="additionalInfoUl" >
                            <div><strong><span style={{ fontSize: '16px' }}>Additional Information:</span></strong></div>
                            <ul>
                                <li>If you are claiming that you are exempt from the requirement to hold a BC driver&apos;s licence, you will need to submit evidence that supports your application.</li>
                                <li>If you believe that you should not have been identified as an unlicensed driver, you will need to explain why you held that belief.</li>
                                <li>The adjudicator will also consider your driving record in the review; you can <a href="https://www.icbc.com/driver-licensing/getting-licensed/Pages/Your-driving-record.aspx" rel="noopener" target="_blank">get a copy from ICBC</a>.</li>
                            </ul>
                        </div>
                        <div id="writtenReviewInfoUl">
                            <div><strong><span style={{ fontSize: '16px' }}>Written Review Information:</span></strong></div>
                            <ul>
                                <li>You can provide a written statement and evidence that address the grounds you selected in this application.</li>
                                <li>In a written review you won&apos;t be able to talk to the adjudicator.</li>
                            </ul>
                        </div>
                </div>
            }
            {
                controlIsIrp &&
                <div id="reviewInfoIrp">
                        <div id="reviewTextIrp">
                            <p>The information you will provide should address the grounds you choose below. The burden of proof is on the applicant in a review. Hardship is not a consideration in a review.</p>                        
                            <p>These are the only grounds for review under <a href="https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/96318_07">s.215.5</a> of the Motor Vehicle Act. They have been simplified for readability.</p>
                        </div>
                        <div id="prepareForReviewIrp" >
                            <div><strong><span style={{ fontSize: '16px' }}>Preparing for your review:</span></strong></div>
                            <ul>
                                <li>Before your review, we&apos;ll send you the police evidence.</li>
                                <li>You can use the evidence to prepare for your review.</li>
                                <li>The adjudicator will use it with the information you submit to make a decision about your prohibition.</li>
                                <li>A lawyer may represent you in your review.&nbsp;</li>
                                <li>Review decisions are sent by regular mail.</li></ul>
                        </div>
                        <div id="additionalInfoIrp" >
                            <div><strong><span style={{ fontSize: '16px' }}>Additional Information:</span></strong></div>
                            <ul>
                                <li><a href="https://www2.gov.bc.ca/gov/content/transportation/driving-and-cycling/roadsafetybc/prohibitions/apply-online/certificates" rel="noopener" target="_blank">Technical materials</a> the adjudicator may rely on in the review.</li>
                            </ul>
                        </div>
                        <div id="writtenReviewInfoIrp">
                            <div><strong><span style={{ fontSize: '16px' }}>Written Review Information:</span></strong></div>
                            <ul>
                                <li>You can provide a written statement and evidence that address the grounds you selected in this application.</li>
                                <li>In a written review you won&apos;t be able to talk to the adjudicator.</li>
                            </ul>
                        </div>
                </div>
            }
            {
                controlIsAdp &&
                <div id="reviewInfoAdp">
                        <div id="reviewTextAdp">
                            <p>The information you will provide should address the grounds you choose below. The burden of proof is on the applicant in a review. Hardship is not a consideration in a review.</p>
                            <p>These are the only grounds for review under <a href="https://www.bclaws.gov.bc.ca/civix/document/id/complete/statreg/96318_07">s.215.5</a> of the Motor Vehicle Act. They have been simplified for readability.</p>
                        </div>
                        <div id="prepareForReviewAdp" >
                            <div><strong><span style={{ fontSize: '16px' }}>Preparing for your review:</span></strong></div>
                            <ul>
                                <li>Before your review, we&apos;ll send you the police evidence.</li>
                                <li>You can use the evidence to prepare for your review.</li>
                                <li>The adjudicator will use it with the information you submit to make a decision about your prohibition.</li>
                                <li>A lawyer may represent you in your review.&nbsp;</li>
                                <li>Review decisions are sent by regular mail.</li>
                            </ul>
                        </div>
                       
                </div>
            }
            
            

        </div>

    );
};
export default Step3;

