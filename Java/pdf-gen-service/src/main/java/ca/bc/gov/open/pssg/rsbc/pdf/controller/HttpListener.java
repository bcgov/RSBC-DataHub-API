package ca.bc.gov.open.pssg.rsbc.pdf.controller;

import java.io.StringReader;
import java.util.Base64;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

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
import org.xml.sax.InputSource;

import ca.bc.gov.open.pssg.rsbc.pdf.exception.UnsupportedXMLFormTypeException;
import ca.bc.gov.open.pssg.rsbc.pdf.models.PDFRenderResponse;
import ca.bc.gov.open.pssg.rsbc.pdf.service.EmailAssemblyService;
import ca.bc.gov.open.pssg.rsbc.pdf.service.EmailClientService;
import ca.bc.gov.open.pssg.rsbc.pdf.service.PdfRenderService;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities.FormType;

/**
 * 
 * Excepts APR, XML Form 3 Payloads. Returns PDF rendering as stream.
 * 
 */
@RestController
public class HttpListener {

	private static final Logger logger = LoggerFactory.getLogger(HttpListener.class);

	private PdfRenderService pService;
	private EmailAssemblyService aService;
	private EmailClientService eService;

	public HttpListener(PdfRenderService pService, EmailAssemblyService aService, EmailClientService eService) {
		super();
		this.pService = pService;
		this.aService = aService;
		this.eService = eService;
	}

	public PdfRenderService getpService() {
		return pService;
	}

	public EmailAssemblyService getaService() {
		return aService;
	}

	public EmailClientService geteService() {
		return eService;
	}

	@PostMapping("/renderpdf")
	public ResponseEntity<byte[]> renderPdf(@RequestBody String base64XmlPayload) {

		String noticeNumber = "unknown";

		try {

			logger.info("APR PDF Generator received a payload at the HttpListener.");

			// STEP 1 - Decode the incoming XML payload content
			byte[] decodedBytes = Base64.getDecoder().decode(base64XmlPayload);
			String xml = new String(decodedBytes);

			// STEP 2 - Parse the XML form payload
			DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
			dbFactory.setNamespaceAware(false);

			DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
			String _xml = XmlUtilities.formatXml(xml);
			InputSource is = new InputSource(new StringReader(_xml));
			Document doc = dBuilder.parse(is);

			noticeNumber = XmlUtilities.getNoticeNumber(doc);
			MDC.put("notice", noticeNumber);

			logger.info("Received a form payload for notice number: " + noticeNumber);
			
	        //STEP 3 - Ensure this is a form type 3 payload. 
	        FormType formType = XmlUtilities.categorizeFormType(doc);
	        
	        if (formType.equals(FormType.UNKNOWN) && !formType.equals(FormType.f3)) {
	        	throw new UnsupportedXMLFormTypeException("HttpListener: XML form content not the expected Form 3 type.");
	        }
			
	        logger.info("XML form type identified as " + formType);
	        
	        //STEP 4 - Generate PDF and stream
        	PDFRenderResponse renderResp = pService.render(formType, _xml, doc);
        	
            byte[] pdfBytes = renderResp.getPdf();

            return ResponseEntity.ok()
                        .header(HttpHeaders.CONTENT_DISPOSITION, "inline; filename=apr_form3.pdf")
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


