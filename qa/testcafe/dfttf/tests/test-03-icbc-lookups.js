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
fixture.skip `DFTTF 03: ICBC look-ups`

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


        await t
            .wait(5)
            .click(form12h.button_12h)
            .expect(Selector('#app > div.card-body > div.card.w-100.mt-3.mb-3.border-primary > div.card-header.text-white.bg-secondary.pt-2.pb-0').innerText).contains("Notice of 12 Hour Licence Suspension")

        for (let step = 0; step < 5000; step++) 
        {
            // Returned to the main page after logging in
            await t
                .click(form12h.driver_jurisdiction)
                .click(Selector ('#drivers_licence_jurisdiction option').withText('British Columbia'))
            
            await t
                // ICBC driver lookup
                // See https://justice.gov.bc.ca/wiki/pages/viewpage.action?pageId=318901613&moved=true
                // Test DLs:
                // - 1660005 DEAN JOHNSON, 1957-06-18
                // - 1660027 ROSINA FALKUS, 1970-08-28
                // - 1660044 KUO JOZI, 1900-01-01
                // - 1660174 STEVEN BERTRAM, 1909-07-30
                .typeText(form12h.driver_dl_number,"1660174", {paste: true, replace: true})
                .click(form12h.driver_lookup_button)

            // ICBC vehicle lookup
            // See https://justice.gov.bc.ca/wiki/pages/viewpage.action?pageId=318901613&moved=true
            // Plates for testing with individual owners:
            // - LH215R
            // - LH211R
            // - LT016G
            // - LH207R
            // - PR822G
            // Plates for testing with corporate / multiple owners:
            // - LT052G
            // - RH5234
            // - RH5235
            await t
                .typeText(form12h.vehicle_plate_number,"LH215R", {paste: true, replace: true})
                .click(form12h.vehicle_lookup_button)

            await t
                .wait(15000)
        }

        await t
            .click(form12h.top_home)

        // Wait for a human before ending
        await t
            .debug()
    })
