package ca.bc.gov.open.rsbc.mailit.mail.controller;

import ca.bc.gov.open.rsbc.mailit.mail.api.MailApi;
import ca.bc.gov.open.rsbc.mailit.mail.api.model.EmailAttachment;
import ca.bc.gov.open.rsbc.mailit.mail.api.model.EmailObject;
import ca.bc.gov.open.rsbc.mailit.mail.api.model.EmailRequest;
import ca.bc.gov.open.rsbc.mailit.mail.api.model.EmailResponse;
import ca.bc.gov.open.rsbc.mailit.mail.mappers.SimpleMessageMapper;
import jakarta.mail.MessagingException;
import jakarta.mail.internet.MimeMessage;
import jakarta.mail.util.ByteArrayDataSource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@RestController
public class MailApiController implements MailApi {

    private final JavaMailSender emailSender;

    private final SimpleMessageMapper simpleMessageMapper;

    Logger logger = LoggerFactory.getLogger(MailApiController.class);

    public MailApiController(JavaMailSender emailSender, SimpleMessageMapper simpleMessageMapper) {
        this.emailSender = emailSender;
        this.simpleMessageMapper = simpleMessageMapper;
    }

    @Override
    public ResponseEntity<EmailResponse> mailSendPost(EmailRequest emailRequest) {
        logger.info("Beginning mail send");

        Optional<EmailObject> emailObject = emailRequest.getTo().stream().findFirst();
        EmailResponse emailResponse = new EmailResponse();

        if (emailObject.isEmpty()) {
            logger.error("No value present in email object");
            return new ResponseEntity("error", HttpStatus.BAD_REQUEST);
        }

        // No attachmentment(s)
        if (null == emailRequest.getAttachment() || emailRequest.getAttachment().isEmpty()) {

            logger.info("Mapping message");
            SimpleMailMessage simpleMailMessage = simpleMessageMapper.toSimpleMailMessage(emailRequest);

            logger.info("Sending message");
            emailSender.send(simpleMailMessage);

            // EmailResponse emailResponse = new EmailResponse();
            emailResponse.setAcknowledge(true);

            logger.info("Message sent successfully w/o attachment(s)");
            return ResponseEntity.accepted().body(emailResponse);

            // Has attachments
        } else {
            MimeMessage message = emailSender.createMimeMessage();

            try {
                MimeMessageHelper helper = new MimeMessageHelper(message, true);

                helper.setFrom(emailRequest.getFrom().getEmail());

                // Extract the to(s).
                List<String> tos = new ArrayList<String>();
                for (EmailObject element : emailRequest.getTo()) {
                    tos.add(element.getEmail());
                }
                helper.setTo(tos.toArray(new String[0]));

                helper.setSubject(emailRequest.getSubject());

                if (emailRequest.getContent().getType().equalsIgnoreCase("text/plain")) {
                    helper.setText(emailRequest.getContent().getValue(), false);
                } else if (emailRequest.getContent().getType().equalsIgnoreCase("text/html")) {
                    helper.setText(emailRequest.getContent().getValue(), true);
                } else {
                    logger.error("Invalid or missing content type value");
                    return new ResponseEntity("error", HttpStatus.BAD_REQUEST);
                }
                // the attachment objects as an array. (see jag-mail-it-api.yaml)
                // if there is error with an attachment, it will throw exception
                for (EmailAttachment emailAttachment : emailRequest.getAttachment()) {
                    if (emailAttachment.getFilename().endsWith(".pdf")) {
                        helper.addAttachment(emailAttachment.getFilename(),
                                new ByteArrayDataSource(emailAttachment.getFilecontents(), "application/pdf"));
                    } else {
                        helper.addAttachment(emailAttachment.getFilename(),
                                new ByteArrayDataSource(emailAttachment.getFilecontents(), "application/octet-stream"));
                    }
                }

                emailSender.send(message);

                emailResponse.setAcknowledge(true);
                logger.info("Message sent successfully w/attachment(s)");
                return ResponseEntity.accepted().body(emailResponse);

            } catch (MessagingException e) {
                logger.error("Failed to send email: ", e);

                return new ResponseEntity("error", HttpStatus.BAD_REQUEST);
            }
        }
    }
}
