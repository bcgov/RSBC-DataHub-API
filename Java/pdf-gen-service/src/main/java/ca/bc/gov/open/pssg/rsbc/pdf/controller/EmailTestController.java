package ca.bc.gov.open.pssg.rsbc.pdf.controller;

import java.io.StringReader;
import java.util.ArrayList;
import java.util.List;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.w3c.dom.Document;
import org.xml.sax.InputSource;

import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailAttachment;
import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailContent;
import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailObject;
import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailRequest;
import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailResponse;
import ca.bc.gov.open.pssg.rsbc.pdf.service.EmailClientService;
import ca.bc.gov.open.pssg.rsbc.pdf.service.EmailTemplateService;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities.FormType;

@RestController
public class EmailTestController {
	
	String base64File = "JVBERi0xLjAKMSAwIG9iajw8L1R5cGUvQ2F0YWxvZy9QYWdlcyAyIDAgUj4+ZW5kb2JqIDIgMCBvYmo8PC9UeXBlL1BhZ2VzL0tpZHNbMyAwIFJdL0NvdW50IDE+PmVuZG9iaiAzIDAgb2JqPDwvVHlwZS9QYWdlL01lZGlhQm94WzAgMCAzIDNdPj5lbmRvYmoKeHJlZgowIDQKMDAwMDAwMDAwMCA2NTUzNSBmCjAwMDAwMDAwMTAgMDAwMDAgbgowMDAwMDAwMDUzIDAwMDAwIG4KMDAwMDAwMDEwMiAwMDAwMCBuCnRyYWlsZXI8PC9TaXplIDQvUm9vdCAxIDAgUj4+CnN0YXJ0eHJlZgoxNDkKJUVPRg==";
	String xmlDocument = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><form xmlns:fr=\"http://orbeon.org/oxf/xml/form-runner\" fr:data-format-version=\"4.0.0\"><submitted>false</submitted><before-you-begin-section><help-text/></before-you-begin-section><prohibition-information><control-prohibition-number>21-013185</control-prohibition-number><control-is-ul>false</control-is-ul><prohibition-number-clean>21013185</prohibition-number-clean><prohibition-no-image filename=\"Combo prohibition no.png\" mediatype=\"image/png\">/fr/service/persistence</prohibition-no-image><control-is-irp>true</control-is-irp><control-is-adp>false</control-is-adp><licence-seized>licence-seized</licence-seized><licence-not-surrendered/><licence-lost-or-stolen/><licence-not-issued/><irp-prohibition-type-length>30-days-warn</irp-prohibition-type-length><date-of-service>2025-06-19</date-of-service></prohibition-information><identification-information><applicant-information-label/><applicant-role-select>driver</applicant-role-select><represented-by-lawyer>no</represented-by-lawyer><applicant-role>driver</applicant-role><control-4/><consent-upload filename=\"\" mediatype=\"\" size=\"\"/><lawyer-information-label/><control-2/><first-name-applicant>Mark</first-name-applicant><last-name-applicant>Pelttest</last-name-applicant><applicant-phone-number>555-555-5555</applicant-phone-number><control-3/><applicant-email-address>shaun.millar@gov.bc.ca</applicant-email-address><appeals-registry-email>chinedu.anaekwe@gov.bc.ca</appeals-registry-email><email-bcc>shaun.millar@nttdata.com</email-bcc><applicant-email-confirm>shaun.millar@gov.bc.ca</applicant-email-confirm><do-not-reply-address>form.handler.application@gov.bc.ca</do-not-reply-address><driver-information-label/><driver-first-name/><driver-last-name/><driver-bcdl>01000020</driver-bcdl><address-label/><street-address>1234 Main</street-address><control-driver-city-town>Victoria</control-driver-city-town><control-driver-province>british-columbia</control-driver-province><control-driver-postal-code>A1A1A1</control-driver-postal-code></identification-information><review-information><ul-burden-of-proof-text/><ul-grounds/><irp-burden-of-proof-text/><irp-grounds-list>0</irp-grounds-list><adp-burden-of-proof-text/><adp-grounds-alcohol/><adp-grounds-drugs/><adp-grounds-alcohol-drugs/><adp-grounds-drug-expert/><adp-grounds-refusal/><control-6>0</control-6><preparing-for-your-review/><preparing-for-review-irp-text/><preparing-for-review-ul-text/><hearing-request-type>written</hearing-request-type><wirtten-review-information/><oral-review-instructions/></review-information><consent-and-submission><signature-applicant-name/><date-signed>2025-06-19-07:00</date-signed><control-5/><form-submit-text/></consent-and-submission></form>";
	
	private static final Logger logger = LoggerFactory.getLogger(EmailTestController.class);
	
	private EmailClientService mService; 
	private EmailTemplateService tService; 
	
	public EmailTestController (EmailClientService mService, EmailTemplateService tService) {
		this.mService = mService;
		this.tService = tService; 
	}
	
	public EmailClientService geteService() {
		return mService;
	}

	public EmailTemplateService gettService() {
		return tService;
	}

	@GetMapping("/mailtest")
    public ResponseEntity<EmailResponse> ordsTest() throws Exception {
		
    	logger.info("Heard a call to the Mail It AEM test controller");
    	
    	EmailRequest er = new EmailRequest();
    	
    	er.setSubject("This is a test email from the PDF Gen controller");
    	
    	//From
    	EmailObject eoFrom  = new EmailObject();
    	eoFrom.setEmail("form.handler.application@gov.bc.ca");
    	er.setFrom(eoFrom);
    	
    	//To 
    	List<EmailObject> eoTos = new ArrayList<EmailObject>();
    	EmailObject eoTo  = new EmailObject();
    	eoTo.setEmail("shaun.millar@gov.bc.ca");
    	eoTos.add(eoTo);
    	
    	er.setTo(eoTos);
    	
    	// add a simple, single attachment. 
    	List<EmailAttachment> attachments = new ArrayList<EmailAttachment>();
    	EmailAttachment attachment = new EmailAttachment();
    	attachment.setFilecontents(this.base64File);
    	attachment.setFilename("prohibition_document.pdf");
    	attachments.add(attachment);
    	
    	er.setAttachment(attachments);
    	
    	EmailContent ec = new EmailContent(); 
    	ec.setType("text/html");
    	
		DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
        dbFactory.setNamespaceAware(false);
       
        DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
        String _xml = XmlUtilities.formatXml(this.xmlDocument);
        InputSource is = new InputSource(new StringReader(_xml));
        Document doc = dBuilder.parse(is);
    	
    	ec.setValue(tService.generateEmailHtml(FormType.f1p1, doc));
    	
    	er.setContent(ec);
    	
    	return mService.sendEmail(er, "21-013185");
       
    }
}


