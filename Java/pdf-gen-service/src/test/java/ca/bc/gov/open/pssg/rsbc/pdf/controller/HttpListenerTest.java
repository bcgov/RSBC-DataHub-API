package ca.bc.gov.open.pssg.rsbc.pdf.controller;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.util.Base64;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.MockedStatic;
import org.springframework.http.ResponseEntity;
import org.w3c.dom.Document;

import ca.bc.gov.open.pssg.rsbc.pdf.models.PDFRenderResponse;
import ca.bc.gov.open.pssg.rsbc.pdf.service.PdfRenderService;
import ca.bc.gov.open.pssg.rsbc.pdf.service.XMLParserDecoder;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities.FormType;

/**
 * 
 * Main HttpListener class unit tests
 * 
 */
public class HttpListenerTest {

    private PdfRenderService pdfRenderService;
    private HttpListener controller;

    @BeforeEach
    public void setUp() {
        pdfRenderService = mock(PdfRenderService.class);
        controller = new HttpListener(pdfRenderService);
    }

	@Test
    public void renderPdf_shouldReturnBadRequest_whenPayloadIsNull() {
        ResponseEntity<?> response = controller.renderPdf(null);
        assertEquals(400, response.getStatusCodeValue());
        assertEquals("Request body cannot be null", response.getBody());
    }

    @Test
    public void renderPdf_shouldReturnPdf_whenPayloadIsValid() throws Exception {
        String xml = "<root><notice>12345</notice><form>...</form></root>";
        String base64Xml = Base64.getEncoder().encodeToString(xml.getBytes());
        Document doc = mock(Document.class);
        byte[] mockPdf = "Fake PDF content".getBytes();

        try (MockedStatic<XmlUtilities> xmlUtilMock = org.mockito.Mockito.mockStatic(XmlUtilities.class);
             MockedStatic<XMLParserDecoder> xmlParserMock = org.mockito.Mockito.mockStatic(XMLParserDecoder.class)) {

            xmlUtilMock.when(() -> XmlUtilities.getNoticeNumber(any())).thenReturn("12345");
            xmlUtilMock.when(() -> XmlUtilities.categorizeFormType(any())).thenReturn(FormType.f3);
            xmlParserMock.when(() -> XMLParserDecoder.getDocument(any())).thenReturn(doc);

            when(pdfRenderService.render(eq(FormType.f3), any(), eq(doc)))
                .thenReturn(new PDFRenderResponse(mockPdf));

            ResponseEntity<?> response = controller.renderPdf(base64Xml);

            assertEquals(200, response.getStatusCodeValue());
            assertEquals(mockPdf, response.getBody());
            assertEquals("inline; filename=\"evidence.pdf\"",
                         response.getHeaders().getContentDisposition().toString());
        }
    }

    @Test
    public void renderPdf_shouldReturnServerError_whenFormTypeIsInvalid() throws Exception {
        String xml = "<root><form>invalid</form></root>";
        String base64Xml = Base64.getEncoder().encodeToString(xml.getBytes());
        Document doc = mock(Document.class);

        try (MockedStatic<XmlUtilities> xmlUtilMock = org.mockito.Mockito.mockStatic(XmlUtilities.class);
             MockedStatic<XMLParserDecoder> xmlParserMock = org.mockito.Mockito.mockStatic(XMLParserDecoder.class)) {

            xmlUtilMock.when(() -> XmlUtilities.getNoticeNumber(any())).thenReturn("00000");
            xmlUtilMock.when(() -> XmlUtilities.categorizeFormType(any())).thenReturn(FormType.UNKNOWN);
            xmlParserMock.when(() -> XMLParserDecoder.getDocument(any())).thenReturn(doc);

            ResponseEntity<?> response = controller.renderPdf(base64Xml);

            assertEquals(500, response.getStatusCodeValue());
            assertTrue(new String((byte[]) response.getBody())
                .contains("XML form content not the expected Form 3 type"));
        }
    }
}