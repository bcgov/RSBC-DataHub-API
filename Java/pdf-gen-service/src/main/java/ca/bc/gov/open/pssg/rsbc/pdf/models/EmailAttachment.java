package ca.bc.gov.open.pssg.rsbc.pdf.models;

public class EmailAttachment {

	private String filename;
	private String filecontents; // Base64-encoded
	
	public String getFilename() {
		return filename;
	}
	public void setFilename(String filename) {
		this.filename = filename;
	}
	public String getFilecontents() {
		return filecontents;
	}
	public void setFilecontents(String filecontents) {
		this.filecontents = filecontents;
	}

}
