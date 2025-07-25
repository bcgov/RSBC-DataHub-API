package ca.bc.gov.open.pssg.rsbc.pdf.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import ca.bc.gov.open.pssg.rsbc.pdf.component.AdobeOrdsProperties;

@SpringBootTest
public class AdobeReportServerServiceTest {

    @Mock
    private RestTemplateBuilder restTemplateBuilder;

    @Mock
    private RestTemplate restTemplate;

    @Mock
    private AdobeOrdsProperties adobeOrdsProperties;

    @InjectMocks
    private AdobeReportServerService adobeReportServerService;

    @BeforeEach
    public void setUp() {
    	
        AdobeOrdsProperties.Aem.Report.Server server = new AdobeOrdsProperties.Aem.Report.Server();
        server.setUrl("https://dummy-report-server.com/render");

        AdobeOrdsProperties.Aem.Report report = new AdobeOrdsProperties.Aem.Report();
        report.setServer(server);

        AdobeOrdsProperties.Aem aem = new AdobeOrdsProperties.Aem();
        aem.setReport(report);

        AdobeOrdsProperties adobeProps = new AdobeOrdsProperties();
        adobeProps.setAem(aem);

        when(restTemplateBuilder.build()).thenReturn(restTemplate);

        adobeReportServerService = new AdobeReportServerService(adobeProps, restTemplateBuilder);
    }

    @Test
    public void testCallReportServer_SuccessfulResponse() {
        byte[] mockPdfBytes = "Fake PDF content".getBytes();
        ResponseEntity<Object> mockResponse = new ResponseEntity<>(mockPdfBytes, HttpStatus.OK);

        when(restTemplate.getForEntity(anyString(), any())).thenReturn(mockResponse);

        ResponseEntity<byte[]> response = adobeReportServerService.callReportServer("cfg123", "formX", "key999");

        assert response.getStatusCode() == HttpStatus.OK;
        assert new String(response.getBody()).equals("Fake PDF content");
    }
}
