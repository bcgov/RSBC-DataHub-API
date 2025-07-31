package ca.bc.gov.open.pssg.rsbc.pdf.controller;

import java.util.Base64;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.w3c.dom.Document;

import ca.bc.gov.open.pssg.rsbc.pdf.exception.UnsupportedXMLFormTypeException;
import ca.bc.gov.open.pssg.rsbc.pdf.models.PDFRenderResponse;
import ca.bc.gov.open.pssg.rsbc.pdf.service.PdfRenderService;
import ca.bc.gov.open.pssg.rsbc.pdf.service.XMLParserDecoder;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities.FormType;

/**
 * 
 * Excepts APR, XML Form 3 Payloads. Returns PDF rendering as stream.
 * 
 * This is not a public service. Called only from the NextJS, server side. 
 * 
 */
@RestController
public class HttpListener {

	private static final Logger logger = LoggerFactory.getLogger(HttpListener.class);

	private PdfRenderService pService;

	public HttpListener(PdfRenderService pService) {
		super();
		this.pService = pService;
	}

	public PdfRenderService getpService() {
		return pService;
	}

	@PostMapping("/renderpdf")
	public ResponseEntity<?> renderPdf(@RequestBody String base64XmlPayload) {

		String noticeNumber = "unknown";

		try {

			logger.info("APR PDF Generator received a payload at the HttpListener.");
			
			if (base64XmlPayload == null) {
	            return ResponseEntity
	            	.status(HttpStatus.BAD_REQUEST)
	            	.contentType(MediaType.TEXT_PLAIN)
	                .body("Request body cannot be null");
	        }

			// STEP 1 - Decode the incoming XML payload content
			byte[] decodedBytes = Base64.getDecoder().decode(base64XmlPayload);
			String xml = new String(decodedBytes);

			// STEP 2 - Load a Document from the incoming XML form payload			
			Document doc = XMLParserDecoder.getDocument(xml);
			
			noticeNumber = XmlUtilities.getNoticeNumber(doc);
			MDC.put("notice", noticeNumber);

			logger.info("Received a form payload for notice number: " + noticeNumber);
			
	        //STEP 3 - Ensure this is a form type 3 payload. 
	        FormType formType = XmlUtilities.categorizeFormType(doc);
	        
	        if (formType.equals(FormType.UNKNOWN) || !formType.equals(FormType.f3)) {
	        	throw new UnsupportedXMLFormTypeException("HttpListener: XML form content not the expected Form 3 type.");
	        }
			
	        logger.info("XML form type identified as " + formType);
	        
	        //STEP 4 - Generate PDF and stream
        	PDFRenderResponse renderResp = pService.render(formType, xml, doc);
        	
            byte[] pdfBytes = renderResp.getPdf();

            return ResponseEntity.ok()
                        .header(HttpHeaders.CONTENT_DISPOSITION, "inline; filename=evidence.pdf")
                        .contentType(MediaType.APPLICATION_PDF)
                        .body(pdfBytes);

		} catch (Exception e) {
			
			String err = "An exception occurred while consuming the XML payload form form 3: " + e.getMessage();
			logger.error(err);
			e.printStackTrace();
			
			return ResponseEntity
			        .status(HttpStatus.INTERNAL_SERVER_ERROR)
			        .contentType(MediaType.TEXT_PLAIN)
			        .body(e.getMessage().getBytes());
		}

		finally {
			MDC.remove("notice");
		}
	}
}


