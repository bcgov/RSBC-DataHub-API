import React from "react";
import { jsPDF,  } from "jspdf";
import html2canvas from 'html2canvas';


type props = {
    id: string;
};

export const generatePdf = async (id: string): Promise<jsPDF | null> => {
    const content = document.getElementById(id);
    if (content) {
        const canvas = await html2canvas(content);
        const imgData = canvas.toDataURL('image/png');

        const pdf = new jsPDF({
            orientation: 'p',
            unit: 'px',
            format: [canvas.width, canvas.height]
        });

        

        pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height);
        return pdf;
    }
    return null;

}


   