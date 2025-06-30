package ca.bc.gov.open.pssg.rsbc.pdf.service;

import java.util.HashMap;
import java.util.Map;

import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.w3c.dom.Document;

import org.thymeleaf.TemplateEngine;
import org.thymeleaf.context.Context;

import ca.bc.gov.open.pssg.rsbc.pdf.exception.EmailTemplateServiceException;
import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities.FormType;

/**
 * 
 * Provides HTML Email generation for Form1 only.
 * 
 */
@Service
public class EmailTemplateService {

    @Autowired
    private TemplateEngine templateEngine;

    public String generateEmailHtml(FormType formType, Document xmlDocument) throws EmailTemplateServiceException {
    	
        String templateName = getTemplateName(formType);
        
        Map<String, Object> variables = extractVariablesFromXml(formType, xmlDocument);
        
        Context context = new Context();
        context.setVariables(variables);

        return templateEngine.process(templateName, context);
    }

    private String getTemplateName(FormType formType) {
        return formType.name().toLowerCase(); // e.g., "f1p1"
    }

    private Map<String, Object> extractVariablesFromXml(FormType formType, Document document) throws EmailTemplateServiceException {
    	
        Map<String, Object> variables = new HashMap<>();
        XPath xpath = XPathFactory.newInstance().newXPath();
        
        try {
        
	        switch (formType) {
	        case f1p1:
	        	variables.put("applicantFirstName", xpath.evaluate("/form/identification-information/first-name-applicant", document));
	            variables.put("applicantLastName", xpath.evaluate("/form/identification-information/last-name-applicant", document));
	            variables.put("noticeNumber", xpath.evaluate("/form/prohibition-information/control-prohibition-number", document));
	            break;
	        case f1p2:
	        	 variables.put("lawyerFirstName", xpath.evaluate("/form/identification-information/first-name-applicant", document));
	             variables.put("lawyerLastName", xpath.evaluate("/form/identification-information/last-name-applicant", document));
	             variables.put("noticeNumber", xpath.evaluate("/form/prohibition-information/control-prohibition-number", document));
	            break;  
	        case f1p3:
	       	 	variables.put("lawyerFirstName", xpath.evaluate("/form/identification-information/first-name-applicant", document));
	            variables.put("lawyerLastName", xpath.evaluate("/form/identification-information/last-name-applicant", document));
	            variables.put("noticeNumber", xpath.evaluate("/form/prohibition-information/control-prohibition-number", document));
	           break; 
	        case f1p4:
	       	 	variables.put("AuthPersonFirstName", xpath.evaluate("/form/identification-information/first-name-applicant", document));
	            variables.put("AuthPersonLastName", xpath.evaluate("/form/identification-information/last-name-applicant", document));
	            variables.put("noticeNumber", xpath.evaluate("/form/prohibition-information/control-prohibition-number", document));
	           break;
	        default:
	            throw new EmailTemplateServiceException("Unsupported formType value: " + formType);
	        }
        
        } catch (XPathExpressionException ex) {
        	throw new EmailTemplateServiceException(ex.getMessage(), ex);
        }

        return variables;
    }
}
