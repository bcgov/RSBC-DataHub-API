package ca.bc.gov.open.pssg.rsbc.pdf.service;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import java.util.Base64;
import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.w3c.dom.Document;

import ca.bc.gov.open.pssg.rsbc.pdf.component.MailItProperties;
import ca.bc.gov.open.pssg.rsbc.pdf.models.*;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities;

class EmailAssemblyServiceTest {

    private EmailAssemblyService service;
    private MailItProperties props;

    @BeforeEach
    void setUp() {
        props = mock(MailItProperties.class);
        when(props.getFrom()).thenReturn("from@example.com");
        when(props.getBcc1()).thenReturn("bcc1@example.com");
        when(props.getBcc2()).thenReturn("bcc2@example.com");

        service = new EmailAssemblyService(props);
    }

    @Test
    void testGetEmailRequest_WithConsentForm() {
        PDFRenderResponse response = new PDFRenderResponse();
        response.setPdf("sample-pdf".getBytes());
        response.setEmailBody("<html>Email Body</html>");

        Document doc = mock(Document.class);
        // Simulate utility result
        mockStatic(XmlUtilities.class);
        when(XmlUtilities.getApplicantEmailAddress(doc)).thenReturn("user@example.com");

        String consentForm = Base64.getEncoder().encodeToString("consent".getBytes());

        EmailRequest result = service.getEmailRequest(response, doc, "ABC123", consentForm);

        assertEquals("Copy of Application form - Driving Prohibition ABC123 Review", result.getSubject());
        assertEquals("from@example.com", result.getFrom().getEmail());

        List<EmailObject> toList = result.getTo();
        assertTrue(toList.stream().anyMatch(e -> e.getEmail().equals("user@example.com")));
        assertTrue(toList.stream().anyMatch(e -> e.getEmail().equals("bcc1@example.com")));
        assertTrue(toList.stream().anyMatch(e -> e.getEmail().equals("bcc2@example.com")));

        List<EmailAttachment> attachments = result.getAttachment();
        assertEquals(2, attachments.size()); // PDF + Consent

        assertEquals("text/html", result.getContent().getType());
        assertEquals("<html>Email Body</html>", result.getContent().getValue());
    }
}
