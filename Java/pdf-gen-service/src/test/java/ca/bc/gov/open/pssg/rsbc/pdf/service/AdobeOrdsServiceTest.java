package ca.bc.gov.open.pssg.rsbc.pdf.service;

import ca.bc.gov.open.pssg.rsbc.pdf.component.AdobeOrdsProperties;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.*;
import org.springframework.http.*;
import org.springframework.retry.annotation.EnableRetry;
import org.springframework.test.context.junit.jupiter.SpringJUnitConfig;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.client.RestTemplate;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

@SpringJUnitConfig
@EnableRetry
public class AdobeOrdsServiceTest {

    @Mock
    private RestTemplate restTemplate;

    private AdobeOrdsService adobeOrdsService;

    private AdobeOrdsProperties adobeOrdsProperties;

    @BeforeEach
    public void setup() {
        MockitoAnnotations.openMocks(this);

        // Setup AdobeOrdsProperties manually
        adobeOrdsProperties = new AdobeOrdsProperties();
        adobeOrdsProperties.getOrds().getAuth().setUsername("testuser");
        adobeOrdsProperties.getOrds().getAuth().setPassword("testPassword");
        adobeOrdsProperties.getOrds().setBaseUrl("http://mock-api/");

        // Manually instantiate the service
        adobeOrdsService = new AdobeOrdsService(adobeOrdsProperties);

        // Inject mock RestTemplate
        ReflectionTestUtils.setField(adobeOrdsService, "restTemplate", restTemplate);
    }

    @Test
    public void testAdobeSaveXML_SuccessfulRequest_ReturnsResponse() {
        String xmlPayload = "<data>test</data>";
        String endpoint = adobeOrdsProperties.getOrds().getBaseUrl() + "adobesavexml";
        ResponseEntity<String> expectedResponse = new ResponseEntity<>("Success", HttpStatus.OK);

        when(restTemplate.postForEntity(eq(endpoint), any(), eq(String.class)))
            .thenReturn(expectedResponse);

        ResponseEntity<String> actualResponse = adobeOrdsService.adobeSaveXML(xmlPayload);

        assertEquals(HttpStatus.OK, actualResponse.getStatusCode());
        assertEquals("Success", actualResponse.getBody());

        // Verify the call happened
        verify(restTemplate, times(1)).postForEntity(eq(endpoint), any(), eq(String.class));
    }
}