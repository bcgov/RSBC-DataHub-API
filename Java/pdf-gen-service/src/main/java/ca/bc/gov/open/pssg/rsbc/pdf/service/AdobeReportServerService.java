package ca.bc.gov.open.pssg.rsbc.pdf.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Recover;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import ca.bc.gov.open.pssg.rsbc.pdf.component.AdobeOrdsProperties;

/**
 * 
 * Provides access to AEM Report Server operations.
 * 
 */
@Service
public class AdobeReportServerService {

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
	public AdobeReportServerService(AdobeOrdsProperties adobeOrdsProperties) {
		this.adobeOrdsProperties = adobeOrdsProperties;
		this.restTemplate = new RestTemplateBuilder().build();
	}

	/**
	 * 
	 * callReportServer - Calls AEM Report Server rto fetch PDF based on key and
	 * environmental config name.
	 * 
	 * @param xmlPayload
	 * @return
	 */
	@Retryable(retryFor = { HttpServerErrorException.class, ResourceAccessException.class,
			HttpClientErrorException.class }, maxAttempts = 5, backoff = @Backoff(delay = 10000))
	public ResponseEntity<byte[]> callReportServer(String configName, String XdpName, String pKey) {

		// Create the url
		String url = UriComponentsBuilder.fromUriString(adobeOrdsProperties.getAem().getReport().getServer().getUrl())
				.queryParam("param1", XdpName).queryParam("param2", pKey).queryParam("param3", configName)
				.queryParam("document_format", "pdfa").toUriString();

		logger.info("Requesting a PDF from the AEM Report Server endpoint: {}", url);

		// Requesting binary data (PDF)
		ResponseEntity<byte[]> response = restTemplate.getForEntity(url, byte[].class);

		logger.info("Received response with status: {}", response.getStatusCode());

		return response;
	}

	@Recover
	private ResponseEntity<String> recover(HttpClientErrorException ex) {
		if (ex instanceof HttpClientErrorException.BadRequest) {
			logger.error("BadRequest exception—retries exhausted: {}", ex.getMessage(), ex);
		} else {
			logger.error("Other client error—retries exhausted: {}", ex.getMessage(), ex);
		}
		return new ResponseEntity<>("Client error after retries.", HttpStatus.BAD_REQUEST);
	}

	@Recover
	private ResponseEntity<String> recover(ResourceAccessException ex) {
		logger.error("Connection issue—retries exhausted: {}", ex.getMessage(), ex);
		return new ResponseEntity<>("Unable to connect to Adobe Report Server after retries.",
				HttpStatus.SERVICE_UNAVAILABLE);
	}

	@Recover
	private ResponseEntity<String> recover(HttpServerErrorException ex) {
		logger.error("Server error—retries exhausted: {} - {}", ex.getStatusCode(), ex.getResponseBodyAsString(), ex);
		return new ResponseEntity<>(ex.getResponseBodyAsString(), ex.getStatusCode());
	}

}
