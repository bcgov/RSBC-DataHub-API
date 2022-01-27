const supportedScanners = [
    {vendorId: 0x0801, productId: 0x0002},  // MagTek - USB Swipe Reader
    {vendorId: 0x0980, productId: 0x91f0}   // Posh Manufacturing - MX5-K9
]

export default {

    async getScanner() {
        // get scanner from list of scanners user has granted us access
        console.log("inside searchForScanner()")
        const device_list = await navigator.hid.getDevices();
        return device_list[0];
    },

    async requestAccessToScanner() {
        // ask user for permission to access hardware scanner
        console.log("inside connectToScanner()")
        let devices = await navigator.hid.requestDevice({
            filters: supportedScanners,
        });
        console.log("openDevice(): device list", devices);
        return devices[0];
    },

    // asynchronously get the scanner
    async openScanner() {
        let scanner = await this.getScanner();
        if (! scanner ) {
            scanner = await this.requestAccessToScanner();
        }

        if (scanner.opened) {
            return scanner;
        } else {
            await scanner.open()
            return scanner;
        }
    },
    
    async readFromScanner(device, reportId, data) {
        console.log(`readDataFromScanner(): Received input report ${reportId} from ${device.productName}`);
        var magStripe = String.fromCharCode.apply(null, new Uint8Array(data.buffer)); // convert BufferSource into string
        return this.parseAAMVA2009(magStripe)
    },

    // parse AAMVA 2009 data (NB: no track 3 support - not required for RSI Digital Forms project)
    // See: https://www2.gov.bc.ca/assets/gov/health/practitioner-pro/medical-services-plan/teleplan-ch4.pdf
    parseAAMVA2009(magStripe) {

        let tracks = magStripe.split("?")

        // province, city, name: [surname, given name], address: [street, city, province, postal code]
        const track1 = tracks[0].match(/%([A-Z]{2})([^^]{0,13})\^?([^^]{0,35})\^?([^^]{0,74})?/);

        // ISO Issuer Identification Number, DL number, DL expiration, date of birth
        var track2 = tracks[1].match(/;(\d{6})(\d{0,13})(=)(\d{4})(\d{8})(\d{0,5})?/);

        var province = track1[1];
        var city = track1[2];
        var name = track1[3].match(/([^$]{0,35}),\$?([^$]{0,35})?/);
        var address = track1[4].match(new RegExp("^(.+)\\$(.+)\\s(" + province + ")\\s*(.{6,7})$"));

        return {
            // track 1
            "province": province,
            "city": city,
            "name": function () {
                if (!name) return;
                return {
                    surname: name[1],
                    given: name[2],
                }
            }(),
            "address": function () {
                if (!address) return;
                return {
                    street: address[1],
                    city: address[2],
                    province: address[3],
                    postalCode: address[4]
                }
            }(),
            // track 2
            "iso_iin": track2[1],
            "number": track2[2],
            "expiration": this.parseDate(track2[4]),
            "dob": function () {
                var dob = track2[5].match(/(\d{4})(\d{2})(\d{2})/);
                if (!dob) return;
                return dob[1] + dob[2] + dob[3];
            }()
        };
    },

    // parse date into a string (yyyymmdd)
    parseDate(date) {
        var start = parseInt(date[0] + date[1]);
        if (start < 13) {
            return date[4] + date[5] + date[6] + date[7] + date[0] + date[1] + date[2] + date[3];
        }
        return date;
    }

}