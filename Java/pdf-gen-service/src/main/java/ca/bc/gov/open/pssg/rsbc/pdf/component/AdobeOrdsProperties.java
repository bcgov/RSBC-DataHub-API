package ca.bc.gov.open.pssg.rsbc.pdf.component;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "adobe")
public class AdobeOrdsProperties {

	private Ords ords;
	private Aem aem;

	public Ords getOrds() {
		return ords;
	}

	public void setOrds(Ords ords) {
		this.ords = ords;
	}

	public Aem getAem() {
		return aem;
	}

	public void setAem(Aem aem) {
		this.aem = aem;
	}

	public static class Ords {
		private Auth auth;
		private String baseUrl;

		public Auth getAuth() {
			return auth;
		}

		public void setAuth(Auth auth) {
			this.auth = auth;
		}

		public String getBaseUrl() {
			return baseUrl;
		}

		public void setBaseUrl(String baseUrl) {
			this.baseUrl = baseUrl;
		}

		public static class Auth {
			private String username;
			private String password;

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
		}
	}

	public static class Aem {
		private Report report;

		public Report getReport() {
			return report;
		}

		public void setReport(Report report) {
			this.report = report;
		}

		public static class Report {
			private Server server;

			public Server getServer() {
				return server;
			}

			public void setServer(Server server) {
				this.server = server;
			}

			public static class Server {
				private String url;
				private String config;

				public String getUrl() {
					return url;
				}

				public void setUrl(String url) {
					this.url = url;
				}

				public String getConfig() {
					return config;
				}

				public void setConfig(String config) {
					this.config = config;
				}

			}
		}
	}
}

//	private Auth auth;
//    private String baseUrl;
//
//    public static class Auth {
//    	
//		private String username;
//        private String password;
//        
//        public String getUsername() {
//			return username;
//		}
//		public String getPassword() {
//			return password;
//		}
//		public void setUsername(String username) {
//			this.username = username;
//		}
//		public void setPassword(String password) {
//			this.password = password;
//		}
//    }
//
//	public Auth getAuth() {
//		return auth;
//	}
//
//	public String getBaseUrl() {
//		return baseUrl;
//	}
//
//	public void setAuth(Auth auth) {
//		this.auth = auth;
//	}
//
//	public void setBaseUrl(String baseUrl) {
//		this.baseUrl = baseUrl;
//	}
