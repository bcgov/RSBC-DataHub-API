package ca.bc.gov.open.pssg.rsbc.pdf.models;

import org.springframework.http.HttpStatus;

/**
 * 
 * Used for the PDF Rendering response from the Adobe Report Server. 
 * 
 */
public class PDFRenderResponse {

	private HttpStatus respCd;
	private byte[] pdf;

	public HttpStatus getRespCd() {
		return respCd;
	}

	public void setRespCd(HttpStatus respCd) {
		this.respCd = respCd;
	}

	public byte[] getPdf() {
		return pdf;
	}

	public void setPdf(byte[] pdf) {
		this.pdf = pdf;
	}
}
