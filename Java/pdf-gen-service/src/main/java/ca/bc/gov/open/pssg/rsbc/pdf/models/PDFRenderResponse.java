package ca.bc.gov.open.pssg.rsbc.pdf.models;

/**
 * 
 * Used for the PDF Rendering response from the Adobe Report Server. 
 * 
 */
public class PDFRenderResponse {

	private byte[] pdf;
	private String emailBody; 

	public byte[] getPdf() {
		return pdf;
	}

	public void setPdf(byte[] pdf) {
		this.pdf = pdf;
	}

	public String getEmailBody() {
		return emailBody;
	}

	public void setEmailBody(String emailBody) {
		this.emailBody = emailBody;
	}

}
