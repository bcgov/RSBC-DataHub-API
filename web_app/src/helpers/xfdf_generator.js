const builder = require('xmlbuilder2');

function generate(pdf_filename, form_key_value_pairs) {

    const base64_encoded_template = encode_template(pdf_filename)
    const xml = get_xml(base64_encoded_template, form_key_value_pairs)
    return new File([xml], "documentElement.xml")

}

function encode_template(pdf_filename) {
    console.log("pdf_filename", pdf_filename)
    const pdf_template = require("@/assets/pdf/" + pdf_filename)
    const base64_string = pdf_template.split(',')[1];
    console.log("pdf_template", base64_string)
    return base64_string
}

function get_xml(base64_encoded_template, form_key_value_pairs) {
    let root = builder.create({version: "1.0", encoding: "UTF-8"})
    .ins("xfa", "generator='AdobeDesigner_V7.0' APIVersion='2.2.4333.0'")
    .ele('xdp:xdp', {'xmlns:xdp': 'http://ns.adobe.com/xdp/'})
        .ele('xfa:datasets', {'xmlns:xfa': 'http://www.xfa.org/schema/xfa-data/1.0/'})
            .ele('xfa:data');
    Object.entries(form_key_value_pairs).forEach( property => {
        console.log("property", property)
        root.ele(property[0]).txt(property[1]);
    });
    root.up()
        .up()
    .ele('pdf', {xmlns: "http://ns.adobe.com/xdp/pdf/"})
    .ele('document')
        .ele('chunk').txt(base64_encoded_template).up()
        .up()
    .up()
    .doc()
    const root_string = root.end({format: 'xml', prettyPrint: true})
    console.log("root_string", root_string )
    return root_string;

}

export default { generate }

