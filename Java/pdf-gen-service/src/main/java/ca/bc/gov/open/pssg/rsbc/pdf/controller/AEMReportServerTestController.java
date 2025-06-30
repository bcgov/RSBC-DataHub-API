package ca.bc.gov.open.pssg.rsbc.pdf.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import ca.bc.gov.open.pssg.rsbc.pdf.exception.AdobeReportServerException;
import ca.bc.gov.open.pssg.rsbc.pdf.service.AdobeReportServerService;

@RestController
public class AEMReportServerTestController {
	
	private static final Logger logger = LoggerFactory.getLogger(AEMReportServerTestController.class);
	
	private AdobeReportServerService service;  
	
	public AEMReportServerTestController (AdobeReportServerService service) {
		this.service = service; 
	}
	
    public AdobeReportServerService getService() {
		return service;
	}

	@GetMapping("/aemtest")
    public ResponseEntity<byte[]> ordsTest() throws AdobeReportServerException {
		
    	logger.info("Heard a call to the AEM Report Server test controller");
    	
    	//TODO - switch this once the new XDPs have been installed. 
    	//return service.callReportServer("rsbc-apr-dev", "form1_p1", "key");
    	
    	return service.callReportServer("justindev", "PCR014", "SHAUN_APR_DATA");
       
    }
}


