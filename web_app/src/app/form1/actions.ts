'use server'
import type { NextApiRequest, NextApiResponse } from 'next';
import { generatePDFpuppeteer } from '../components/GeneratePDF';

//------------------------------------------
//PDF generation api call 
//------------------------------------------
export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse
) {
    try {
        const html = req.body.html;
        const pdfBuffer = await generatePDFpuppeteer(html);
        res.setHeader('Content-Type', 'application/pdf');
        res.send(pdfBuffer);
    }
    catch (error) {
        console.error(error);
        res.status(500).send('Internal Server Error');
    }
}
