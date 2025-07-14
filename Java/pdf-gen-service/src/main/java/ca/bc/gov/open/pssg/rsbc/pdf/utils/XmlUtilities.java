package ca.bc.gov.open.pssg.rsbc.pdf.utils;

import java.io.StringReader;
import java.io.StringWriter;
import java.util.EnumSet;

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

/**
 * 
 * XML Utilities for parsing an APR XML Payload. 
 * 
 */
public class XmlUtilities {
	
    public enum FormType {
        f1p1, // form 1, permutation 1, driver no lawyer
        f1p2, // form 1, permutation 2, driver obtained Lawyer
        f1p3, // form 1, permutation 3, Lawyer Office
        f1p4, // form 1, permutation 4, Authorized Person
        f3p1,   // form 3, driver permutation
        f3p2,   // form 3, law office permutation
        f3p3,   // form 3, advocate permutation
        UNKNOWN // unknown form 1 permutation. 
    }
    
    public enum XDPType {
    	Form_1_P1,
    	Form_1_P2,
    	Form_1_P3,
    	Form_1_P4,
    	Form_3_driver,
    	Form_3_law_office,
    	Form_3_advocate,
        UNKNOWN
    }
    
    /**
     * 
     * Form Type to XDP name conversion. 
     * 
     * @param formType
     * @return
     */
    public static XDPType toXDPType(FormType formType) {
        if (formType == null) {
            return XDPType.UNKNOWN;
        }

        switch (formType) {
            case f1p1: return XDPType.Form_1_P1;
            case f1p2: return XDPType.Form_1_P2;
            case f1p3: return XDPType.Form_1_P3;
            case f1p4: return XDPType.Form_1_P4;
            case f3p1: return XDPType.Form_3_driver;
            case f3p2: return XDPType.Form_3_law_office;
            case f3p3: return XDPType.Form_3_advocate;
            case UNKNOWN:
            default:   
            	return XDPType.UNKNOWN;
        }
    }
    
    private static final EnumSet<FormType> F3_PERMUTATIONS = EnumSet.of(FormType.f3p1, FormType.f3p2, FormType.f3p3);

    public static boolean isFormTypeF3Permutation(FormType formType) {
        return F3_PERMUTATIONS.contains(formType);
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
    
    /**
     * Categorize the incomming for type. 
     * 
     * Return FormType.UNKNOWN if indescribable.  
     * 
     * @param xmlDoc
     * @return
     */
	public static FormType categorizeFormType(Document xmlDoc) {

		try {

			// test for form 1
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
				
				//TODO - complete this for form3
//				String evidenceSection = getNodeValue(xmlDoc, "evidence-section");
//				if (evidenceSection != null)
//					return FormType.f3;
//				else
					return FormType.UNKNOWN;
			}

		} catch (Exception ex) {
			return FormType.UNKNOWN;
		}
	}
	
	
    
    private static String getNodeValue(Document doc, String tagName) {
        NodeList nodes = doc.getElementsByTagName(tagName);
        if (nodes.getLength() > 0 && nodes.item(0).getTextContent() != null) {
            return nodes.item(0).getTextContent().trim();
        }
        return null;
    }
    
    private static String getAttributeValue(Document doc, String nodeName, String attributeName) {
        NodeList nodeList = doc.getElementsByTagName(nodeName);
        if (nodeList.getLength() > 0) {
            Node node = nodeList.item(0);
            if (node.getNodeType() == Node.ELEMENT_NODE) {
                Element element = (Element) node;
                return element.getAttribute(attributeName);
            }
        }
        return null;
    }

	public static String getNoticeNumber(Document doc) {
		return getNodeValue(doc, "prohibition-number-clean");
	}
	
	public static String getApplicantEmailAddress(Document doc) {
		return getNodeValue(doc, "applicant-email-address");
	}

	public static String getConsentFormData(Document doc) {
		return getAttributeValue(doc, "consent-upload", "data");
	}
}
