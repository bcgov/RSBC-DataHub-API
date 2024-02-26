import MUIAccordion, { AccordionProps } from '@mui/material/Accordion';
import MUIAccordionSummary, { AccordionSummaryProps } from '@mui/material/AccordionSummary';
import MUIAccordionDetails from '@mui/material/AccordionDetails';
import styled from '@emotion/styled';
import { KeyboardArrowRight } from '@mui/icons-material';
import Typography from '@mui/material/Typography';
import  React, { useState, ReactNode } from 'react';


type CustomAccordionProps = {
    title: string;
    content: ReactNode;
}
const AccordionSummary = styled((props: AccordionSummaryProps) => (
    <MUIAccordionSummary
        expandIcon={<KeyboardArrowRight sx={{ fontSize: '30px' }} />}
        {...props}
    />
))(({ theme }) => ({
    flexDirection: 'row-reverse',
    '& .MuiAccordionSummary-expandIconWrapper.Mui-expanded': {
        transform: 'rotate(90deg)',
    },
    '.MuiAccordionSummary-root': {
        padding: '0px 10px',
    },
    '.MuiAccordionSummary-content': {
        margin: '0px',
    },
    '.MuiAccordion-root': {
        paddingBottom: '20px',
        display: 'table-cell',
    },
    '.MuiBox-root': {
        display: 'table-cell',
    }


}));

const AccordionDetails = styled(MUIAccordionDetails)(({ theme }) => ({
    borderTop: '0px solid rgba(0, 0, 0, .125)',
}));

const Accordion = styled((props: AccordionProps) => (
    <MUIAccordion disableGutters elevation={0} square {...props} />
))(({ theme }) => ({
    '&:not(:last-child)': {
        borderBottom: 0,
        margin: '0px',
        fontSize: '30px',
    },
    '&::before': {
        display: 'none',
    },
}));

const CustomAccordion: React.FC<CustomAccordionProps> = ({ title, content }) => {

    const [expanded, setExpanded] = useState<string | false>(false);

    const toggleAccordion = (panel: string) => (event: React.ChangeEvent<{}>, isExpanded : boolean) => {
        setExpanded(isExpanded ? panel : false);
    };
    
    return (
        <Accordion expanded={expanded === 'panel1'} onChange={toggleAccordion('panel1')} style={{paddingBottom:'10px'} }>
            <AccordionSummary 
            expandIcon={< KeyboardArrowRight />}
            aria-controls="panel1-content"
            id="panel1-header" className="accordionSummary header2"
            >
                <h2 className="header2" style={{fontSize:"30px", margin:"0px"} }><Typography style={{ textDecoration: "none", color: "#555", minHeight: "36px", fontSize: "30px",  }}>{title}</Typography></h2>
            </AccordionSummary>
            <AccordionDetails style={{ paddingLeft:'30px' }}>
                {content}
        </AccordionDetails>
    </Accordion>
    )
}
export default CustomAccordion;