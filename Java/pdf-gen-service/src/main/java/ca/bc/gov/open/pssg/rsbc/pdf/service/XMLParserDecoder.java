package ca.bc.gov.open.pssg.rsbc.pdf.service;

import java.util.Base64;

import org.json.JSONObject;
import org.springframework.stereotype.Service;

@Service
public class XMLParserDecoder {

	public static String extractAndDecodeXml(String jsonPayload) {
		try {
			// Step 1: Parse JSON string
			JSONObject jsonObject = new JSONObject(jsonPayload);
			JSONObject prohibitionReview = jsonObject.getJSONObject("prohibition_review");

			// Step 2: Extract the base64-encoded XML string
			String base64Xml = prohibitionReview.getString("xml");

			// Step 3: Decode the base64 string into XML
			byte[] decodedBytes = Base64.getDecoder().decode(base64Xml);
			return new String(decodedBytes, java.nio.charset.StandardCharsets.UTF_8);

		} catch (Exception e) {
			System.err.println("Error extracting or decoding XML: " + e.getMessage());
			return null;
		}
	}
}
