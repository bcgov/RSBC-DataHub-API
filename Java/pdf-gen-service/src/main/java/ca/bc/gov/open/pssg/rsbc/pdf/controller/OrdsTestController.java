package ca.bc.gov.open.pssg.rsbc.pdf.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import ca.bc.gov.open.pssg.rsbc.pdf.service.AdobeOrdsService;

@RestController
public class OrdsTestController {
	
	private static final Logger logger = LoggerFactory.getLogger(OrdsTestController.class);
	
	private AdobeOrdsService service;  
	
	public OrdsTestController (AdobeOrdsService service) {
		this.service = service; 
	}
	
    public AdobeOrdsService getService() {
		return service;
	}

	@GetMapping("/ordstest")
    public ResponseEntity<String> ordsTest() {
		
    	logger.info("Heard a call to the ORDS test controller");
    	
    	String xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n"
    			+ "<library>\r\n"
    			+ "  <book>\r\n"
    			+ "    <title>The Wind in the Willows</title>\r\n"
    			+ "    <author>Kenneth Grahame</author>\r\n"
    			+ "    <year>1908</year>\r\n"
    			+ "  </book>\r\n"
    			+ "  <book>\r\n"
    			+ "    <title>1984</title>\r\n"
    			+ "    <author>George Orwell</author>\r\n"
    			+ "    <year>1949</year>\r\n"
    			+ "  </book>\r\n"
    			+ "</library>";
    	
    	return service.adobeSaveXML(xml);
       
    }
}


