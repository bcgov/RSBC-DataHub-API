package ca.bc.gov.open.pssg.rsbc.pdf.component;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "adobeords")
public class AdobeOrdsProperties {
	
	private Auth auth;
    private String baseUrl;

    public static class Auth {
    	
		private String username;
        private String password;
        
        public String getUsername() {
			return username;
		}
		public String getPassword() {
			return password;
		}
		public void setUsername(String username) {
			this.username = username;
		}
		public void setPassword(String password) {
			this.password = password;
		}
    }

	public Auth getAuth() {
		return auth;
	}

	public String getBaseUrl() {
		return baseUrl;
	}

	public void setAuth(Auth auth) {
		this.auth = auth;
	}

	public void setBaseUrl(String baseUrl) {
		this.baseUrl = baseUrl;
	}
	
}
