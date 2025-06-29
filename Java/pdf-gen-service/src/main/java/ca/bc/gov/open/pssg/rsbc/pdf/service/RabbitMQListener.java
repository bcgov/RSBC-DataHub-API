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

import ca.bc.gov.open.pssg.rsbc.pdf.exception.UnsupportedXMLFormTypeException;
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
	private PdfRenderService renderer;
	
	public RabbitMQListener(XMLParserDecoder xmlDecoder, PdfRenderService renderer) {
		super();
		this.xmlDecoder = xmlDecoder;
		this.renderer = renderer;
	}

	public XMLParserDecoder getXmlDecoder() {
		return xmlDecoder;
	}

	public PdfRenderService getRenderer() {
		return renderer;
	}

	@RabbitListener(queues = "DF.pdf")
    public void receiveMessage(String message) {
		
        logger.info("APR PDF Generator received a message from the DF.pdf queue.");
        
        try {
        	
        	//STEP 1 - Extract and decode the XML form data from the JSON payload.  
			String xml = XMLParserDecoder.extractAndDecodeXml(message);
			
			//STEP 2 - Parse the XML form payload
			DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
	        dbFactory.setNamespaceAware(false);
	        dbFactory.setNamespaceAware(false);
	        DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
	        String _xml = XmlUtilities.formatXml(xml);
	        InputSource is = new InputSource(new StringReader(_xml));
	        Document doc = dBuilder.parse(is);

	        //STEP 3 - Categorize the XML form payload 
	        FormType formType = XmlUtilities.categorizeFormType(doc);
	       
	        if (!formType.equals(FormType.UNKNOWN)) {
	        	logger.info("XML form type identified as " + formType);
	        
	        	//STEPS 4, 5, etc. - Continue here to generate PDF, add template body, and mail. 
	        	
	        } else {
	        	throw new UnsupportedXMLFormTypeException("Unknown XML for type content in JSON payload.");
	        }
			
		} catch (Exception e) {
			logger.error(e.getMessage());
			e.printStackTrace();
		}
    }
}
