package ca.bc.gov.open.pssg.rsbc.pdf.service;

import java.io.StringReader;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Service;
import org.w3c.dom.Document;
import org.xml.sax.InputSource;

import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities.FormType;



/**
 * 
 * Receives message from DF.pdf queue, renders form and mails. 
 * 
 */
@Service
public class RabbitMQListener {
	
	private static final Logger logger = LoggerFactory.getLogger(RabbitMQListener.class);
	
	private XMLParserDecoder xmlDecoder; 

	public XMLParserDecoder getXmlDecoder() {
		return xmlDecoder;
	}
	
	public void setXmlDecoder(XMLParserDecoder xmlDecoder) {
		this.xmlDecoder = xmlDecoder;
	}

	@RabbitListener(queues = "DF.pdf")
    public void receiveMessage(String message) {
        logger.info("APR PDF Generator received a message from the DF.pdf queue.");
        try {
        	
        	//STEP 1 - Extract and decode the XML form data from the JSON payload.  
			logger.info("Extracting XML form payload..."); 
			String xml = XMLParserDecoder.extractAndDecodeXml(message);
			logger.info(xml);
			logger.info(XmlUtilities.formatXml(xml));
			
			//STEP 2 - Select the XDP template type based on the XML form data.
			DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
	        dbFactory.setNamespaceAware(false);
	        dbFactory.setNamespaceAware(false);
	        DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();

	        // Parse from string
	        InputSource is = new InputSource(new StringReader(xml));
	        Document doc = dBuilder.parse(is);

	        // TODO need to enhance the next line to pick out form 3 types 
	        FormType formType = XmlUtilities.categorizeFormType(doc);
	        logger.info("Form type: " + formType);
			
			
		} catch (Exception e) {
			logger.error(e.getMessage());
			e.printStackTrace();
		}
    }
}
