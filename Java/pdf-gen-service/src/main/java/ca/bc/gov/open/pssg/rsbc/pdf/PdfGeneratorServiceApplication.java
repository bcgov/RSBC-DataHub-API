package ca.bc.gov.open.pssg.rsbc.pdf;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.retry.annotation.EnableRetry;

@EnableRetry
@SpringBootApplication
public class PdfGeneratorServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(PdfGeneratorServiceApplication.class, args);
	}

}
