package ca.bc.gov.open.pssg.rsbc.pdf.component;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "mail.it")
public class MailItProperties {

    private String username;
    private String password;
    private String url;
    private String from; 
    private String registry; 
    private String bcc1;
    private String bcc2; 

    public String getRegistry() {
		return registry;
	}

	public void setRegistry(String registry) {
		this.registry = registry;
	}

	public String getBcc1() {
		return bcc1;
	}

	public void setBcc1(String bcc1) {
		this.bcc1 = bcc1;
	}

	public String getBcc2() {
		return bcc2;
	}

	public void setBcc2(String bcc2) {
		this.bcc2 = bcc2;
	}

	public String getFrom() {
		return from;
	}

	public void setFrom(String from) {
		this.from = from;
	}

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }
    
}
