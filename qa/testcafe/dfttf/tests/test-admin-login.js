import { Selector } from 'testcafe'
import LoginSsoSelectionPage from '../page-objects/pages/LoginSsoSelectionPage'
import BceidLoginPage from '../page-objects/pages/BceidLoginPage'
import DfttfMainPage from '../page-objects/pages/DfttfMainPage'


// Page object models
const dfttfMainPage = new DfttfMainPage()
const loginSsoSelectionPage = new LoginSsoSelectionPage()
const bceidLoginPage = new BceidLoginPage()

// prettier-ignore
fixture.skip `DFTTF admin login`

    .page `process.env.DFTTF_URL.toLowerCase()`


    test ("Admin deletes existing test officer", async t=> 
    {
        // BCeID account
        const sso_username = process.env.SSO_IDIR_USERNAME.toLowerCase()
        const sso_password = process.env.SSO_IDIR_PASSWORD    
        const officer_to_clean_up = process.env.SSO_IDIR_USERNAME.toLowerCase()

        await t.click(dfttfMainPage.login_button)

        loginSsoSelectionPage.selectIDIR()
        bceidLoginPage.login(sso_username, sso_password)

        // Returned to the main page after logging in
        await t.expect(dfttfMainPage.ui_shown_username.innerText).contains(sso_username)
            .click('#roadsafety-header > div > div > div.mt-auto.small > a > span')

        const officer_row = Selector('#app > div.card-body > div.card.w-100.mt-3.mb-3 > div.card-body.text-left.pb-1 > table > tbody').find('td').withText(officer_to_clean_up + '@bceid-business')
        const officer_approve_button = officer_row.sibling('td').find('button').withText('Approve')
        const officer_delete_button = officer_row.sibling('td').find('button').withText('Delete')

        if (await officer_row.exists) {
            console.log(" - Found officer " + officer_to_clean_up + "...")
            if (await officer_approve_button.exists) {
                //console.log("Found an approve button. Clicking it...")
                await t.click(officer_approve_button)
            }
    
            if (await officer_delete_button.exists) {
                //console.log("Found a delete button. Clicking it...")
                await t.click(officer_delete_button)
            }
        }
        else {
            console.log(" - Officer " + officer_to_clean_up + " not signed up.")
        }
    })
