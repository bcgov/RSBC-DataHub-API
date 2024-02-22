package ca.bc.gov.open.pssg.rsbc.controller;

import java.io.ByteArrayInputStream;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RestController;

import ca.bc.gov.open.pssg.rsbc.api.AvscanApi;
import ca.bc.gov.open.pssg.rsbc.api.model.AvscanRequest;
import ca.bc.gov.open.pssg.rsbc.api.model.AvscanResponse;
import ca.bc.gov.open.pssg.rsbc.exception.VirusDetectedException;
import ca.bc.gov.open.pssg.rsbc.service.ClamAvService;

@RestController
public class AvscanControllerImpl implements AvscanApi {

	Logger logger = LoggerFactory.getLogger(AvscanControllerImpl.class);

	@Autowired
	ClamAvService clamAvService;
	
	@Override
	public ResponseEntity<AvscanResponse> avscanPost(AvscanRequest avscanRequest) {
		
		ResponseEntity<AvscanResponse> response = new ResponseEntity<AvscanResponse>(new AvscanResponse(), HttpStatus.ACCEPTED);		
		ByteArrayInputStream bis = new ByteArrayInputStream(avscanRequest.getDocument());
		
		try {
			clamAvService.scan(bis);
			response.getBody().setAcknowledge(true);
		} catch (VirusDetectedException e) {
			response.getBody().setAcknowledge(false);
		}
		
		return response;
	}
	
}
