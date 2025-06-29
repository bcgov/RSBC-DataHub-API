package ca.bc.gov.open.pssg.rsbc.pdf.service;

import org.springframework.stereotype.Service;

import ca.bc.gov.open.pssg.rsbc.pdf.component.AdobeOrdsProperties;
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

	public PdfRenderService(AdobeOrdsService oService, AdobeReportServerService rService, AdobeOrdsProperties props) {
		super();
		this.oService = oService;
		this.rService = rService;
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

	public PDFRenderResponse render(FormType type, String xml) {
		return null; 
		//TODO - continue here. 
	} 

}
