package ca.bc.gov.open.pssg.rsbc.pdf.component;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "adobeOrds")
public class AdobeOrdsProperties {
	
	private Auth auth;
    private String url;

    public static class Auth {
    	
		private String username;
        private String password;
        
        public String getUsername() {
			return username;
		}
		public String getPassword() {
			return password;
		}
    }

	public Auth getAuth() {
		return auth;
	}

	public String getUrl() {
		return url;
	}
}
