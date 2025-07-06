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
import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailRequest;
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
	private PdfRenderService pService;
	private EmailClientService eService; 
	private EmailAssemblyService aService;
	
	public RabbitMQListener(XMLParserDecoder xmlDecoder, 
			PdfRenderService pService, 
			EmailClientService eService,
			EmailAssemblyService aService) {
		super();
		this.xmlDecoder = xmlDecoder;
		this.pService = pService;
		this.eService = eService;
		this.aService = aService; 
	}

	public XMLParserDecoder getXmlDecoder() {
		return xmlDecoder;
	}

	public PdfRenderService getpService() {
		return pService;
	}

	public EmailClientService geteService() {
		return eService;
	}

	@RabbitListener(queues = "DF.pdf")
    public void receiveMessage(String message) {
		
        logger.info("APR PDF Generator received a message from the DF.pdf queue.");
        
        String noticeNumber = "unknown"; 
        
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
	       
	        //STEP 3 - Determine the form payload type. 
	        noticeNumber = XmlUtilities.getNoticeNumber(doc);
	        FormType formType = XmlUtilities.categorizeFormType(doc);
	        
	        if (formType.equals(FormType.UNKNOWN) || !formType.equals(FormType.f3)) {
	        	throw new UnsupportedXMLFormTypeException("Unknown XML for type content in JSON payload for notice: " + noticeNumber);
	        }
	        	
	        logger.info("XML form type identified as " + formType);
	        
        	//STEP 4 - Generate PDF and email body
        	PDFRenderResponse renderResp = pService.render(formType, _xml, doc);
        	
        	//STEP 5 - Extract consent form data form1 types types 3 and 4. Should be found 
        	String consentForm = null;
        	//in the XML document already in base64. 
        	if (formType.equals(FormType.f1p3) || formType.equals(FormType.f1p4)) {
        		consentForm = XmlUtilities.getConsentFormData(doc); 
        	} 
        	
        	EmailRequest req = aService.getEmailRequest(renderResp, doc, noticeNumber, consentForm);
        	
        	//STEP 7 - Mail it!
        	eService.sendEmail(req, noticeNumber);	
			
		} catch (Exception e) {
			logger.error("An exception occurred while generating an applcant PDF and email for Notice Number {}, {}", noticeNumber, e.getMessage());
			e.printStackTrace();
		}
    }
}
