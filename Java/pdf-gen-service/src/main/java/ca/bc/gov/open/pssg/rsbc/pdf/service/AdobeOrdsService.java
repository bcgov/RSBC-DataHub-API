package ca.bc.gov.open.pssg.rsbc.pdf.service;



import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;

import ca.bc.gov.open.pssg.rsbc.pdf.component.AdobeOrdsProperties;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * 
 * Provides access to Adobe ORDs operations. 
 * 
 */
@Service
public class AdobeOrdsService {
	
	private static final Logger logger = LoggerFactory.getLogger(AdobeOrdsService.class);

    private final RestTemplate restTemplate;
    private final AdobeOrdsProperties adobeOrdsProperties;
    
    /**
     * 
     * Service Constructor 
     * 
     * @param adobeOrdsProperties
     * @param restTemplate
     */
    public AdobeOrdsService(AdobeOrdsProperties adobeOrdsProperties, RestTemplate restTemplate) {
        this.adobeOrdsProperties = adobeOrdsProperties;
        this.restTemplate = new RestTemplateBuilder()
                .basicAuthentication(
                    adobeOrdsProperties.getAuth().getUsername(), 
                    adobeOrdsProperties.getAuth().getPassword()
                )
                .build();
    }

    /**
     * 
     * adobeSaveXML - Sets XML payload in the Adobe Schema Document Content table. 
     * 
     * @param xmlPayload
     * @return
     */
    public ResponseEntity<String> adobeSaveXML(String xmlPayload) {
        
    	HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_XML);
        HttpEntity<String> request = new HttpEntity<>(xmlPayload, headers);

        try {
            logger.info("Sending XML payload to Adobe ORDS endpoint: {}", adobeOrdsProperties.getUrl());
            ResponseEntity<String> response = restTemplate.postForEntity(
                adobeOrdsProperties.getUrl(), request, String.class);
            logger.info("Received response with status: {}", response.getStatusCode());
            return response;
        } catch (HttpClientErrorException | HttpServerErrorException ex) {
            logger.error("HTTP error occurred: {} - {}", ex.getStatusCode(), ex.getResponseBodyAsString(), ex);
            return new ResponseEntity<>(ex.getResponseBodyAsString(), ex.getStatusCode());
        } catch (ResourceAccessException ex) {
            logger.error("Resource access error (possibly timeout or connection issue with the Adobe ORDS ): {}", ex.getMessage(), ex);
            return new ResponseEntity<>("Unable to connect to the Adobe ORDS service.", HttpStatus.SERVICE_UNAVAILABLE);
        } catch (Exception ex) {
            logger.error("Unexpected error occurred while calling Adobe ORDS service", ex);
            return new ResponseEntity<>("Internal server error", HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}
