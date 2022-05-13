import { Selector, t } from 'testcafe'

class Form12h {
    constructor() {

        // Header
        this.top_home = Selector ('#roadsafety-header div a img')

        // Buttons
        this.button_12h = Selector('a').withText('New 12Hour Form');
        this.button_24h = Selector('#app a').withText('New 24Hour Form');
        this.button_vi  = Selector('#app a').withText('New VI Form');
        this.button_irp = Selector('#btn-primary').withText('New IRP Form');
    
        // Driver fields
        this.driver_jurisdiction =  Selector ('#drivers_licence_jurisdiction')
        this.driver_jurisdiction_option =  Selector ('#drivers_licence_jurisdiction option')
        this.driver_dl_number =     Selector ('#drivers_number')
        this.driver_lookup_button = Selector ('#app button').withText("Driver's Lookup")
        this.driver_lastname =      Selector ('#last_name')
        this.driver_firstname =     Selector ('#first_name')
        this.driver_dob =           Selector ('#dob')
        this.driver_address =       Selector ('#address1')
        this.driver_city =          Selector ('.form-control').nth(6)
        //this.driver_province =      Selector ('')
        this.driver_postal =        Selector ('#postal')

        // Vehicle fields
        this.vehicle_jurisdiction = Selector ('#plate_province')
        this.vehicle_plate_number = Selector ('#plate_number')
        this.vehicle_lookup_button = Selector ('#app button').withText('ICBC Lookup')
        this.vehicle_year =         Selector ('.form-control').nth(14)
        this.vehicle_make =         Selector ('.form-control').nth(15)
        this.vehicle_model =        Selector ('.form-control').nth(16)
        this.vehicle_colour =        Selector ('.form-control').nth(18)
        this.vehicle_puj =          Selector ('#puj_code')
        this.vehicle_nsc =          Selector ('#nsc_number')

        // Return of driver's licence
        this.licence_surrendered_yes = Selector('#licence_surrendered')
        this.licence_surrendered_no = Selector('[name="licence_surrendered"]').nth(1)
        this.licence_return_by_mail    = Selector ('#return_of_licence')
        this.licence_return_by_person =  Selector ('[name="return_of_licence"]').nth(1)
        this.licence_pickup_address = Selector ('.form-control').nth(22)

        // Vehicle disposition
        this.vehicle_towed_yes =  Selector ('#vehicle_towed')
        this.vehicle_towed_no =  Selector ('[name="vehicle_towed"]').nth(1)
        this.vehicle_keys_vehicle = Selector ('#location_of_keys')
        this.vehicle_keys_driver = Selector ('[name="location_of_keys"]').nth(1)
        this.vehicle_tow_operator = Selector ('.form-control').nth(23)
        this.vehicle_tow_no_released = Selector ('#reason_for_not_towing')
        this.vehicle_tow_no_left = Selector ('[name="reason_for_not_towing"]').nth(1)
        this.vehicle_tow_no_private = Selector ('[name="reason_for_not_towing"]').nth(2)
        this.vehicle_tow_no_seized = Selector ('[name="reason_for_not_towing"]').nth(3)
        this.vehicle_released_to = Selector('#vehicle_released_to')
        this.vehicle_release_date = Selector('#datetime_released')
        this.vehicle_release_time = Selector('#app .form-control').nth(25)

        // Prohibition
        this.prohibition_type_alcohol = Selector ('#prohibition_type_12hr')
        this.prohibition_type_drugs = Selector('[name="prohibition_type_12hr"]').nth(1)
        this.prohibition_intersection = Selector('#offence_address')
        this.prohibition_city = Selector ('.form-control').nth(27)
        this.prohibition_file_number = Selector('#file_number')
        this.prohibition_date = Selector('#prohibition_start_time')
        this.prohibition_time = Selector('.form-control').nth(30)

        // Officer
        this.officer_agency = Selector ('#agency')
        this.officer_badge = Selector ('#badge_number')
        this.officer_lastname = Selector ('#officer_name')

        this.pdf_button = Selector('#app button').withText("PDF")
        
    }

    async clickJurisdiction() {
        await t
            .click(this.driver_jurisdiction)
    }
}

export default Form12h