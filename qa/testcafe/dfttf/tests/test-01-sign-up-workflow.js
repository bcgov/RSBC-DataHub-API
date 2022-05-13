import { Selector } from 'testcafe'
import LoginSsoSelectionPage from '../page-objects/pages/LoginSsoSelectionPage'
import BceidLoginPage from '../page-objects/pages/BceidLoginPage'
import DfttfMainPage from '../page-objects/pages/DfttfMainPage'


// Page object models
const dfttfMainPage = new DfttfMainPage()
const loginSsoSelectionPage = new LoginSsoSelectionPage()
const bceidLoginPage = new BceidLoginPage()

// prettier-ignore
fixture.skip `DFTTF 01: officer sign-up workflow`

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

    test ("Officer SSO BCeID sign-up", async t=> 
    {
        // BCeID account
        const sso_username = process.env.SSO_BCEID2_USERNAME.toLowerCase()
        const sso_password = process.env.SSO_BCEID2_PASSWORD    

        await t.click(dfttfMainPage.login_button)

        loginSsoSelectionPage.selectBceid()
        bceidLoginPage.login(sso_username, sso_password)

        // Returned to the main page after logging in
        await t.expect(dfttfMainPage.ui_shown_username.innerText).contains(sso_username)
            .expect(dfttfMainPage.logged_in_welcome_message.innerText).contains("you haven't used this app before.")
            .expect(dfttfMainPage.logged_in_footer.innerText).contains(dfttfMainPage.expected_version)
            .expect(dfttfMainPage.unlock_prompt.innerText).contains("Until you're authorized, this app is disabled.")
            .expect(dfttfMainPage.unlock_link.innerText).contains("Unlock")
            .expect(dfttfMainPage.apply_form.exists).notOk()  // Form should not be visible until Unlock is selected
            
            // Unlock the application button
            .click(dfttfMainPage.unlock_link)
            .expect(dfttfMainPage.apply_form.exists).ok()

            // Click the application button (username will show up in DFTTF admin page with "Approve" button)
            .click(dfttfMainPage.apply_button)
            .expect(dfttfMainPage.page_body_small_text.innerText).contains("Until you\'re authorized, this app is disabled.")
            .expect(dfttfMainPage.page_body_muted_text.innerText).contains("Waiting for the administrator to unlock")
    })

    test ("Admin approves new officer application", async t=> 
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
        
        await t.click(officer_approve_button)
    })