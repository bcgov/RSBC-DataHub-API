import { jsPDF,  } from "jspdf";
import html2canvas from 'html2canvas';

type props = {
    id: string;
    pageNumber: number;
};

export const generatePDF = async (value: props[], headerText:string): Promise<jsPDF | null> => {
    const doc = new jsPDF("p", "mm", "a4", true);

    const totalPages : number = value.at(value.length - 1)?.pageNumber as number ;

    for (let i = 1; i <= totalPages; i++) {

        const imgWidth = 190;
        const pageHeight = 295;
        const margin = 15;
        //Add header
        doc.setFontSize(10);
        doc.text(headerText, 15, 10);
        doc.setLineWidth(0.5);
        doc.line(15, 15, doc.internal.pageSize.getWidth() - 15, 15);

        //Add footer
        const footerText = `${i}/${totalPages}`;
        doc.text(headerText, 15, pageHeight - 10);
        doc.text(footerText, doc.internal.pageSize.getWidth() - 15 - doc.getStringUnitWidth(footerText) * doc.getFontSize() / 2, pageHeight - 10);
        doc.line(15, pageHeight - 20, doc.internal.pageSize.getWidth() - 15, pageHeight - 20);

        let yPosition = 20;
        for (const element of value) {
            if (element.pageNumber === i) {                
                const content = document.getElementById(element.id);
                const canvas = await html2canvas(content as HTMLElement);
                const img = canvas.toDataURL("image/png", 0.8);
               
                const imgHeight = canvas.height * imgWidth / canvas.width;
                if (img !== 'data:,') {
                        doc.addImage(img, 'PNG', margin, yPosition, imgWidth, imgHeight);
                        yPosition += imgHeight + 5;    
                }
            }
        }

        if (i !== totalPages)
            doc.addPage();

    }    
    return doc;
}
