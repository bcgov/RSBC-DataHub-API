package ca.bc.gov.open.pssg.rsbc.config;

import fi.solita.clamav.ClamAVClient;
import ca.bc.gov.open.pssg.rsbc.service.ClamAvService;
import ca.bc.gov.open.pssg.rsbc.service.ClamAvServiceImpl;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableConfigurationProperties(ClamAvProperties.class)
public class AutoConfiguration {

    private final ClamAvProperties clamAvProperties;

    Logger logger = LoggerFactory.getLogger(AutoConfiguration.class);

    public AutoConfiguration(ClamAvProperties clamAvProperties) {
        this.clamAvProperties = clamAvProperties;
    }

    @Bean
    @ConditionalOnMissingBean(ClamAVClient.class)
    public ClamAVClient clamAVClient() {

        logger.info("Configuring ClamAv Client");
        logger.info("ClamAv host: [{}]", clamAvProperties.getHost());
        logger.info("ClamAv port: [{}]", clamAvProperties.getPort());
        logger.info("ClamAv timeout: [{}]", clamAvProperties.getTimeout());
        logger.info("ClamAv user: [{}]", clamAvProperties.getUser());
        logger.info("ClamAv pword: [{}]", clamAvProperties.getPassword());

        return new ClamAVClient(clamAvProperties.getHost(), clamAvProperties.getPort(), clamAvProperties.getTimeout());

    }

    @Bean
    @ConditionalOnMissingBean(ClamAvService.class)
    public ClamAvService clamAvService(ClamAVClient clamAVClient) {
        return new ClamAvServiceImpl(clamAVClient);
    }

}
