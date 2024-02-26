'use client'
import { FormEvent } from 'react';
import Image from 'next/image';
import CustomAccordion from '../components/Accordion';
import Step1 from './steps/Step1';
import Step2 from './steps/Step2';
import Step3 from './steps/Step3';
import Step4 from './steps/Step4';


export default function Page() {
    async function onSubmit(event: FormEvent<HTMLFormElement>){
        event.preventDefault()

        const formData = new FormData(event.currentTarget)
        const response = await fetch('/api/submit', {
            method: 'POST',
            body: formData,
        })

    const data = await response.json()
        console.log(data);
    }
    return <div>
            <h1 className="header1">Notice of Driving Prohibition Application for Review</h1>
        <div className="formContent">
        <CustomAccordion title="Before You Begin:"
                content={<div style={{ fontSize: "16px", fontFamily:"'BC Sans', 'Noto Sans',  Arial, sans-serif"} }><p>When you see this symbol <Image
                src="/./././assets/icons/info-icon.png"
                width={15}
                height={15}
                alt="Info" />
            &nbsp;click it for more information.
        </p>
        <p>Submit only <strong> 1 online application</strong> for your prohibition review.</p>
                    <p>You&apos;ll receive at least <strong> 2 emails</strong> when you submit the form:</p>
        <ol>
        <li>A copy of your completed application, and</li>
                        <li>The next step in the application process.</li>
                    </ol>
                <p>If you don&apos;t enter anything in the form for 15 minmutes, it may time out.</p> </div>} />


            <CustomAccordion title="Step 1: Enter Prohibition Information"
                content={<Step1></Step1>} />

      

        <CustomAccordion title="Step 2: Enter Applicant Information"
            content={<Step2></Step2>} />

        <CustomAccordion title="Step 3: Complete Review Information"
            content={<Step3></Step3>} />

        <CustomAccordion title="Step 4: Consent and Submit"
            content={<Step4> </Step4>} />   
        </div>
    </div >
}