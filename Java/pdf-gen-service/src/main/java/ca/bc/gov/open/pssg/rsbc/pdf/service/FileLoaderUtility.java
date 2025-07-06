package ca.bc.gov.open.pssg.rsbc.pdf.service;

import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.io.InputStream;

/**
 * 
 * Utility service for loading a file from the resources folder. 
 * 
 */
@Service
public class FileLoaderUtility {

    /**
     * Loads a file from the classpath (src/main/resources) and returns it as a byte array.
     *
     * @param filePath the relative path to the PDF file (e.g., "documents/sample.pdf")
     * @return byte array representing the PDF content
     * @throws IOException if the file cannot be read
     */
    public byte[] loadFileFromResources(String filePath) throws IOException {
        ClassPathResource resource = new ClassPathResource(filePath);
        try (InputStream inputStream = resource.getInputStream()) {
            return inputStream.readAllBytes(); 
        }
    }
}


