package ca.bc.gov.open.pssg.rsbc.security;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.util.matcher.AntPathRequestMatcher;

import ca.bc.gov.open.pssg.rsbc.config.ClamAvProperties;
import ca.bc.gov.open.pssg.rsbc.exception.AuthenticationFailureHandler;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity
//@RequiredArgsConstructor
public class SecurityConfiguration {
	
	  @Autowired
	    private ClamAvProperties properties;

	    @Autowired
	    private AuthenticationFailureHandler authenticationFailureHandler;

	    @Bean
	    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
	        http.sessionManagement(
	                httpSecuritySessionManagementConfigurer -> {
	                    httpSecuritySessionManagementConfigurer.sessionCreationPolicy(
	                            SessionCreationPolicy.STATELESS);
	                });

	        http.csrf(csrf -> csrf.disable())
	                .authorizeHttpRequests(authorizeHttpRequests -> authorizeHttpRequests
	                        .requestMatchers(new AntPathRequestMatcher("api/v1/auth/**")
	                                , new AntPathRequestMatcher("/v3/api-docs/**")
	                                , new AntPathRequestMatcher("/swagger-resources*")
	                                , new AntPathRequestMatcher("/swagger-ui.html")
	                                , new AntPathRequestMatcher("/swagger-ui/**")
	                                , new AntPathRequestMatcher("/webjars/**")
	                                , new AntPathRequestMatcher("/swagger-config/**")
	                                , new AntPathRequestMatcher("/actuator/**")
	                        ).permitAll().anyRequest().authenticated()
	                );

	        http.httpBasic(
	                httpSecurityHttpBasicConfigurer -> {
	                    httpSecurityHttpBasicConfigurer.authenticationEntryPoint(
	                            authenticationFailureHandler);
	                });

	        return http.build();
	    }

	    @Bean
	    public InMemoryUserDetailsManager userDetailsService() {
	        UserDetails user =
	                User.builder()
	                        .username(properties.getUser())
	                        .password(passwordEncoder().encode(properties.getPassword()))
	                        .roles("USER")
	                        .build();
	        return new InMemoryUserDetailsManager(user);
	    }

	    @Bean
	    public PasswordEncoder passwordEncoder() {
	        return new BCryptPasswordEncoder();
	    }

}
