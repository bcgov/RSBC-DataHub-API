import jsPDF from "jspdf";

const FONT_COLOR = "rgb(0, 0, 128)"

export default {

    async generatePDF(print_definitions, document_types_to_print, form_data, filename) {
        return await new Promise((resolve) => {
          console.log("inside generatePDF()", filename)
          let doc = new jsPDF(
              print_definitions['orientation'],
              print_definitions['units'],
              print_definitions['dimensions'],
              true);
          let page_index = 0
          this.buildPdfVariants(doc, document_types_to_print, print_definitions, page_index, form_data)
              .then( (doc) => {
                  resolve(doc.save(filename));
              })
        })
    },

    async buildPdfVariants(doc, document_types_to_print, print_definitions, page_index, form_data) {
        for (const variant of document_types_to_print) {
            console.log("A:", variant, print_definitions['variants'][variant], doc)
            doc = await this.buildPages(doc,print_definitions, variant, page_index, form_data)
            page_index++
        }
        return doc;
    },


    async buildPages(doc, print_definitions, variant, page_index, form_data) {
        for (const page of print_definitions['variants'][variant]['pages']) {
            console.log("doc", doc)
            await this.fetchCacheName(page['image']['filename'])
                .then( (response) => {
                    console.log("B - got response");
                    return new URL(response.responseURL)
                })
                .then( (url) => {
                    console.log("C - URL_pathname", url.pathname + url.search)
                    let imgLogo = new Image();
                    imgLogo.src = url.pathname + url.search
                    return imgLogo;
                })
                .then( (imgLogo) => {
                    console.log("D - imgLogo", imgLogo)
                    if ( page_index > 0 ) {
                        doc.addPage()
                    }
                    doc.setPage(page_index + 1)
                    return doc.addImage(
                                imgLogo,
                                'PNG',
                                page['image']['offset_x'],
                                page['image']['offset_y'],
                                page['image']['width'],
                                page['image']['height'],
                                null
                            )
                })
                .then((doc) => {
                     page['show_fields'].forEach( field => {
                         let field_definition = print_definitions['fields'][field]
                         console.log("field_definition", field_definition, field)
                        if (field_definition['field_type'] === 'label') {
                            doc.text(field, field_definition['start']['x'], field_definition['start']['y']);
                        }
                        if (form_data[field]) {
                            doc.setTextColor(FONT_COLOR);
                            doc.setFontSize(field_definition['font_size'])
                            if (field_definition['field_type'] === 'text') {
                                doc.text(form_data[field], field_definition['start']['x'], field_definition['start']['y']);
                            }
                            if (field_definition['field_type'] === 'checkbox') {
                                if (form_data[field] === true) {
                                    doc.text("X", field_definition['start']['x'], field_definition['start']['y']);
                                }
                            }
                            if (field_definition['field_type'] === 'memo') {
                                doc.text(form_data[field], field_definition['start']['x'], field_definition['start']['y'], {
                                    maxWidth: field_definition['max_width'],
                                    align: 'justify'
                                });
                            }
                        }
                    })
                    return doc;
                })
                .then( () => {
                    page_index++
                })
            } // end of for loop
        return doc;
    },



    async downloadImage(imageUrl) {
        return await new Promise( (resolve) => {
            console.log("URL_pathname", imageUrl.pathname + imageUrl.search)
            const image = new Image();
            image.src = imageUrl.pathname + imageUrl.search;
            image.onload = function() {
                resolve(image);
            }
        })
    },

    async fetchCacheName(filename) {
        return await new Promise( (resolve) => {
            const xml_request = new XMLHttpRequest();
            try {
                xml_request.open("GET", filename, true);
                xml_request.onload = function () {
                    console.log("fetchCacheName() - about to resolve")
                    resolve(xml_request);
                }
                xml_request.send();
            }
            catch(error) {
                console.log("catch error", error)
            }
        })
    },

}