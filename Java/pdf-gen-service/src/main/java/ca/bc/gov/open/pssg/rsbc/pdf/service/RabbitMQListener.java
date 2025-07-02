package ca.bc.gov.open.pssg.rsbc.pdf.service;

import java.io.StringReader;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Service;
import org.w3c.dom.Document;
import org.xml.sax.InputSource;

import ca.bc.gov.open.pssg.rsbc.pdf.exception.UnsupportedXMLFormTypeException;
import ca.bc.gov.open.pssg.rsbc.pdf.models.PDFRenderResponse;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities.FormType;

/**
 * 
 * Receives message from DF.pdf queue, renders form and mails.
 * 
 * This listener should only be receiving Form 1 type requests. 
 * 
 * Form 3 requests should be received via the HTTP Listener class. 
 * 
 */
@Service
public class RabbitMQListener {

	private static final Logger logger = LoggerFactory.getLogger(RabbitMQListener.class);
	
	private XMLParserDecoder xmlDecoder; 
	private PdfRenderService renderer;
	
	public RabbitMQListener(XMLParserDecoder xmlDecoder, PdfRenderService renderer) {
		super();
		this.xmlDecoder = xmlDecoder;
		this.renderer = renderer;
	}

	public XMLParserDecoder getXmlDecoder() {
		return xmlDecoder;
	}

	public PdfRenderService getRenderer() {
		return renderer;
	}

	@RabbitListener(queues = "DF.pdf")
    public void receiveMessage(String message) {
		
        logger.info("APR PDF Generator received a message from the DF.pdf queue.");
        
        String noticeNumber = null; 
        
        try {
        	
        	//STEP 1 - Extract and decode the XML form data from the JSON payload.  
			String xml = XMLParserDecoder.extractAndDecodeXml(message);
			
			//STEP 2 - Parse the XML form payload
			DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
	        dbFactory.setNamespaceAware(false);
	       
	        DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
	        String _xml = XmlUtilities.formatXml(xml);
	        InputSource is = new InputSource(new StringReader(_xml));
	        Document doc = dBuilder.parse(is);

	        //STEP 3 - Categorize the XML form payload 
	        noticeNumber = XmlUtilities.getNoticeNumber(doc);
	        FormType formType = XmlUtilities.categorizeFormType(doc);
	        
	       
	        if (formType.equals(FormType.UNKNOWN) || !formType.equals(FormType.f3)) {
	        	throw new UnsupportedXMLFormTypeException("Unknown XML for type content in JSON payload.");
	        }
	        	
	        logger.info("XML form type identified as " + formType);
	        
        	//STEPS 4 generate PDF and email body
        	PDFRenderResponse resp = renderer.render(formType, _xml, doc);
        	System.out.println(resp.getEmailBody());
	        	
        	//STEP 5 mail the PDF to the applicant 
	        	
			
		} catch (Exception e) {
			logger.error("An exception occurred while generating an applcant PDF and email for Notice Number {}, {}", noticeNumber, e.getMessage());
			e.printStackTrace();
		}
    }
}
