package ca.bc.gov.open.pssg.rsbc.pdf.component;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class AdobeOrdsPropertiesTest {

    @Test
    public void testPropertiesSetAndGet() {
    	
        AdobeOrdsProperties properties = new AdobeOrdsProperties();

        // Set values
        properties.getAem().getReport().getServer().setAppId("myAppId");
        properties.getAem().getReport().getServer().setUrl("https://api.example.com");
        properties.getOrds().setBaseUrl("https://api.example.com");
        properties.getOrds().getAuth().setUsername("user");
        properties.getOrds().getAuth().setPassword("pass");

        // Assert values
        assertEquals("myAppId", properties.getAem().getReport().getServer().getAppId());
        assertEquals("https://api.example.com", properties.getAem().getReport().getServer().getUrl());
        assertEquals("https://api.example.com", properties.getOrds().getBaseUrl());
        assertEquals("user", properties.getOrds().getAuth().getUsername());
        assertEquals("pass", properties.getOrds().getAuth().getPassword());
    }
}
