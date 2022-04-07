import { Selector } from 'testcafe'
import DfttfMainPage from '../page-objects/pages/DfttfMainPage'

// Page object models
const dfttfMainPage = new DfttfMainPage()



// prettier-ignore
fixture.skip `DFTTF landing page`
`process.env.DFTTF_URL.toLowerCase()`
    .page 

test("Landing page", async t=> {

    await t.expect(dfttfMainPage.header_logo.exists).ok()
    await t.expect(dfttfMainPage.page_body.exists).ok()
    await t.expect(dfttfMainPage.welcome_message.innerText).contains('Welcome')
    await t.expect(dfttfMainPage.version_header.innerText).eql(dfttfMainPage.expected_version)
        .expect(dfttfMainPage.version_footer.innerText).contains(dfttfMainPage.expected_version)
})