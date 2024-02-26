package ca.bc.gov.open.rsbc.mailit.mail;

import ca.bc.gov.open.rsbc.mailit.mail.mappers.SimpleMessageMapper;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInstance;
import org.springframework.boot.test.context.runner.ApplicationContextRunner;

import static org.assertj.core.api.Assertions.assertThat;

@TestInstance(TestInstance.Lifecycle.PER_CLASS)
public class MailConfigTest {

    ApplicationContextRunner context = new ApplicationContextRunner()
            .withUserConfiguration(MailConfig.class);

    @Test
    @DisplayName("ok: testing email configuration")
    public void shouldReturnValidConfiguration() {

        context.run(it -> {
            assertThat(it).hasSingleBean(SimpleMessageMapper.class);
        });

    }

}
