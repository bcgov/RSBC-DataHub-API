'use client'
import React from 'react';
import { Container, Typography } from '@mui/material';

const Acknowledgement: React.FC = () => {

    return (
        <Container maxWidth="sm" style={{ textAlign: 'center', marginTop: '50px' }}>
            <Typography variant="h4" gutterBottom>
                Thank You!
            </Typography>
            <Typography variant="body1" gutterBottom>
            Your request has been successfully submitted. Please check your email for further instructions. If you do not receive an email please contact RoadSafetyBC by calling 1-855-387-7747 and select option 5 or attend a driver licensing office.
            </Typography>
        </Container>
    );
};

export default Acknowledgement;