package ca.bc.gov.open.pssg.rsbc.pdf.service;

import org.springframework.stereotype.Service;
import org.w3c.dom.Document;

import ca.bc.gov.open.pssg.rsbc.pdf.component.AdobeOrdsProperties;
import ca.bc.gov.open.pssg.rsbc.pdf.exception.EmailTemplateServiceException;
import ca.bc.gov.open.pssg.rsbc.pdf.models.PDFRenderResponse;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities.FormType;


/**
 * 
 * Main PDF rendering service (e.g., called by controllers).
 * 
 * This service orchestrates:
 * 	
 * 	- Saving XML payload to the Adobe Schema Document Content table. 
 * 	- Capturing the returned pKey value.
 * 	- Use the returned pKey to render the desired version of the APR form.  
 * 
 */
@Service
public class PdfRenderService {
	
	private AdobeOrdsService oService;
	private AdobeReportServerService rService;
	private AdobeOrdsProperties props;
	private EmailTemplateService eService; 

	public PdfRenderService(AdobeOrdsService oService, AdobeReportServerService rService, EmailTemplateService eService, AdobeOrdsProperties props) {
		super();
		this.oService = oService;
		this.rService = rService;
		this.eService = eService;
		this.props = props;
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

	
	public PDFRenderResponse render(FormType type, Document doc) {
		
		//TODO - return here
		String email;
		try {
			email = eService.generateEmailHtml(type, doc);
			System.out.println(email);
		} catch (EmailTemplateServiceException e) {
			e.printStackTrace();
		}
	
		return null;
	} 
}
