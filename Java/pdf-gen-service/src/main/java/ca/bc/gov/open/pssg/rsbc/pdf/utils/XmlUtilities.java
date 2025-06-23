package ca.bc.gov.open.pssg.rsbc.pdf.utils;

import java.io.StringReader;
import java.io.StringWriter;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.w3c.dom.Text;

import ca.bc.gov.open.pssg.rsbc.pdf.exception.UnsupportedFormTypeException;

public class XmlUtilities {
	
    public enum FormType {
        f1p1, // form 1, permutation 1, driver no lawyer
        f1p2, // form 1, permutation 2, driver obtained Lawyer
        f1p3, // form 1, permutation 3, Lawyer Office
        f1p4, // form 1, permutation 4, Authorized Person
        UNKNOWN // unknown form 1 permutation. 
    }

    public static String formatXml(String xml) throws Exception {
    	
        // Parse the XML input
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setIgnoringElementContentWhitespace(true);
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document document = builder.parse(new org.xml.sax.InputSource(new StringReader(xml)));

        // Normalize and remove empty text nodes
        document.normalize();
        removeWhitespaceNodes(document.getDocumentElement());

        // Set up a transformer with indentation properties
        Transformer transformer = TransformerFactory.newInstance().newTransformer();
        transformer.setOutputProperty(OutputKeys.INDENT, "yes");
        transformer.setOutputProperty(
                "{http://xml.apache.org/xslt}indent-amount", "4");

        // Convert the DOM back to a string
        StringWriter output = new StringWriter();
        transformer.transform(new DOMSource(document), new StreamResult(output));
        return output.toString();
    }

    private static void removeWhitespaceNodes(Element element) {
        NodeList children = element.getChildNodes();
        for (int i = children.getLength() - 1; i >= 0; i--) {
            Node child = children.item(i);
            if (child instanceof Text && ((Text) child).getData().trim().isEmpty()) {
                element.removeChild(child);
            } else if (child instanceof Element) {
                removeWhitespaceNodes((Element) child);
            }
        }
    }
    
    public static FormType categorizeFormType(Document xmlDoc) throws UnsupportedFormTypeException {
        String role = getNodeValue(xmlDoc, "applicant-role-select");
        String represented = getNodeValue(xmlDoc, "represented-by-lawyer");

        if ("driver".equalsIgnoreCase(role) && "no".equalsIgnoreCase(represented)) {
            return FormType.f1p1;
        } else if ("driver".equalsIgnoreCase(role) && "yes".equalsIgnoreCase(represented)) {
            return FormType.f1p2;
        } else if ("lawyer".equalsIgnoreCase(role) && (represented == null || represented.isEmpty())) {
            return FormType.f1p3;
        } else if ("advocate".equalsIgnoreCase(role) && (represented == null || represented.isEmpty())) {
            return FormType.f1p4;
        } else {
            throw new UnsupportedFormTypeException(
                "Unsupported combination: applicant-role-select = '" + role + "', represented-by-lawyer = '" + represented + "'"
            );
        }
    }
    
    private static String getNodeValue(Document doc, String tagName) {
        NodeList nodes = doc.getElementsByTagName(tagName);
        if (nodes.getLength() > 0 && nodes.item(0).getTextContent() != null) {
            return nodes.item(0).getTextContent().trim();
        }
        return null;
    }


}
