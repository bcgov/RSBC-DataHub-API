package ca.bc.gov.open.pssg.rsbc.pdf.component;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class MailItPropertiesTest {

    @Test
    public void testGettersAndSetters() {
        MailItProperties props = new MailItProperties();

        props.setUsername("testuser");
        props.setPassword("securepassword");
        props.setUrl("smtp.mail.com");
        props.setFrom("noreply@mail.com");
        props.setRegistry("mail-registry");
        props.setBcc1("bcc1@mail.com");
        props.setBcc2("bcc2@mail.com");

        assertEquals("testuser", props.getUsername());
        assertEquals("securepassword", props.getPassword());
        assertEquals("smtp.mail.com", props.getUrl());
        assertEquals("noreply@mail.com", props.getFrom());
        assertEquals("mail-registry", props.getRegistry());
        assertEquals("bcc1@mail.com", props.getBcc1());
        assertEquals("bcc2@mail.com", props.getBcc2());
    }
}
