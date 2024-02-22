package ca.bc.gov.open.pssg.rsbc.controller;

import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RestController;

import ca.bc.gov.open.pssg.rsbc.api.PingApi;
import ca.bc.gov.open.pssg.rsbc.service.ClamAvService;

@RestController
public class PingControllerImpl implements PingApi {

	Logger logger = LoggerFactory.getLogger(PingControllerImpl.class);

	@Autowired
	ClamAvService clamAvService;
	
	 /**
     * GET /ping : Utility operation to check back end connectivity
     * Utility operation to check back end connectivity
     *
     * @return Ping Response (status code 200)
     * @see PingApi#ping
     */
	@Override
    public ResponseEntity<String> pingGet() {
		
		ResponseEntity<String> response = null; 
		
		try {
			if (clamAvService.ping()) {
				response = ResponseEntity
					.status(HttpStatus.OK)
					.body("ClamAv ping response: Success");
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
