const vendorId = 0x0801; // MagTek
const productId = 0x0002; // USB Swipe Reader

export default {

    async searchForScanner() {
        // get scanner from list of devices user has granted us access
        console.log("inside searchForScanner()")
        const device_list = await navigator.hid.getDevices();
        return device_list.find(d => d.vendorId === vendorId && d.productId === productId);
    },

    async connectToScanner() {
        // ask user for permission to access hardware scanner
        console.log("inside connectToScanner()")
        let devices = await navigator.hid.requestDevice({
            filters: [{
                vendorId,
                productId
            }],
        });
        console.log("openDevice(): device list", devices);
        return devices[0];
    },

    // asynchronously get the scanner
    async getScanner() {

        let scanner = await this.searchForScanner();
        if (! scanner ) {
            scanner = await this.connectToScanner();
        }
        return scanner;
    },
    
    async readFromScanner(scanner) {
        try {
            scanner.oninputreport = ({
                device,
                reportId,
                data
            }) => {
                console.log(`readDataFromScanner(): Received input report ${reportId} from ${device.productName}`);
                var magStripe = String.fromCharCode.apply(null, new Uint8Array(data.buffer)); // convert BufferSource into string
                console.log("mag stripe: " + magStripe);
                return magStripe;
            };
        } catch (error) {
            console.error("readDataFromScanner(): failed", error);
        }
    },

    // parse AAMVA 2009 data (NB: no track 3 support - not required for RSI Digital Forms project)
    parseAAMVA2009(magStripe) {

        // remove new lines from data
        magStripe = magStripe.replace(/\n/, "");

        // replace all whitespace characters (e.g. tabs) with regular space
        magStripe = magStripe.replace(/\s/g, " ");

        // try parsing for three tracks
        var tracks = magStripe.match(/%(.+)\?.*;(.+)\?.*%(.+)\?/);

        if (tracks) {
            tracks = magStripe.match(/%(.+)\?.*;(.+)\?/);
        }

        // province, city, name: [surname, given name], address: [street, city, province, postal code]
        var track1 = tracks[1].match(/([A-Z]{2})([^^]{0,13})\^?([^^]{0,35})\^?([^^]{0,74})/);

        // ISO Issuer Identification Number, DL number, DL expiration, date of birth
        var track2 = tracks[2].match(/(\d{6})(\d{0,13})(=)(\d{4})(\d{8})(\d{0,5})/);

        //	console.log("track1: >>>" + tracks[1] + "<<<");
        //	console.log("track2: >>>" + tracks[2] + "<<<");
        //	console.log("track3: >>>" + tracks[3] + "<<<");

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