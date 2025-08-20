package ca.bc.gov.open.pssg.rsbc.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "clamav.client")
public class ClamAvProperties {

    private String host;
    private int port;
    private int timeout;
    private String user;
    private String password; 

    public String getHost() {
        return host;
    }

    public void setHost(String host) {
        this.host = host;
    }

	public int getPort() {
        return port;
    }

    public void setPort(int port) {
        this.port = port;
    }

    public int getTimeout() {
        return timeout;
    }

    public void setTimeout(int timeout) {
        this.timeout = timeout;
    }
    
    public String getUser() {
  		return user;
  	}

  	public void setUser(String user) {
  		this.user = user;
  	}

  	public String getPassword() {
  		return password;
  	}

  	public void setPassword(String password) {
  		this.password = password;
  	}

}
