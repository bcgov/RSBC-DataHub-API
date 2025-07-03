package ca.bc.gov.open.pssg.rsbc.pdf.controller;

import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import ca.bc.gov.open.pssg.rsbc.pdf.exception.AdobeReportServerException;
import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailContent;
import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailObject;
import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailRequest;
import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailResponse;
import ca.bc.gov.open.pssg.rsbc.pdf.service.EmailClientService;

@RestController
public class EmailTestController {
	
	private static final Logger logger = LoggerFactory.getLogger(EmailTestController.class);
	
	private EmailClientService service;  
	
	public EmailTestController (EmailClientService service) {
		this.service = service; 
	}

	@GetMapping("/mailtest")
    public ResponseEntity<EmailResponse> ordsTest() throws AdobeReportServerException {
		
    	logger.info("Heard a call to the Mail It AEM test controller");
    	
    	EmailRequest er = new EmailRequest();
    	
    	er.setSubject("This is a test email from the PDF Gen controller");
    	
    	//From
    	EmailObject eoFrom  = new EmailObject();
    	eoFrom.setEmail("form.handler.application@gov.bc.ca");
    	er.setFrom(eoFrom);
    	
    	//To 
    	List<EmailObject> eoTos = new ArrayList<EmailObject>();
    	EmailObject eoTo  = new EmailObject();
    	eoTo.setEmail("shaunmillaris@gmail.com");
    	eoTos.add(eoTo);
    	
    	er.setTo(eoTos);
    	
    	
    	EmailContent ec = new EmailContent(); 
    	ec.setType("text/html");
    	ec.setValue("<html>\r\n"
    			+ "<head>\r\n"
    			+ "  <title>Hello World Page</title>\r\n"
    			+ "</head>\r\n"
    			+ "<body>\r\n"
    			+ "  <h1>Hello, World!</h1>\r\n"
    			+ "</body>\r\n"
    			+ "</html>\r\n"
    			+ "\r\n");
    	
    	er.setContent(ec);
    	
    	return service.sendEmail(er, "21-013189");
       
    }
}


