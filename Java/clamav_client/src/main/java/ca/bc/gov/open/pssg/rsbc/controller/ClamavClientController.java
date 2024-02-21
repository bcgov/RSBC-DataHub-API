package ca.bc.gov.open.pssg.rsbc.controller;

import ca.bc.gov.open.pssg.rsbc.config.AutoConfiguration;
import ca.bc.gov.open.pssg.rsbc.exception.VirusDetectedException;
import ca.bc.gov.open.pssg.rsbc.service.ClamAvService;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.InputStream;
import java.io.ByteArrayInputStream;
import java.io.IOException;

@RestController
public class ClamavClientController {

	Logger logger = LoggerFactory.getLogger(AutoConfiguration.class);

	@Autowired
	ClamAvService clamAvService;

	@GetMapping("/avscan")
	public String getAvScan() {

		//TODO - this needs to be update to receive a stream of bytes from the caller and 
		// return a simple true or false response. 
		String testString = "some text";
		InputStream inputStream = new ByteArrayInputStream(testString.getBytes());

		try {
			clamAvService.scan(inputStream);
			return "No Virus";
		} catch (VirusDetectedException e) {
			return "Virus Found";
		}

	}

	@GetMapping("/ping")
	public ResponseEntity<String> getPing() {
		
		ResponseEntity<String> response = null; 
		
		try {
			if (clamAvService.ping()) {
				response = ResponseEntity
					.status(HttpStatus.OK)
					.body("ClamAv Ping response: true");
			}
			
		} catch (IOException e) {
			e.printStackTrace();
			response = ResponseEntity
					.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body("Failure to connect to ClamAv server.");
		}
		
		return response;

	}

}
