package ca.bc.gov.open.pssg.rsbc.pdf.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.w3c.dom.Document;

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
		
        logger.info("APR PDF Generator received a message from the DF.pdf queue.");
        
        String noticeNumber = "unknown"; 
        
        logger.debug("RabbitMQListener received a message: " + noticeNumber);
        
        try {
        	
        	//STEP 1 - Extract and decode the XML form data from the JSON payload.  
			String xml = XMLParserDecoder.extractAndDecodeXml(message);
			
			//STEP 2 - Parse the XML form payload
			Document doc = XMLParserDecoder.getDocument(xml);
			
			noticeNumber = XmlUtilities.getNoticeNumber(doc);
			MDC.put("notice", noticeNumber);	        
	        
	        logger.info("Received a form payload for notice number: " + noticeNumber);
	        
	        //STEP 3 - Determine the form payload type. ONly allow form type 1 messages to be processed. 
	        FormType formType = XmlUtilities.categorizeFormType(doc);
	        
	        if (formType.equals(FormType.UNKNOWN) || formType.equals(FormType.f3)) {
	        	throw new UnsupportedXMLFormTypeException("RabbitMQListener: Form3 permutation or unknown XML content in JSON payload");
	        }
	        	
	        logger.info("XML form type identified as " + formType);
	        
        	//STEP 4 - Generate PDF and email body
        	PDFRenderResponse renderResp = pService.render(formType, xml, doc);
        	
        	//STEP 5 - Extract expected consent form data for form 1 types types 3 and 4. 
        	//String consentForm = null;
        	
        	//Consent form already in base64 format. 
// Consent form no longer held in the f1p3 or f1p4 XML form data.         	
//        	if (formType.equals(FormType.f1p3) || formType.equals(FormType.f1p4)) {
//        		consentForm = XmlUtilities.getConsentFormData(doc);
//        		if (null == consentForm || consentForm.length() == 0) {
//        			logger.info("No consent form attached.");
//        		}
//        	} 
        	
        	// EmailRequest req = aService.getEmailRequest(renderResp, doc, noticeNumber, consentForm);
        	EmailRequest req = aService.getEmailRequest(renderResp, doc, noticeNumber);
        	
        	//STEP 6 - Mail it!
        	ResponseEntity<EmailResponse> eResp = eService.sendEmail(req, noticeNumber);
        	if (!eResp.getStatusCode().is2xxSuccessful()) {
        		logger.error("Invalid status code returned when attempting to send mail for form.");
        	} else { 
        		logger.info("Email sent successfully for form.");
        	}
			
		} catch (Exception e) {
			
			// just consume unsupported XML Form type exceptions as we're not interested in these message types. 
			if (!(e instanceof UnsupportedXMLFormTypeException)) {
				logger.error("An exception occurred while generating a review submission form PDF and emailing, {}", e.getMessage());
				e.printStackTrace();
			} 
		}
        
        finally {
        	MDC.remove("notice");
        }
    }
}
