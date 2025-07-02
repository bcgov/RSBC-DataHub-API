package ca.bc.gov.open.pssg.rsbc.pdf.exception;

public class PdfRenderServiceException extends Exception {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -7819699561018828366L;

	public PdfRenderServiceException(String message, Throwable cause) {
        super(message, cause);
    }
	
	public PdfRenderServiceException(String message) {
        super(message);
    }

}
