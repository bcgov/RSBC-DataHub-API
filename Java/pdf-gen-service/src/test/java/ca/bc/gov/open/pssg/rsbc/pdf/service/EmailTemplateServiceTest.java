package ca.bc.gov.open.pssg.rsbc.pdf.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.thymeleaf.TemplateEngine;
import org.thymeleaf.context.Context;
import org.w3c.dom.Document;

import ca.bc.gov.open.pssg.rsbc.pdf.exception.EmailTemplateServiceException;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities.FormType;

public class EmailTemplateServiceTest {

    private EmailTemplateService emailTemplateService;

    @Mock
    private TemplateEngine templateEngine;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
        emailTemplateService = new EmailTemplateService(templateEngine);
    }

    @Test
    public void testGenerateEmailHtml_f1p1_success() throws Exception {
    	
    	Document xmlDoc = XMLParserDecoder.getDocument("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n"
    			+ "<form xmlns:fr=\"http://orbeon.org/oxf/xml/form-runner\" fr:data-format-version=\"4.0.0\">\r\n"
    			+ "	<submitted>false</submitted>\r\n"
    			+ "</form>");
    	
        when(templateEngine.process(eq("f1p1"), any(Context.class))).thenReturn("<html>Mocked HTML</html>");

        String result = emailTemplateService.generateEmailHtml(FormType.f1p1, xmlDoc);

        assertNotNull(result);
        assertEquals("<html>Mocked HTML</html>", result);
    }

    @Test
    public void testGenerateEmailHtml_unsupportedFormType_shouldThrowException() throws Exception {
        Document xmlDoc = XMLParserDecoder.getDocument("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n"
        		+ "<form xmlns:fr=\"http://orbeon.org/oxf/xml/form-runner\" fr:data-format-version=\"4.0.0\">\r\n"
        		+ "	<identification-information>\r\n"
        		+ "		<applicant-information-label/>\r\n"
        		+ "		<applicant-role-select>tester</applicant-role-select>\r\n"
        		+ "	</identification-information>\r\n"
        		+ "</form>");

        EmailTemplateServiceException ex = assertThrows(
            EmailTemplateServiceException.class,
            () -> emailTemplateService.generateEmailHtml(FormType.UNKNOWN, xmlDoc)
        );

        assertTrue(ex.getMessage().contains("Unsupported"));
    }
}