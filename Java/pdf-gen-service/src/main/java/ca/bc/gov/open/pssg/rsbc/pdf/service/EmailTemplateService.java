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

import ca.bc.gov.open.pssg.rsbc.pdf.utils.XmlUtilities.FormType;

@Service
public class EmailTemplateService {

    @Autowired
    private TemplateEngine templateEngine;

    public String generateEmailHtml(FormType formType, Document xmlDocument) {
        String templateName = getTemplateName(formType);
        Map<String, Object> variables = extractVariablesFromXml(xmlDocument);

        Context context = new Context();
        context.setVariables(variables);

        return templateEngine.process(templateName, context);
    }

    private String getTemplateName(FormType formType) {
        return formType.name().toLowerCase(); // e.g., "f1p1"
    }

    private Map<String, Object> extractVariablesFromXml(Document document) {
    	
        Map<String, Object> variables = new HashMap<>();
        XPath xpath = XPathFactory.newInstance().newXPath();

        try {
            // Extract values from the XML payload using XPath
            variables.put("applicantFirstName", xpath.evaluate("/form/identification-information/first-name-applicant", document));
            variables.put("applicantLastName", xpath.evaluate("/form/identification-information/last-name-applicant", document));
            variables.put("noticeNumber", xpath.evaluate("/form/prohibition-information/control-prohibition-number", document));
            
        } catch (XPathExpressionException e) {
            throw new RuntimeException("Error parsing XML", e);
        }

        return variables;
    }
}
