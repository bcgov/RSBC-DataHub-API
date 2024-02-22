'use client'
import { FormEvent, useState } from 'react';
import Image from 'next/image';

import HelpRoundedIcon from '@mui/icons-material/HelpRounded';
import Button from '@mui/material/Button';
import ArrowForwardIosSharpIcon from '@mui/icons-material/ArrowForwardIosSharp';
import Typography from '@mui/material/Typography';
import styled from '@emotion/styled';
import { createContext } from 'react'
import TextField from '@mui/material/TextField';
import InputLabel from '@mui/material/InputLabel';
import Popover, { PopoverProps } from '@mui/material/Popover';
import CustomAccordion from '../components/Accordion';
import Step1 from './steps/step1';

export default function Page() {
    async function onSubmit(event: FormEvent<HTMLFormElement>){
        event.preventDefault()

        const formData = new FormData(event.currentTarget)
        const response = await fetch('/api/submit', {
            method: 'POST',
            body: formData,
        })

    const data = await response.json()

}
    
    
    const [containerEl, setContainerEl] = useState(null);    

    const open = Boolean(containerEl);
    const id = open ? "simple-popover" : undefined;

    return <form onSubmit={onSubmit }>
        <div id="formContent"><div id="topicTemplate" className="template container">
            <h1 className="header1" style={{ fontSize: '2.074em', paddingLeft: '25px', fontFamily: "'BC Sans', 'Noto Sans',  Arial, sans-serif", fontWeight: '600', color:'rgb(49,49,50)' }}>Notice of Driving Prohibition Application for Review</h1>
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

                <Step1></Step1>

      

        <CustomAccordion title="Step 2: Enter Applicant Information"
            content={<div><p>When you see this symbol <Image
                src="/./././assets/icons/info-icon.png"
                width={15}
                height={15}
                alt="Info" />
                &nbsp;click here for more information.
            </p>
                <p>Submit only <strong> 1 online application</strong> for your prohibition review.</p>
                <p>You&apos;ll receive at least <strong> 2 emails</strong> when you submit the form:</p>
                <p>1. A copy of your completed application, and</p>
                <p>2. The next step in the application process.</p>
                <p>If you don&apos;t enter anything in the form for 15 minmutes, it may time out.</p> </div>} />

        <CustomAccordion title="Step 3: Complete Review Information"
            content={<div><p>When you see this symbol <Image
                src="/./././assets/icons/info-icon.png"
                width={15}
                height={15}
                alt="Info" />
                &nbsp;click here for more information.
            </p>
                <p>Submit only <strong> 1 online application</strong> for your prohibition review.</p>
                <p>You&apos;ll receive at least <strong> 2 emails</strong> when you submit the form:</p>
                <p>1. A copy of your completed application, and</p>
                <p>2. The next step in the application process.</p>
                <p>If you don&apos;t enter anything in the form for 15 minmutes, it may time out.</p> </div>} />

        <CustomAccordion title="Step 4: Consent and Submit"
            content={<div><p>When you see this symbol <Image
                src="/./././assets/icons/info-icon.png"
                width={15}
                height={15}
                alt="Info" />
                &nbsp;click here for more information.
            </p>
                <p>Submit only <strong> 1 online application</strong> for your prohibition review.</p>
                <p>You&apos;ll receive at least <strong> 2 emails</strong> when you submit the form:</p>
                <p>1. A copy of your completed application, and</p>
                <p>2. The next step in the application process.</p>
                    <p>If you don&apos;t enter anything in the form for 15 minmutes, it may time out.</p> </div>} />   
        </div>
    </div >
        </div>
    </form>
}