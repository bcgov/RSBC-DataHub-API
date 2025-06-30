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
import ca.bc.gov.open.pssg.rsbc.pdf.exception.AdobeReportServerException;

/**
 * 
 * Provides access to AEM Report Server operations for PDF rendering.
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
	 * callReportServer - Renders a PDF. 
	 * 
	 * @param configName
	 * @param XdpName
	 * @param pKey
	 * @return
	 * @throws AdobeReportServerException
	 */
	@Retryable(retryFor = { 
			HttpClientErrorException.class,
            HttpServerErrorException.class,
            ResourceAccessException.class}, maxAttempts = 5, backoff = @Backoff(delay = 10000))
	public ResponseEntity<byte[]> callReportServer(String configName, String XdpName, String pKey) throws AdobeReportServerException {

		// Create the Adobe Report Server url
		String url = UriComponentsBuilder.fromUriString(adobeOrdsProperties.getAem().getReport().getServer().getUrl())
				.queryParam("param1", XdpName).queryParam("param2", pKey).queryParam("param3", configName)
				.queryParam("document_format", "pdfa").toUriString();

		logger.info("Requesting a PDF from the AEM Report Server endpoint of: {}", url);

		// Requesting binary data (PDF)
		return restTemplate.getForEntity(url, byte[].class);
	}
	
	// 4xx
    @Recover
    public ResponseEntity<byte[]> recover(HttpClientErrorException ex, String configName, String XdpName, String pKey) {
    	logger.error("Server error—retries exhausted when accessing {} {} - {}", ex.getStatusCode(), ex.getResponseBodyAsString(), ex);
    	return new ResponseEntity<>("Retries exhausted attempting to call the Adobe Report Server".getBytes(), HttpStatus.BAD_REQUEST);
    }

    
    //5xx
	@Recover
	private ResponseEntity<byte[]> recover(HttpServerErrorException ex, String configName, String XdpName, String pKey) {
		logger.error("Server error—retries exhausted: {}", ex);
		return new ResponseEntity<>("Retries exhausted attempting to call the Adobe Report Server".getBytes(), HttpStatus.INTERNAL_SERVER_ERROR);
	}
	
	// I/O errors - connection time out, etc. No logical status code for this situation. 
	@Recover
	private ResponseEntity<byte[]> recover(ResourceAccessException ex, String configName, String XdpName, String pKey) {
		logger.error("Server error—retries exhausted: {}", ex);
		return new ResponseEntity<>("Adobe Report Server endpoint unavailable".getBytes(), null);
	}

}
