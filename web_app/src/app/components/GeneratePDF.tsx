import { jsPDF,  } from "jspdf";
import html2canvas from 'html2canvas';

type props = {
    id: string;
    pageNumber: number;
};

export const generatePdf = async (id: string): Promise<jsPDF | null> => {
     
    const content2 = document.getElementById(id);
    const canvas2 = await html2canvas(content2 as HTMLElement);
    const imgData = canvas2.toDataURL('image/png');
    const imgWidth = 210;
    const pageHeight = 295;
    const imgHeight = canvas2.height * imgWidth / canvas2.width;
    let heightLeft = imgHeight;
    const doc = new jsPDF('p', 'mm');
    let position = 10; // give some top padding to first page

    const totalPages = Math.ceil(heightLeft / (pageHeight - 20)) ;

    const addHeaderFooter = (doc: jsPDF, pageNumber: number) => {
        //add header
        doc.setFontSize(10);
        doc.text('Notice of Driving Prohibition Application for Review', 15, 10);
        doc.setLineWidth(0.5);
        doc.line(15, 12, doc.internal.pageSize.getWidth() - 15, 12);

        //Add footer
        const footerText = `${pageNumber}/${totalPages}`;
        doc.text('Notice of Driving Prohibition Application for Review', 15, pageHeight - 10);
        doc.text(footerText, doc.internal.pageSize.getWidth() - 15 - doc.getStringUnitWidth(footerText) * doc.getFontSize() /2, pageHeight - 10);
        doc.line(15, pageHeight - 12, doc.internal.pageSize.getWidth() - 15 , pageHeight - 12);
    }
    addHeaderFooter(doc, 1);
    let pageNumber = 2;
    doc.addImage(imgData, 'PNG', 15, position, imgWidth, imgHeight);
    heightLeft = heightLeft - pageHeight -30;

    while (heightLeft >= 0) {
        position = heightLeft - imgHeight + 10; // top padding for other pages
        doc.addPage();
        addHeaderFooter(doc, pageNumber);
        doc.addImage(imgData, 'PNG', 15, position, imgWidth, imgHeight);
        heightLeft -= (pageHeight - 30);
        pageNumber++;
    }
    doc.save('file.pdf');   
    return doc;

}

export const generatePdfIds = async (value: props[]): Promise<jsPDF | null> => {
    const doc = new jsPDF("p", "mm", "a4");

    const totalPages : number = value.at(value.length - 1)?.pageNumber as number ;

    for (let i = 1; i <= totalPages; i++) {

        const imgWidth = 170;
        const pageHeight = 295;
        const margin = 15;
        //Add header
        doc.setFontSize(10);
        doc.text('Notice of Driving Prohibition Application for Review', 15, 10);
        doc.setLineWidth(0.5);
        doc.line(15, 15, doc.internal.pageSize.getWidth() - 15, 15);

        //Add footer
        const footerText = `${i}/${totalPages}`;
        doc.text('Notice of Driving Prohibition Application for Review', 15, pageHeight - 10);
        doc.text(footerText, doc.internal.pageSize.getWidth() - 15 - doc.getStringUnitWidth(footerText) * doc.getFontSize() / 2, pageHeight - 10);
        doc.line(15, pageHeight - 20, doc.internal.pageSize.getWidth() - 15, pageHeight - 20);

        console.log('page:' + i);
        let yPosition = 20;
        for (const element of value) {
            console.log('element:' + element.id);
            console.log('element page:' + element.pageNumber);
            if (element.pageNumber === i) {
                
                const content = document.getElementById(element.id);
                const canvas = await html2canvas(content as HTMLElement);
                const img = canvas.toDataURL("image/png", 1.0);
                const imgHeight = canvas.height * imgWidth / canvas.width;
                doc.addImage(img, 'PNG', margin, yPosition, imgWidth, imgHeight);
                yPosition += imgHeight+5;

                console.log('image added');
            }

        }
        console.log('page added');

        if (i !== totalPages)
            doc.addPage();

    }    
    return doc;
}

export const generatepdfnew = async (id: string): Promise<jsPDF | null> => {
    const pdf = new jsPDF("p", "mm", "a4");
    const content2 = document.getElementById('formContent');
    //const canvas2 = await html2canvas(content2 as HTMLElement);
    //const imgData = canvas2.toDataURL('image/png');

   
    
             const canvas = await html2canvas(content2 as HTMLElement);
            const img = canvas.toDataURL("image/png", 1.0);
            let w =  canvas.width;
            const actw = canvas.width;
            let h = canvas.height;
    const acth = canvas.height;

    let margin = 20;
            
            let width = pdf.internal.pageSize.width;
            let maxWidth = pdf.internal.pageSize.width;
            let height = pdf.internal.pageSize.height - 50;
            let maxHeight = pdf.internal.pageSize.height - 50;
            if (!maxWidth) maxWidth = width;
            if (!maxHeight) maxHeight = height;
            if (w > maxWidth) {
                w = maxWidth;
                h = Math.round(acth / actw * maxWidth);
    }



    const totalPages = Math.ceil(acth / height);
    let pageNumber = 1;

    const addHeaderFooter = (doc: jsPDF, pageNumber: number) => {
        //add header
        doc.setFontSize(10);
        doc.text('Notice of Driving Prohibition Application for Review', 15, 10);
        doc.setLineWidth(0.5);
        doc.line(15, 15, doc.internal.pageSize.getWidth() - 15, 15);

        //Add footer
        doc.text('Notice of Driving Prohibition Application for Review', 15, doc.internal.pageSize.getHeight() - 10);
        doc.text(`${pageNumber}/${totalPages}`, doc.internal.pageSize.getWidth() - 30, doc.internal.pageSize.getHeight() - 10);
        doc.line(15, doc.internal.pageSize.getHeight() - 20, doc.internal.pageSize.getWidth() - 15, doc.internal.pageSize.getHeight() - 20);
    }

    addHeaderFooter(pdf, 1);
            pdf.addImage(img, 'JPEG', 20, 20, w, height);
            let count = Math.ceil(h) / Math.ceil(maxHeight);
            count = Math.ceil(count);
            let position = 0;
            for (let i = 1; i <= count; i++) {
                position = -(maxHeight * i) + 20;
                alert(position);
                pdf.addPage();
                addHeaderFooter(pdf, ++pageNumber);
                pdf.addImage(img, 'JPEG', margin, position, w, height);
            }
            pdf.save("cart.pdf");
       

    return pdf;
        
   
}

export const generatemypdf = async (id: string) => {
    const doc = new jsPDF('p', 'mm');
    const content2 = document.getElementById('formContent');
    const canvas = await html2canvas(content2 as HTMLElement);
    const imgData = canvas.toDataURL('image/png');
    const imgWidth = 210;
    const pageHeight = doc.internal.pageSize.getHeight();
    const imgHeight = (canvas.height * imgWidth) / canvas.width;
    const totalPageSize = Math.ceil(imgHeight / pageHeight);
    let yPosition = 20;
    doc.setFontSize(10);
    doc.text('Notice of Driving Prohibition Application for Review', 15, 10);
    doc.setLineWidth(0.5);
    doc.line(15, 20, doc.internal.pageSize.getWidth() - 15, 20);
    doc.addImage(imgData, 'PNG', 15 , yPosition, imgWidth, imgHeight+60);

    for (let pageIndex = 1; pageIndex < totalPageSize; pageIndex++) {
        // making it negative to crop the image
        // and adding 10 because of the initial padding
        yPosition = pageIndex * pageHeight * -1 + 30 + 30; 
        console.log(yPosition);
        console.log(yPosition);
        console.log(yPosition);
        doc.setFontSize(10);
        doc.text('Notice of Driving Prohibition Application for Review', 15, 10);
        doc.setLineWidth(0.5);
        doc.line(15, 20, doc.internal.pageSize.getWidth() - 15, 20);
        doc.text('Notice of Driving Prohibition Application for Review', 15, doc.internal.pageSize.getHeight() - 10);
        doc.text(`${pageIndex}/${totalPageSize}`, doc.internal.pageSize.getWidth() - 30, doc.internal.pageSize.getHeight() - 10);
        doc.line(15, doc.internal.pageSize.getHeight() - 20, doc.internal.pageSize.getWidth() - 15, doc.internal.pageSize.getHeight() - 20);
        doc.addPage();
        doc.addImage(
            imgData,
            'PNG',
            15,
            yPosition,
            imgWidth,
            imgHeight
        );
    }

    doc.save('myfile.pdf');
    
}

export const generatePdf1 = () => {
    const doc = new jsPDF();

    const html = document.getElementById("formContent")?.innerText;

    //let split = doc.splitTextToSize(html as string, html?.length as number);
    //doc.text(split, 5, 20);
   // doc.output("dataurlnewwindow");

    const pdf = doc.html(html as string, { x: 0, y: -20, autoPaging: true, filename: 'output.pdf'  });
    pdf.outputPdf("dataurlnewwindow");

};


export const generatePDF = async (id: string): Promise<jsPDF | null> => {

        const content2 = document.getElementById(id);
        const canvas = await html2canvas(content2 as HTMLElement);
        const image = { type: 'jpeg', quality: 0.98 };
        const margin = [0.5, 0.5];

        let imgWidth = 8.5;
        let pageHeight = 11;

        let innerPageWidth = imgWidth - margin[0] * 2;
        let innerPageHeight = pageHeight - margin[1] * 2;

        // Calculate the number of pages.
        let pxFullHeight = canvas.height;
        let pxPageHeight = Math.floor(canvas.width * (pageHeight / imgWidth));
        let nPages = Math.ceil(pxFullHeight / pxPageHeight);

        // Define pageHeight separately so it can be trimmed on the final page.
        pageHeight = innerPageHeight;

        // Create a one-page canvas to split up the full image.
        let pageCanvas = document.createElement('canvas');
        let pageCtx = pageCanvas.getContext('2d');
        pageCanvas.width = canvas.width;
        pageCanvas.height = pxPageHeight;

        // Initialize the PDF.
        let pdf = new jsPDF('p', 'in', [8.5, 12]);

        for (let page = 0; page < nPages; page++) {
            // Trim the final page to reduce file size.
            if (page === nPages - 1 && pxFullHeight % pxPageHeight !== 0) {
                pageCanvas.height = pxFullHeight % pxPageHeight;
                pageHeight = (pageCanvas.height * innerPageWidth) / pageCanvas.width;
            }

            // Display the page.
            let w = pageCanvas.width;
            let h = pageCanvas.height;
            //pageCtx.fillStyle = 'white';
            pageCtx?.fillRect(0, 0, w, h);
            pageCtx?.drawImage(canvas, 0, page * pxPageHeight, w, h, 0, 0, w, h);

           

            // Add the page to the PDF.
            if (page > 0) pdf.addPage();
            //Add header and footer
            pdf.setFontSize(10);
            pdf.text('Notice of Driving Prohibition Application for Review', 15, 10);
            pdf.setLineWidth(0.5);
            pdf.line(15, 20, pdf.internal.pageSize.getWidth() - 15, 20);
            debugger;
            let imgData = pageCanvas.toDataURL('image/' + image.type, image.quality);
            pdf.addImage(imgData, image.type, margin[1], margin[0], innerPageWidth, pageHeight);
        }

       

    return pdf;
}


