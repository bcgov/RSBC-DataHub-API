package ca.bc.gov.open.pssg.rsbc.pdf.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Service;


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
        //logger.info("APR PDF Generator received a message from the DF.pdf queue: " + message);
        logger.info("XML extraction: " + XMLParserDecoder.extractAndDecodeXml(message));
    }
}
