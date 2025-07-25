package ca.bc.gov.open.pssg.rsbc.pdf.configuration;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

import ca.bc.gov.open.pssg.rsbc.pdf.component.HttpListenerProperties;

import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.crypto.factory.PasswordEncoderFactories;
import org.springframework.security.crypto.password.PasswordEncoder;
import static org.springframework.security.config.Customizer.withDefaults;

/**
 * 
 * Adds Basic Auth to the HttpListener endpoint
 * 
 */
@Configuration
public class SecurityConfig {
	
	private HttpListenerProperties props; 

	public SecurityConfig(HttpListenerProperties props) {
		this.props = props; 
	}
	
    @Bean
    SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                .authorizeHttpRequests(auth -> auth
                                .requestMatchers("/renderpdf").authenticated()
                                .anyRequest().permitAll()
                )
                .httpBasic(withDefaults())
                .csrf(csrf -> csrf.disable()); // For API-only applications

        return http.build();
    }

    @Bean
    UserDetailsService userDetailsService() {
        PasswordEncoder encoder = PasswordEncoderFactories.createDelegatingPasswordEncoder();
        
        UserDetails user = User.builder()
            .username(props.getUsername())
            .password(encoder.encode(props.getPassword()))
            .roles("USER")
            .build();

        return new InMemoryUserDetailsManager(user);
    }
}