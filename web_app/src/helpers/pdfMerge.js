import jsPDF from "jspdf";
import checkDigit from "./checkDigit";
import {font}  from "./BCSans-Regular-normal";
import moment from "moment-timezone";
import constants from "../config/constants";
import {barcode_font}  from "./LibreBarcode39-Regular-normal";

const FONT_FILE = "bc_sans.ttf"
const FONT = "BC_SANS"
const FONT_COLOR = "rgb(0, 0, 128)"
const BARCODE_FILE = "code39.ttf"
const BARCODE = "code39"
const DEFAULT_FONT = "Helvetica"
const PUBLIC_PATH = process.env.BASE_URL


export default {

    async generatePDF(print_definitions, document_types_to_print, form_data, filename, form_type) {
        return await new Promise((resolve) => {
          console.log("inside generatePDF()", filename, document_types_to_print)
          let doc = new jsPDF({
              orientation: print_definitions['orientation'],
              units: print_definitions['units'],
              format: print_definitions['format'],
              putOnlyUsedFonts: true,
              compress: true
          });
          doc.addFileToVFS(FONT_FILE, font);
          doc.addFont(FONT_FILE, FONT, "normal");
          doc.setFont(FONT);
          doc.addFileToVFS(BARCODE_FILE, barcode_font);
          doc.addFont(BARCODE_FILE, BARCODE, "normal");
          doc.setTextColor(FONT_COLOR);
          let page_index = 0
          this.buildPdfVariants(doc, document_types_to_print, print_definitions, page_index, form_data, form_type)
              .then( (doc) => {
                  resolve(doc.save(filename));
              })
        })
    },

    async buildPdfVariants(doc, document_types_to_print, print_definitions, page_index, form_data, form_type) {
        for (const variant of document_types_to_print) {
            console.log("A:", variant, print_definitions['variants'][variant], doc)
            doc = await this.buildPages(doc,print_definitions, variant, page_index, form_data, form_type)
            page_index++
        }
        return doc;
    },


    async buildPages(doc, print_definitions, variant, page_index, form_data, form_type) {
        for (const page of print_definitions['variants'][variant]['pages']) {
            console.log("doc", doc)
            await this.fetchCacheName(PUBLIC_PATH + page['image']['filename'])
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
                                '',
                                'FAST'
                            )
                })
                .then((doc) => {
                     page['show_fields'].forEach( field => {

                         if (field in print_definitions['fields']) {
                             let field_definition = print_definitions['fields'][field]
                             console.log("field_definition", field, field_definition, form_data)

                             doc.setFontSize(field_definition['font_size'])

                             if (field_definition['field_type'] === 'label') {
                                 doc.text(field_definition['value'], field_definition['start']['x'], field_definition['start']['y']);
                             }

                             // temporary kludge while refactoring
                             let display_value = ''
                             if(form_type === "VI") {
                                 display_value = this[field_definition['function']](form_data, field_definition['parameters'])
                             } else {
                                 if (form_data[field]) {
                                     display_value = form_data[field]
                                 }
                             }

                             console.log("render_field_value", display_value)
                             if (field_definition['field_type'] === 'text') {
                                 doc.setFont(DEFAULT_FONT);
                                 doc.text(display_value, field_definition['start']['x'], field_definition['start']['y'])
                             }
                             if (field_definition['field_type'] === 'checkbox') {
                                 if (display_value === true) {
                                     doc.setFont(DEFAULT_FONT);
                                     doc.text("X", field_definition['start']['x'], field_definition['start']['y']);
                                 }
                             }
                             if (field_definition['field_type'] === 'memo') {
                                 doc.setFont(DEFAULT_FONT);
                                 doc.text(display_value, field_definition['start']['x'], field_definition['start']['y'], {
                                     maxWidth: field_definition['max_width'],
                                     align: 'justify'
                                 });
                             }

                             if (field_definition['field_type'] === 'barcode') {
                                  doc.setFont(BARCODE)
                                  doc.text(display_value, field_definition['start']['x'], field_definition['start']['y']);
                             }


                         } else {
                             console.log("print_layout.json is missing", field)
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

    getFormattedFormId(form_data) {
        if ("form_id" in form_data) {
            const sixDigitString = form_data.form_id.substr(2,7)
            const digit = checkDigit.checkDigit(sixDigitString)
            return form_data.form_id.substr(0,2) + "-" + sixDigitString + digit
        }
        return ''
    },

    getFormIdForBarCode(form_data) {
        if ("form_id" in form_data) {
            const sixDigitString = form_data.form_id.substr(2,7)
            const digit = checkDigit.checkDigit(sixDigitString)
            return "*" + sixDigitString + digit + "*"
        }
        return ''
    },

    getStringValue(form_data, attribute) {
        if (attribute in form_data.data) {
            return form_data.data[attribute].toUpperCase()
        }
        return ''
    },

    getDateValue(form_data, attribute) {
        if (attribute in form_data.data) {
            const date_time = moment(form_data.data[attribute], 'YYYYMMDD', true)
            return date_time.format("YYYY-MM-DD")
        }
        return ''
    },

    getDateTimeValue(form_data, date_and_time_array) {
        if (date_and_time_array[0] in form_data.data && date_and_time_array[1] in form_data.data) {
            const date_time_string = form_data.data[date_and_time_array[0]] + " " + form_data.data[date_and_time_array[1]]
            const date_time = moment.tz(date_time_string, 'YYYYMMDD HHmm', true, constants.TIMEZONE)
            return date_time.format("YYYY-MM-DD")
        }
        return ''
    },

    getJurisdictionCode(form_data, attribute) {
        if (attribute in form_data.data) {
            if ('objectCd' in form_data.data[attribute]) {
                return form_data.data[attribute].objectCd
            }
        }
        return ''
    },

    getValuesConcatenatedWithCommas(form_data, attributes_array) {
        let attributeValues = []
        attributes_array.forEach( (attribute) => {
            if (attribute in form_data.data) {
                attributeValues.push(form_data.data[attribute])
            }
        })
        return attributeValues.join(", ")
    },

    getPhoneAreaCodeValue(form_data, attribute) {
        if (attribute in form_data.data) {
            return form_data.data[attribute].substr(0, 3)
        }
        return ''
    },

    getPhoneValue(form_data, attribute) {
        if (attribute in form_data.data) {
            return form_data.data[attribute].substr(3,3) + "-" + form_data.data[attribute].substr(6,9)
        }
        return ''
    },

    getSubStringValue(form_data, [attribute, start, end]) {
        if (attribute in form_data.data) {
            return form_data.data[attribute].substr(start,end)
        }
        return ''
    },

    getIsChecked(form_data, [attribute, expectedValue]) {
        if (attribute in form_data.data) {
            return form_data.data[attribute].includes(expectedValue)
        }
        return false
    },

    getRadioValue(form_data, [attribute, expectedValue]) {
        if (attribute in form_data.data) {
            return (form_data.data[attribute] === expectedValue);
        }
        return false;
    },

    getImpoundLotOperator(form_data, key) {
        if ("impound_lot_operator" in form_data.data) {
            const ilo = form_data.data.impound_lot_operator
            if (key in ilo) {
                return ilo[key].toUpperCase();
            }
        }
        return '';
    },

    getIsFieldPopulated(form_data, attribute) {
        if (attribute in form_data.data) {
            return (form_data.data[attribute].length > 0)
        }
        return false
    },

    // print static text to the printout
    label(form_data, label_text) {
        return label_text
    },

    // --- methods below are being used as a temporary workaround until refactoring --- //

    isJurisdictionBC(form_data) {
        const attribute = "drivers_licence_jurisdiction"
        if (attribute in form_data.data) {
            if ('objectCd' in form_data.data[attribute]) {
                return (form_data.data[attribute].objectCd === "BC");
            }
        }
        return false;
    },

    isUnlicensed(form_data) {
        const attribute = "reason_unlicensed"
        if (attribute in form_data.data) {
            return (form_data.data[attribute] === true);
        }
        return false;
    },

    getJurisdictionIfUnlicensed(form_data, attribute) {
        if(this.isJurisdictionBC(form_data) && this.isUnlicensed(form_data)) {
            if(attribute in form_data.data) {
                if ("objectCd" in form_data.data[attribute]) {
                    return form_data.data[attribute].objectCd
                }
                return ''
            }
        }
        return ''
    },

    getStringIfUnlicensed(form_data, attribute) {
        console.log("getStringIfUnlicensed()", this.isJurisdictionBC(form_data), this.isUnlicensed(form_data))
        if(this.isJurisdictionBC(form_data) && this.isUnlicensed(form_data)) {
            if(attribute in form_data.data) {
                return form_data.data[attribute]
            }
        }
        return ''
    },

    getUnlicensedAndOutOfProvince(form_data) {
        return this.isJurisdictionBC(form_data) && this.isUnlicensed(form_data)
    }

}