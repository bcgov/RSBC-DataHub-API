package ca.bc.gov.open.pssg.rsbc.pdf.service;

import java.util.Base64;

import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import ca.bc.gov.open.pssg.rsbc.pdf.exception.UnsupportedPayloadException;
import ca.bc.gov.open.pssg.rsbc.pdf.exception.XmlExtractionException;

/**
 * 
 * JSON Payload utilities
 * 
 */
@Service
public class XMLParserDecoder {
	
	private static final Logger logger = LoggerFactory.getLogger(XMLParserDecoder.class);
	
	public static String extractAndDecodeXml(String jsonPayload)
	        throws XmlExtractionException, UnsupportedPayloadException {
	    try {
	        JSONObject jsonObject = new JSONObject(jsonPayload);
	        String eventType = jsonObject.optString("event_type");
	        
	        logger.info("Received JSON Payload Event type of '" + eventType + "'");
	        
	        if (!"prohibition_review".equals(eventType) && !"Document_submission".equals(eventType)) {
	            throw new UnsupportedPayloadException("Unsupported JSON Payload event_type: '" + eventType + "'");
	        }

	        JSONObject eventData = jsonObject.getJSONObject(eventType);
	        String base64Xml = eventData.getString("xml");

	        byte[] decodedBytes = Base64.getDecoder().decode(base64Xml);
	        return new String(decodedBytes, java.nio.charset.StandardCharsets.UTF_8);

	    } catch (UnsupportedPayloadException e) { 
	        throw e; // Re-throw to preserve payload context
	    } catch (Exception e) {
	        throw new XmlExtractionException("Failed to decode XML from JSON payload", e);
	    }
	}
}
