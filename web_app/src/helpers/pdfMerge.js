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
          document_types_to_print.forEach( variant => {
            console.log(variant, print_definitions['variants'][variant])
            print_definitions['variants'][variant]['pages'].forEach( page => {
                if ( page_index > 0 ) {
                    doc.addPage()
                }
                doc.setPage(page_index + 1)
                let imgLogo = new Image()
                imgLogo.src = `${page['image']['filename']}`
                doc.addImage(
                imgLogo,
                'PNG',
                page['image']['offset_x'],
                page['image']['offset_y'],
                page['image']['width'],
                page['image']['height'],
                null )
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
          resolve(doc.save(filename));
        })

    }

}