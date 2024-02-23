package ca.bc.gov.open.pssg.rsbc.exception;

import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.authentication.www.BasicAuthenticationEntryPoint;
import org.springframework.stereotype.Component;

import ca.bc.gov.open.pssg.rsbc.utils.AppConstants;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

/**
 * Authentication failure response handler
 * 
 * @author 237563
 *
 */
@Component
public class AuthenticationFailureHandler extends BasicAuthenticationEntryPoint  {
	
	private final Logger logger = LoggerFactory.getLogger(AuthenticationFailureHandler.class);

	@Override
	public void commence(HttpServletRequest request, HttpServletResponse response,
			AuthenticationException authException) throws IOException {
		
		//String errorMessage = "401 - Unauthorized entry, please authenticate";
		//JSONObject json = new JSONObject();
		//json.put("status_message", errorMessage);
		
		logger.debug("API basic authentication failed");
		response.setContentType(AppConstants.JSON_CONTENT);
		response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
		//response.setCharacterEncoding("UTF-8");
	}
	
	@Override
    public void afterPropertiesSet() {
        setRealmName("APR - CLamAv Client");
        super.afterPropertiesSet();
    }

}