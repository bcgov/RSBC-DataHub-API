package ca.bc.gov.open.pssg.rsbc.pdf.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Recover;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;

import ca.bc.gov.open.pssg.rsbc.pdf.component.AdobeOrdsProperties;

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
	 * 
	 */
	public AdobeOrdsService(AdobeOrdsProperties adobeOrdsProperties) {
		this.adobeOrdsProperties = adobeOrdsProperties;
		this.restTemplate = new RestTemplateBuilder().basicAuthentication(adobeOrdsProperties.getOrds().getAuth().getUsername(),
				adobeOrdsProperties.getOrds().getAuth().getPassword()).build();
	}

	/**
	 * 
	 * adobeSaveXML - Sets XML payload in the Adobe Schema Document Content table.
	 * 
	 * @param xmlPayload
	 * @return
	 */
	@Retryable(retryFor = { HttpServerErrorException.class,
			ResourceAccessException.class }, maxAttempts = 5, backoff = @Backoff(delay = 10000))
	public ResponseEntity<String> adobeSaveXML(String xmlPayload) {

		HttpHeaders headers = new HttpHeaders();
		headers.setContentType(MediaType.MULTIPART_FORM_DATA);

		MultiValueMap<String, Object> formData = new LinkedMultiValueMap<>();
		formData.add("documentContentText", xmlPayload);

		HttpEntity<MultiValueMap<String, Object>> request = new HttpEntity<>(formData, headers);

		logger.info("Sending XML payload to Adobe ORDS endpoint: {}",
				adobeOrdsProperties.getOrds().getBaseUrl() + "adobesavexml");

		ResponseEntity<String> response = restTemplate.postForEntity(adobeOrdsProperties.getOrds().getBaseUrl() + "adobesavexml",
				request, String.class);

		logger.info("Received response with status: {}", response.getStatusCode());
		return response;
	}

	@Recover
	private ResponseEntity<String> recover(ResourceAccessException ex, String xmlPayload) {
		logger.error("Connection issue—retries exhausted: {}", ex.getMessage(), ex);
		return new ResponseEntity<>("Unable to connect to Adobe ORDS after retries.", HttpStatus.SERVICE_UNAVAILABLE);
	}

	@Recover
	private ResponseEntity<String> recover(HttpServerErrorException ex, String xmlPayload) {
		logger.error("Server error—retries exhausted: {} - {}", ex.getStatusCode(), ex.getResponseBodyAsString(), ex);
		return new ResponseEntity<>(ex.getResponseBodyAsString(), ex.getStatusCode());
	}

}
