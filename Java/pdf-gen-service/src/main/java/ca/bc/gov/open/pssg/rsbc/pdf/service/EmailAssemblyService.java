package ca.bc.gov.open.pssg.rsbc.pdf.service;

import java.util.ArrayList;
import java.util.Base64;
import java.util.List;

import org.springframework.stereotype.Service;
import org.w3c.dom.Document;

import ca.bc.gov.open.pssg.rsbc.pdf.component.MailItProperties;
import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailAttachment;
import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailContent;
import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailObject;
import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailRequest;
import ca.bc.gov.open.pssg.rsbc.pdf.models.PDFRenderResponse;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities;

@Service
public class EmailAssemblyService {

	private MailItProperties props;

	public EmailAssemblyService(MailItProperties props) {
		this.props = props;
	}

	public MailItProperties getProps() {
		return props;
	}

	/**
	 * Generates an Email Request Object
	 * 
	 * @param resp
	 * @param doc
	 * @param noticeNumber
	 * @param applicationForm
	 * @return
	 */
	public EmailRequest getEmailRequest(PDFRenderResponse resp, Document doc, String noticeNumber) {	

		EmailRequest er = new EmailRequest();
		er.setSubject("Copy of Application form - Driving Prohibition " + noticeNumber + " Review");

		// Set From
		EmailObject eoFrom = new EmailObject();
		eoFrom.setEmail(props.getFrom());
		er.setFrom(eoFrom);

		// Set To and BCCs
		List<EmailObject> eoTos = new ArrayList<EmailObject>();
		EmailObject eoTo1 = new EmailObject();
		eoTo1.setEmail(XmlUtilities.getApplicantEmailAddress(doc));
		eoTos.add(eoTo1);

		if (!"null".equals(props.getBcc1())) {
			EmailObject eoTo2 = new EmailObject();
			eoTo2.setEmail(props.getBcc1());
			eoTos.add(eoTo2);
		}

		if (!"null".equals(props.getBcc2())) {
			EmailObject eoTo3 = new EmailObject();
			eoTo3.setEmail(props.getBcc2());
			eoTos.add(eoTo3);
		}

		er.setTo(eoTos);

		List<EmailAttachment> attachments = new ArrayList<EmailAttachment>();

		// Add prohibition review form attachment
		if (resp.getPdf().length > 0) {
			EmailAttachment attachment = new EmailAttachment();
			attachment.setFilecontents(Base64.getEncoder().encodeToString(resp.getPdf()));
			attachment.setFilename("prohibition_document.pdf");
			attachments.add(attachment);
		}

// Consent form no longer held in the f1p3 or f1p4 XML form data.  		
//		// Add consent form (if available - assumed to already be b64 encoded) 
//		if ( null != consentForm && consentForm.length() > 0) {
//			EmailAttachment attachment = new EmailAttachment();
//			attachment.setFilecontents(consentForm);
//			attachment.setFilename("consent.pdf");
//			attachments.add(attachment);
//		} 

		er.setAttachment(attachments);

		EmailContent ec = new EmailContent();
		ec.setType("text/html");

		ec.setValue(resp.getEmailBody()); // html 

		er.setContent(ec);

		return er;

	}

}
