import jsPDF from "jspdf";

const FONT_COLOR = "rgb(0, 0, 128)"

export default {

    async generatePDF(print_definitions, document_types_to_print, form_data, filename) {
        return await new Promise((resolve) => {
          console.log("inside generatePDF()", filename)
          const doc = new jsPDF(
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
        return await new Promise( (resolve) => {
            document_types_to_print.forEach( variant => {
            console.log(variant, print_definitions['variants'][variant])
            print_definitions['variants'][variant]['pages'].forEach( page => {
                this.getPlainImage(page['image']['filename'])
                    // .then( (response) => {
                    //     console.log("response: ", response)
                    //     return new URL(response.responseURL)
                    // })
                    // .then( (url) => {
                    //     console.log("URL_pathname", url.pathname + url.search)
                    //     const image = new Image();
                    //     image.src = url.pathname + url.search
                    //     return image
                    // })
                    // .then( image => {
                    //     setTimeout( () => {return image}, 10000 );
                    // })
                    .then( imgLogo => {
                        if ( page_index > 0 ) {
                            doc.addPage()
                        }
                        doc.setPage(page_index + 1)

                        console.log("imgLogo", imgLogo)
                        doc.addImage(
                            imgLogo,
                            'PNG',
                            page['image']['offset_x'],
                            page['image']['offset_y'],
                            page['image']['width'],
                            page['image']['height'],
                            null );
                        page['fields'].forEach( field => {
                            if (field['field_type'] === 'label') {
                                doc.text(field['name'], field['start']['x'], field['start']['y']);
                            }
                            if (form_data[field['name']]) {
                                doc.setTextColor(FONT_COLOR);
                                doc.setFontSize(field['font_size'])
                                if (field['field_type'] === 'text') {
                                    doc.text(form_data[field['name']], field['start']['x'], field['start']['y']);
                                }
                                if (field['field_type'] === 'checkbox') {
                                    if (form_data[field['name']] === true) {
                                        doc.text("X", field['start']['x'], field['start']['y']);
                                    }
                                }
                                if (field['field_type'] === 'memo') {
                                    doc.text(form_data[field['name']], field['start']['x'], field['start']['y'], {
                                        maxWidth: field['max_width'],
                                        align: 'justify'
                                    });
                                }
                            }
                        })
                        page_index++
                    })
                })
            })
            resolve(doc)
        })
    },

    // async fetchBackgroundImageFromCache(filename) {
    //     return await new Promise( (resolve) => {
    //         const xml_request = new XMLHttpRequest();
    //         try {
    //             xml_request.open("GET", filename, true);
    //             xml_request.onload = function () {
    //                 resolve(xml_request);
    //             }
    //             xml_request.send();
    //         }
    //         catch(error) {
    //
    //             console.log("catch error", error)
    //         }
    //     })
    // },


    async getPlainImage(filename) {
        return await new Promise( (resolve) => {
            const image = new Image();
            try {
                image.src = filename
                resolve(image);
            }
            catch(error) {

                console.log("catch error", error)
            }
        })
    },

}