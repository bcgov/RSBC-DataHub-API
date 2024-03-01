package ca.bc.gov.open.pssg.rsbc.exception;

public class VirusDetectedException extends Exception {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 2852398311625734568L;
	
	private String details; 

    public VirusDetectedException(String message) { super(message); }
    
    public VirusDetectedException(String message, String details) { 
    	super(message); 
    	this.setDetails(details); 
    }

	public String getDetails() {
		return details;
	}

	public void setDetails(String details) {
		this.details = details;
	}

}
