package ca.bc.gov.open.rsbc.mailit.mail;

import ca.bc.gov.open.rsbc.mailit.mail.api.model.EmailObject;
import ca.bc.gov.open.rsbc.mailit.mail.api.model.EmailRequest;
import ca.bc.gov.open.rsbc.mailit.mail.api.model.EmailRequestContent;
import ca.bc.gov.open.rsbc.mailit.mail.api.model.EmailResponse;
import ca.bc.gov.open.rsbc.mailit.mail.controller.MailApiController;
import ca.bc.gov.open.rsbc.mailit.mail.mappers.SimpleMessageMapper;
import ca.bc.gov.open.rsbc.mailit.mail.mappers.SimpleMessageMapperImpl;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInstance;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public class MailApiDelegateImplTest {

    private MailApiController sut;

    @Mock
    private JavaMailSender mailSenderMock;

    @BeforeAll
    public void beforeAll() {

        MockitoAnnotations.initMocks(this);
        Mockito.doNothing().when(mailSenderMock).send(Mockito.any(SimpleMailMessage.class));
        SimpleMessageMapper simpleMessageMapper = new SimpleMessageMapperImpl();
        sut = new MailApiController(mailSenderMock, simpleMessageMapper);
    }

    @Test
    @DisplayName("202: with valid email request should return 202")
    public void withValidEmailRequestShouldReturn202() {

        EmailRequest emailRequest = new EmailRequest();
        EmailObject from = new EmailObject();
        from.setEmail("bobross@paintit.com");
        emailRequest.setFrom(from);
        EmailRequestContent emailContent = new EmailRequestContent();
        emailContent.setType("text/html");
        emailContent.setValue("value");
        emailRequest.setContent(emailContent);
        List<EmailObject> tos = new ArrayList<>();
        EmailObject to = new EmailObject();
        to.setEmail("hansolo@galaxy.r2d2");
        tos.add(to);
        emailRequest.setTo(tos);
        ResponseEntity<EmailResponse> actual = sut.mailSendPost(emailRequest);
        assertEquals(HttpStatus.ACCEPTED, actual.getStatusCode());
        assertEquals(true, actual.getBody().getAcknowledge());

    }

    @Test
    @DisplayName("400: with valid email request should return 202")
    public void withInvalidValidEmailRequestShouldReturn400() {

        ResponseEntity<EmailResponse> actual = sut.mailSendPost(new EmailRequest());
        assertEquals(HttpStatus.BAD_REQUEST, actual.getStatusCode());

    }


}
