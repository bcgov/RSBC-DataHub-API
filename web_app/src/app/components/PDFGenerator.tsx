'use client';
import { jsPDF } from 'jspdf';
import html2pdf from 'html2pdf.js';

interface PdfOptions {
    margin?: number;
    filename?: string;
    image?: { type: string; quality: number };
    html2canvas?: { scale: number };
    jsPDF?: { unit: string; format: string; orientation: string, compress: boolean, putOnlyUsedFonts: boolean };
    pagebreak?: { mode: string[] };
}

export async function generatePDFWithHeaderFooter(
    element: HTMLElement,
    title: string,
    options: PdfOptions = {}
) {
    const defaultOptions: PdfOptions = {
        margin: 15,
        filename: 'document.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait', compress: true, putOnlyUsedFonts: true },
        pagebreak: { mode: ['avoid-all', 'css', 'legacy'] },
        
    };

    const opt = { ...defaultOptions, ...options };
    
    return html2pdf().from(element).set(opt).toPdf().get('pdf').then((pdf: jsPDF) => {
        const totalPages = pdf.internal.pages;
        console.log("pages are: " + totalPages.length );
        for (let i = 1; i < totalPages.length; i++) {
            pdf.setPage(i);
            const pageHeight = pdf.internal.pageSize.getHeight();
            const pageWidth = pdf.internal.pageSize.getWidth();
            const margin = 15;
    
            // Add header
            pdf.setFontSize(9);
            pdf.text(title, margin + 1, 10);
            pdf.setLineWidth(0.3);
            pdf.line(margin, 12, pageWidth - margin, 12);
    
            // Add footer
            const footerText = `${i}/${totalPages.length}`;
            pdf.text(title, margin + 1, pageHeight - 10);
            pdf.text(footerText, pageWidth - margin - pdf.getStringUnitWidth(footerText) * pdf.getFontSize() / 2, pageHeight - 10);
            pdf.line(margin, pageHeight - 15, pageWidth - margin, pageHeight - 15);
        }
        return pdf;
    });
}