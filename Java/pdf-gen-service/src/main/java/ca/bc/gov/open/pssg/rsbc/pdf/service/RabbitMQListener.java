package ca.bc.gov.open.pssg.rsbc.pdf.service;

import java.io.StringReader;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.w3c.dom.Document;
import org.xml.sax.InputSource;

import ca.bc.gov.open.pssg.rsbc.pdf.exception.EmailRequestAssemblyException;
import ca.bc.gov.open.pssg.rsbc.pdf.exception.UnsupportedXMLFormTypeException;
import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailRequest;
import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailResponse;
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
		
        logger.info("RabbitMQListener: APR PDF Generator received a message from the DF.pdf queue.");
        
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
	        MDC.put("notice", noticeNumber);	        
	        
	        logger.info("Received a form 1 payload for notice number: " + noticeNumber);
	        
	        FormType formType = XmlUtilities.categorizeFormType(doc);
	        
	        if (formType.equals(FormType.UNKNOWN) || formType.equals(FormType.f3)) {
	        	throw new UnsupportedXMLFormTypeException("RabbitMQListener: Form3 or unknown XML for type content in JSON payload for notice: " + noticeNumber);
	        }
	        	
	        logger.info("XML form type identified as " + formType);
	        
        	//STEP 4 - Generate PDF and email body
        	PDFRenderResponse renderResp = pService.render(formType, _xml, doc);
        	
        	//STEP 5 - Extract expected consent form data for form 1 types types 3 and 4. 
        	String consentForm = null;
        	
        	//Consent form already in base64 format.  
        	if (formType.equals(FormType.f1p3) || formType.equals(FormType.f1p4)) {
        		consentForm = XmlUtilities.getConsentFormData(doc);
        		if (null == consentForm) {
        			throw new EmailRequestAssemblyException("Error creating email message. No consent form attachment found.");
        		}
        	} 
        	
        	EmailRequest req = aService.getEmailRequest(renderResp, doc, noticeNumber, consentForm);
        	
        	//STEP 7 - Mail it!
        	ResponseEntity<EmailResponse> eResp = eService.sendEmail(req, noticeNumber);
        	if (!eResp.getStatusCode().is2xxSuccessful()) {
        		logger.error("Invalid status code returned when attempting to send mail for form 1.");
        	} else { 
        		logger.info("Email sent successfully for form 1.");
        	}
			
		} catch (Exception e) {
			logger.error("An exception occurred while generating an applcant PDF and emailing, {}", e.getMessage());
			e.printStackTrace();
		}
        
        finally {
        	MDC.remove("notice");
        }
    }
}
