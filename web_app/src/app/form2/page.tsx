'use client'
import Image from 'next/image';
import MUIAccordion, { AccordionProps } from '@mui/material/Accordion';
import AccordionActions from '@mui/material/AccordionActions';
import MUIAccordionSummary, { AccordionSummaryProps } from '@mui/material/AccordionSummary';
import MUIAccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Button from '@mui/material/Button';
import ArrowForwardIosSharpIcon from '@mui/icons-material/ArrowForwardIosSharp';
import Typography from '@mui/material/Typography';
import styled from '@emotion/styled';
import { createContext } from 'react'
import { ArrowBackIosNewSharp, ArrowDownwardSharp, ArrowRightAltSharp, ArrowRightSharp, Expand, ExpandCircleDown, ExpandCircleDownTwoTone, ExpandLess, KeyboardArrowRight } from '@mui/icons-material';


const Accordion = styled((props: AccordionProps) => (
    <MUIAccordion disableGutters elevation={0} square {...props} />
))(({ theme }) => ({
    '&:not(:last-child)': {
        borderBottom: 0,
    },
    '&::before': {
        display: 'none',
    },
}));

const AccordionSummary = styled((props: AccordionSummaryProps) => (
    <MUIAccordionSummary
        expandIcon={<ArrowBackIosNewSharp sx={{ fontSize: '0.9rem' }} />}
        {...props}
    />
))(({ theme }) => ({
    flexDirection: 'row-reverse',
    '& .MuiAccordionSummary-expandIconWrapper.Mui-expanded': {
        transform: 'rotate(90deg)',
    },
    
}));

const AccordionDetails = styled(MUIAccordionDetails)(({ theme }) => ({
    borderTop: '1px solid rgba(0, 0, 0, .125)',
}));
export default function Page() {   

    return <div>
        <h1>Notice of Driving Prohibition Application for Review</h1>
       
        <Accordion>
            <AccordionSummary
                expandIcon={< KeyboardArrowRight />}
                aria-controls="panel1-content"
                id="panel1-header"
            >
                <h2>Before You Begin</h2>
            </AccordionSummary>
            <AccordionDetails>
                <p>When you see this symbol<Image
                    src="/./././assets/icons/info-icon.png"
                    width={20}
                    height={20}
                    alt="Info" />
                    click here for more information.
                </p>
                <p>Submit only <strong> 1 online application</strong> for your prohibition review.</p>
                <p>You&apos;ll receive at least <strong> 2 emails</strong> when you submit the form:</p>
                <p>1. A copy of your completed application, and</p>
                <p>2. The next step in the application process.</p>
                <p>If you don&apos;t enter anything in the form for 15 minmutes, it may time out.</p>
            </AccordionDetails>
        </Accordion>
        <Accordion>
            <AccordionSummary
                expandIcon={< KeyboardArrowRight />}
                aria-controls="panel1-content"
                id="panel1-header"
            >
                <h2>Step 1: Enter Prohibition Information</h2>
            </AccordionSummary>
            <AccordionDetails>
                <p>When you see this symbol<Image
                    src="/./././assets/icons/info-icon.png"
                    width={20}
                    height={20}
                    alt="Info" />
                    click here for more information.
                </p>
                <p>Submit only <strong> 1 online application</strong> for your prohibition review.</p>
                <p>You&apos;ll receive at least <strong> 2 emails</strong> when you submit the form:</p>
                <p>1. A copy of your completed application, and</p>
                <p>2. The next step in the application process.</p>
                <p>If you don&apos;t enter anything in the form for 15 minmutes, it may time out.</p>
            </AccordionDetails>
        </Accordion>
        <Accordion>
            <AccordionSummary
                expandIcon={< KeyboardArrowRight />}
                aria-controls="panel1-content"
                id="panel1-header"
            >
                <h2>Step 2: Enter Applicant Information</h2>
            </AccordionSummary>
            <AccordionDetails>
                <p>When you see this symbol<Image
                    src="/./././assets/icons/info-icon.png"
                    width={20}
                    height={20}
                    alt="Info" />
                    click here for more information.
                </p>
                <p>Submit only <strong> 1 online application</strong> for your prohibition review.</p>
                <p>You&apos;ll receive at least <strong> 2 emails</strong> when you submit the form:</p>
                <p>1. A copy of your completed application, and</p>
                <p>2. The next step in the application process.</p>
                <p>If you don&apos;t enter anything in the form for 15 minmutes, it may time out.</p>
            </AccordionDetails>
        </Accordion>
        <Accordion>
            <AccordionSummary
                expandIcon={< KeyboardArrowRight />}
                aria-controls="panel1-content"
                id="panel1-header"
            >
                <h2>Step 3: Complete Review Information</h2>
            </AccordionSummary>
            <AccordionDetails>
                <p>When you see this symbol hi<Image
                    src="/./././assets/icons/info-icon.png"
                    width={20}
                    height={20}
                    alt="Info" />
                    click here for more information.
                </p>
                <p>Submit only <strong> 1 online application</strong> for your prohibition review.</p>
                <p>You&apos;ll receive at least <strong> 2 emails</strong> when you submit the form:</p>
                <p>1. A copy of your completed application, and</p>
                <p>2. The next step in the application process.</p>
                <p>If you don&apos;t enter anything in the form for 15 minmutes, it may time out.</p>
            </AccordionDetails>
        </Accordion>
        <Accordion>
            <AccordionSummary
                expandIcon={< KeyboardArrowRight />}
                aria-controls="panel1-content"
                id="panel1-header"
            >
                <h2>Step 4: Consent and Submit</h2>
            </AccordionSummary>
            <AccordionDetails>
                <p>When you see this symbol<Image
                    src="/./././assets/icons/info-icon.png"
                    width={20}
                    height={20}
                    alt="Info" />
                    click here for more information.
                </p>
                <p>Submit only <strong> 1 online application</strong> for your prohibition review.</p>
                <p>You&apos;ll receive at least <strong> 2 emails</strong> when you submit the form:</p>
                <p>1. A copy of your completed application, and</p>
                <p>2. The next step in the application process.</p>
                <p>If you don&apos;t enter anything in the form for 15 minmutes, it may time out.</p>
            </AccordionDetails>
        </Accordion>

        </div>
}