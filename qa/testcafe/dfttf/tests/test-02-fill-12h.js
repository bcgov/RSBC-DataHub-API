import { Selector } from 'testcafe'
import LoginSsoSelectionPage from '../page-objects/pages/LoginSsoSelectionPage'
import BceidLoginPage from '../page-objects/pages/BceidLoginPage'
import DfttfMainPage from '../page-objects/pages/DfttfMainPage'
import Form12h from '../page-objects/pages/Form12h'


// Page object models
const dfttfMainPage = new DfttfMainPage()
const loginSsoSelectionPage = new LoginSsoSelectionPage()
const bceidLoginPage = new BceidLoginPage()
const form12h = new Form12h()

// prettier-ignore
fixture.only `DFTTF 02: officer fills out 12h form`

    .page `process.env.DFTTF_URL.toLowerCase()`


    test ("Officer fills out 12h form", async t=> 
    {
        // BCeID account
        const sso_username = process.env.SSO_BCEID2_USERNAME.toLowerCase()
        const sso_password = process.env.SSO_BCEID2_PASSWORD    

        await t.click(dfttfMainPage.login_button)

        loginSsoSelectionPage.selectBceid()
        bceidLoginPage.login(sso_username, sso_password)

        await t.expect(dfttfMainPage.ui_shown_username.innerText).contains(sso_username)

        

        if (await form12h.button_12h.exists) {
            console.log(" - Found 12-Hour button.")
            await t
            .expect(form12h.button_12h.hasAttribute('disabled')).notOk();
        }
        else {
            console.log(" - No 12-Hour button found.")
        }

        if (await form12h.button_24h.exists) {
            console.log(" - Found 24-Hour button.")
            await t
            .expect(form12h.button_24h.hasAttribute('disabled')).notOk();

        }

        if (await form12h.button_vi.exists) {
            console.log(" - Found VI button.")
            //await t
            //    .expect(button_irp.hasAttribute('disabled')).notOk();
        }

        if (await form12h.button_irp.exists) {
            console.log(" - Found IRP button.")
            await t
                .expect(form12h.button_irp.hasAttribute('disabled')).ok();
        }

        for (let step = 0; step < 50; step++) 
        {

            // Returned to the main page after logging in
            await t
                .wait(5000)
                .click(form12h.button_12h)
                .expect(Selector('#app > div.card-body > div.card.w-100.mt-3.mb-3.border-primary > div.card-header.text-white.bg-secondary.pt-2.pb-0').innerText).contains("Notice of 12 Hour Licence Suspension")
                .click(form12h.driver_jurisdiction)
                .click(Selector ('#drivers_licence_jurisdiction option').withText('British Columbia'))
            
            // Driver information
            await t
                .typeText(form12h.driver_dl_number,"197500" + step, {paste: true, replace: true})
                .typeText(form12h.driver_lastname,"LASTNAMELASTNAME", {paste: true, replace: true})
                .typeText(form12h.driver_firstname,"FIRSTNAMEFIRSTNAME", {paste: true, replace: true})
                .typeText(form12h.driver_dob,"1975-01-01", {paste: true, replace: true})
                .typeText(form12h.driver_address,"100-2345 Somestreet Avenue", {paste: true, replace: true})
                .typeText(form12h.driver_city,"Ashcroft", {paste: true, replace: true})
                .typeText(form12h.driver_postal,"V1V2X2", {paste: true, replace: true})

            // Vehicle information
            await t
                .typeText(form12h.vehicle_plate_number,"ICBC", {paste: true, replace: true})
                .typeText(form12h.vehicle_year,"1929", {paste: true, replace: true})
                .typeText(form12h.vehicle_make,"Ford", {paste: true, replace: true})
                .typeText(form12h.vehicle_model,"Model T", {paste: true, replace: true})
                .typeText(form12h.vehicle_colour,"Black", {paste: true, replace: true})
                .typeText(form12h.vehicle_puj,"B.C.", {paste: true, replace: true})
                .typeText(form12h.vehicle_nsc,"212345678", {paste: true, replace: true})

            // Return of driver's licence
            await t
                .expect(form12h.licence_return_by_mail.exists).notOk()  // Should not be shown by default
                .click(form12h.licence_surrendered_no)
                .expect(form12h.licence_return_by_mail.exists).notOk()  // Not shown until 'Yes' selected
                .click(form12h.licence_surrendered_yes)
                .expect(form12h.licence_return_by_mail.exists).ok()  // Toggle shows licence return fields
                .click(form12h.licence_return_by_mail)
                .click(form12h.licence_return_by_person)
                //.expect(form12h.licence_pickup_address.exists).Ok()  // Not shown until 'Pickup in person' selected
                .typeText(form12h.licence_pickup_address, "123 Pickup Avenue West, Vancouver, B.C., V1V 2V2", {paste: true, replace: true})

            // Vehicle part 1 (disposition)
            await t
                // When Yes is selected, key options are shown, reasons not shown
                .click(form12h.vehicle_towed_yes)
                .expect(form12h.vehicle_keys_vehicle.exists).ok()
                .expect(form12h.vehicle_keys_driver.exists).ok()
                .expect(form12h.vehicle_tow_operator.exists).ok()
                .expect(form12h.vehicle_tow_no_released.exists).notOk()
                .expect(form12h.vehicle_tow_no_left.exists).notOk()
                .expect(form12h.vehicle_tow_no_private.exists).notOk()
                .expect(form12h.vehicle_tow_no_seized.exists).notOk()
                .typeText(form12h.vehicle_tow_operator, "tow")
                .pressKey ("down")
                .pressKey ("down")
                .pressKey ("down")
                .pressKey ("down")
                .pressKey ("down")
                .pressKey ("down")
                .pressKey ("down")
                .pressKey ("down")
                .pressKey ("down")
                .pressKey ("enter")
                .click(form12h.vehicle_keys_driver)
                .click(form12h.vehicle_keys_vehicle)
                .click(form12h.vehicle_towed_yes)

            // Vehicle part 2
            await t
                // When No is selected, reasons are shown, key options are not shown
                .click(form12h.vehicle_towed_no)
                .expect(form12h.vehicle_keys_vehicle.exists).notOk()
                .expect(form12h.vehicle_keys_driver.exists).notOk()
                //.expect(form12h.vehicle_tow_operator.exists).notOk()  // Text fields can't be evaluated
                .expect(form12h.vehicle_tow_no_released.exists).ok()
                .expect(form12h.vehicle_tow_no_left.exists).ok()
                .expect(form12h.vehicle_tow_no_private.exists).ok()
                .expect(form12h.vehicle_tow_no_seized.exists).ok()
                .click(form12h.vehicle_tow_no_seized)
                .click(form12h.vehicle_tow_no_private)
                .click(form12h.vehicle_tow_no_left)
                .click(form12h.vehicle_tow_no_released)
                .typeText(form12h.vehicle_released_to, "Harry Barry Larry Lungpayne, III")
                .typeText(form12h.vehicle_release_date, "20220131")
                .typeText(form12h.vehicle_release_time, "0001")

            // Prohibition
            await t
                .click(form12h.prohibition_type_alcohol)
                .click(form12h.prohibition_type_drugs)
                .typeText(form12h.prohibition_intersection, "Yates Street at Quadra Street")
                .typeText(form12h.prohibition_city, "Ashcroft, B.C.")
                .typeText(form12h.prohibition_file_number, "Form# 1234-567")
                .typeText(form12h.prohibition_date, "20220131")
                .typeText(form12h.prohibition_time, "0002")

            // Officer
            await t
                .typeText(form12h.officer_agency, "3301")
                .typeText(form12h.officer_badge, "AS911")
                .typeText(form12h.officer_lastname, "WRISTPAYNE")

            await t
                .wait(1000)
                // We want to ensure that the form has had a chance to save state before printing
                //.expect(form12h.officer_lastname.value).contains("WRISTPAYNE") 
                .click(form12h.pdf_button)
                .click(form12h.top_home)
        }

        // Wait for a human before ending
        //await t
        //    .debug()
    })
