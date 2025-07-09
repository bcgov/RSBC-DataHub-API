package ca.bc.gov.open.pssg.rsbc.pdf.service;

import java.nio.charset.StandardCharsets;
import java.util.Base64;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Recover;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.ResourceAccessException;

import ca.bc.gov.open.pssg.rsbc.pdf.component.MailItProperties;
import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailRequest;
import ca.bc.gov.open.pssg.rsbc.pdf.models.EmailResponse;

/**
 * 
 * Provides email client services from Mail It.
 * 
 */
@Service
public class EmailClientService {
	
	private static final Logger logger = LoggerFactory.getLogger(EmailClientService.class);

    private final RestTemplate restTemplate;
    private MailItProperties props; 
   

    public EmailClientService(RestTemplateBuilder builder, MailItProperties props) {
    	this.props = props; 
        this.restTemplate = new RestTemplateBuilder().basicAuthentication(props.getUsername(),
				props.getPassword()).build();
    }
    
    @Retryable(retryFor = { 
			HttpServerErrorException.class,
			HttpClientErrorException.class,
			ResourceAccessException.class
	}, maxAttempts = 5, backoff = @Backoff(delay = 10000))
    public ResponseEntity<EmailResponse> sendEmail(EmailRequest emailRequest, String noticeNumber) {
    	
		logger.info("Sending mail via EmailClientService.sendMail");
    	 
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        String auth = props.getUsername() + ":" + props.getPassword();
        String encodedAuth = Base64.getEncoder().encodeToString(auth.getBytes(StandardCharsets.UTF_8));
        headers.set(HttpHeaders.AUTHORIZATION, "Basic " + encodedAuth);

        HttpEntity<EmailRequest> request = new HttpEntity<>(emailRequest, headers);

        return restTemplate.exchange(
            props.getUrl() + "/mail/send",
            HttpMethod.POST,
            request,
            EmailResponse.class
        );
    }
    
    // 4xx
    @Recover
    public ResponseEntity<EmailResponse> recover(HttpClientErrorException ex, EmailRequest failedRequest, String noticeNumber) {
    	logger.error("Server error—retries exhausted when calling Mail It for Notice: {} {} - {}", ex.getStatusCode(), ex.getResponseBodyAsString(), ex);
    	EmailResponse resp = new EmailResponse();
    	resp.setAcknowledge(false);
    	return new ResponseEntity<>(resp, HttpStatus.BAD_REQUEST);
    }

    //5xx
	@Recover
	private ResponseEntity<EmailResponse> recover(HttpServerErrorException ex, EmailRequest failedRequest, String noticeNumber) {
		logger.error("Server error—retries exhausted when calling Mail It for Notice: {} {} - {}", ex.getStatusCode(), ex.getResponseBodyAsString(), ex);
	   	EmailResponse resp = new EmailResponse();
    	resp.setAcknowledge(false);
		return new ResponseEntity<>(resp, HttpStatus.INTERNAL_SERVER_ERROR);
	}
	
	// I/O errors - connection time out, etc. No logical status code for this situation. 
	@Recover
	private ResponseEntity<EmailResponse> recover(ResourceAccessException ex, EmailRequest failedRequest, String noticeNumber) {
		logger.error("Connection issue—retries exhausted when calling Mail It for Notice: {} {}", ex.getMessage(), ex);
		EmailResponse resp = new EmailResponse();
    	resp.setAcknowledge(false);
		return new ResponseEntity<>(resp, null);
	}    
    
}
