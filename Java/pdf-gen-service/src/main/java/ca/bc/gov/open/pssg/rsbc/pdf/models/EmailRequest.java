package ca.bc.gov.open.pssg.rsbc.pdf.models;

import java.util.List;

public class EmailRequest {
	
	private EmailObject from;
	private List<EmailObject> to;
	private List<EmailObject> cc;
	private List<EmailObject> bcc;
	private String subject;
	private EmailContent content;
	private List<EmailAttachment> attachment;

	public EmailObject getFrom() {
		return from;
	}

	public void setFrom(EmailObject from) {
		this.from = from;
	}

	public List<EmailObject> getTo() {
		return to;
	}

	public void setTo(List<EmailObject> to) {
		this.to = to;
	}

	public List<EmailObject> getCc() {
		return cc;
	}

	public void setCc(List<EmailObject> cc) {
		this.cc = cc;
	}

	public List<EmailObject> getBcc() {
		return bcc;
	}

	public void setBcc(List<EmailObject> bcc) {
		this.bcc = bcc;
	}

	public String getSubject() {
		return subject;
	}

	public void setSubject(String subject) {
		this.subject = subject;
	}

	public EmailContent getContent() {
		return content;
	}

	public void setContent(EmailContent content) {
		this.content = content;
	}

	public List<EmailAttachment> getAttachment() {
		return attachment;
	}

	public void setAttachment(List<EmailAttachment> attachment) {
		this.attachment = attachment;
	}

}
