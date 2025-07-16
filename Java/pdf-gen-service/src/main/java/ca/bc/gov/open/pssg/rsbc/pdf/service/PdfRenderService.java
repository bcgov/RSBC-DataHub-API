package ca.bc.gov.open.pssg.rsbc.pdf.service;

import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.w3c.dom.Document;

import ca.bc.gov.open.pssg.rsbc.pdf.component.AdobeOrdsProperties;
import ca.bc.gov.open.pssg.rsbc.pdf.exception.EmailTemplateServiceException;
import ca.bc.gov.open.pssg.rsbc.pdf.exception.PdfRenderServiceException;
import ca.bc.gov.open.pssg.rsbc.pdf.models.PDFRenderResponse;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities.FormType;

/**
 * 
 * Main PDF rendering service (e.g., called by controllers).
 * 
 * This service orchestrates:
 * 
 * - Saving XML payload to the Adobe Schema Document Content table. 
 * - Capturing the returned pKey value. 
 * - Use of the returned pKey to render the PDF of the form 1 version of APR form.
 * 
 */
@Service
public class PdfRenderService {

	private static final Logger logger = LoggerFactory.getLogger(PdfRenderService.class);

	private AdobeOrdsService oService;
	private AdobeReportServerService rService;
	private AdobeOrdsProperties props;
	private EmailTemplateService eService;
	private FileLoaderUtility fService;

	public PdfRenderService(AdobeOrdsService oService, AdobeReportServerService rService, EmailTemplateService eService,
			AdobeOrdsProperties props, FileLoaderUtility fService) {
		super();
		this.oService = oService;
		this.rService = rService;
		this.eService = eService;
		this.props = props;
		this.fService = fService;
	}

	public AdobeOrdsService getoService() {
		return oService;
	}

	public AdobeReportServerService getrService() {
		return rService;
	}

	public AdobeOrdsProperties getProps() {
		return props;
	}

	public FileLoaderUtility getfService() {
		return fService;
	}

	public PDFRenderResponse render(FormType type, String xml, Document doc) throws PdfRenderServiceException {

		PDFRenderResponse resp = new PDFRenderResponse();

		//STEP 1 - Store the XML in the Adobe Schema content table.
		String pKey = null; 
		logger.info("PdefRenderService, STEP 1. Store form XML...");
		
		ResponseEntity<String> oResp = oService.adobeSaveXML(xml);
		if (!oResp.getStatusCode().equals(HttpStatus.OK)) {
			throw new PdfRenderServiceException("Failure to store form 1 payload at the Adobe ORDS Schema. Invalid HttpStatus code: " + oResp.getStatusCode().toString()); 
		} else {
			JSONObject obj = new JSONObject(oResp.getBody());
			pKey = obj.getString("pKey");
			logger.debug("pKey value returned from Adobe ORDS call was {}.", pKey);
		}
		
		//STEP 2 - Render the PDF. 
		logger.info("PdefRenderService, STEP 2. Generate the PDF...");
		ResponseEntity<byte[]> rResp = rService.callReportServer(
				props.getAem().getReport().getServer().getAppId(), // AEM Report Server config name. 
				XmlUtilities.toXDPType(type).toString(), // XDP form type name. 
				pKey);
		if (!rResp.getStatusCode().equals(HttpStatus.OK)) {
			throw new PdfRenderServiceException("Failure to render PDF of form type: " + type.name() + " Invalid HttpStatus code: " + rResp.getStatusCode().toString());  
		} else {
			resp.setPdf(rResp.getBody());
			logger.debug("Pdf returned from AEM Report server. Size: {} bytes.", resp.getPdf().length);
		}

		// STEP 3 - Render the applicant email.
		logger.info("PdefRenderService, STEP 3. Generating email from template...");
		
		if (!type.equals(FormType.f3)) {
			String email;
			try {
				email = eService.generateEmailHtml(type, doc);
				resp.setEmailBody(email);
			} catch (EmailTemplateServiceException e) {
				e.printStackTrace();
				throw new PdfRenderServiceException(e.getMessage(), e);
			}
		} else {
			resp.setEmailBody(null);
		}

		return resp;
	}
}
