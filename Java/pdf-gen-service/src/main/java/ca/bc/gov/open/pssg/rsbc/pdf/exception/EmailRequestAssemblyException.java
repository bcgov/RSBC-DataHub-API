package ca.bc.gov.open.pssg.rsbc.pdf.exception;

public class EmailRequestAssemblyException extends Exception {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = -7819699561018828366L;

	public EmailRequestAssemblyException(String message, Throwable cause) {
        super(message, cause);
    }
	
	public EmailRequestAssemblyException(String message) {
        super(message);
    }

}
