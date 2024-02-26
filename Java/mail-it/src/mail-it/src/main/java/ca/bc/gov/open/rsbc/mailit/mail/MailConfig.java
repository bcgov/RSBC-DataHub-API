package ca.bc.gov.open.rsbc.mailit.mail;

import ca.bc.gov.open.rsbc.mailit.mail.mappers.SimpleMessageMapper;
import ca.bc.gov.open.rsbc.mailit.mail.mappers.SimpleMessageMapperImpl;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MailConfig {

    @Bean
    public SimpleMessageMapper simpleMessageMapper() {
        return new SimpleMessageMapperImpl();
    }

}
