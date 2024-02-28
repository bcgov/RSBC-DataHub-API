package ca.bc.gov.open.rsbc.mailit.mail;

import ca.bc.gov.open.rsbc.mailit.mail.mappers.SimpleMessageMapper;
import ca.bc.gov.open.rsbc.mailit.mail.mappers.SimpleMessageMapperImpl;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;

import static org.springframework.security.config.Customizer.withDefaults;

@Configuration
@EnableWebSecurity
public class MailConfig {

    @Value("${mail-auth.clientSecret}")
    private String clientSecret;
    @Value("${mail-auth.clientId}")
    private String clientId;

    @Bean
    public SimpleMessageMapper simpleMessageMapper() {
        return new SimpleMessageMapperImpl();
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests((authz) ->
                authz.anyRequest().authenticated()).httpBasic(withDefaults());
        http.csrf(csrf -> csrf.disable());
        return http.build();
    }

    @Bean
    public UserDetailsService userDetailsService() {
        UserDetails userDetails = User.builder()
                .username(clientId)
                //no in-memory password encoder is required
                .password("{noop}" + clientSecret)
                .build();

        return new InMemoryUserDetailsManager(userDetails);
    }
}
