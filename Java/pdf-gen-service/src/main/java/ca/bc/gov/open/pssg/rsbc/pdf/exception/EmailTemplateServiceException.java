package ca.bc.gov.open.pssg.rsbc.pdf.exception;

public class EmailTemplateServiceException extends Exception {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -7819699561018828366L;

	public EmailTemplateServiceException(String message, Throwable cause) {
        super(message, cause);
    }
	
	public EmailTemplateServiceException(String message) {
        super(message);
    }

}
