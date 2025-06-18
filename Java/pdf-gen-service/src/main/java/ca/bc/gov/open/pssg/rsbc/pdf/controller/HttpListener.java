package ca.bc.gov.open.pssg.rsbc.pdf.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HttpListener {
	
	private static final Logger logger = LoggerFactory.getLogger(HttpListener.class);

    @PostMapping("/renderpdf")
    public String renderPdf(@RequestBody String message) {
    	
        logger.info("APR PDF Generator received a message from the HTTP Listener: " + message);
        return "ok";
    }
}


