import { Selector, t } from 'testcafe'

class DfttfMainPage {
    constructor() {
        this.header_logo = Selector('#roadsafety-header > div > a')
        this.page_body = Selector ("#app > div.card-body > div:nth-child(1)")
        this.welcome_message = Selector("div.card-body:nth-child(1)")
        this.version_header = Selector('#roadsafety-header span');
        this.version_footer = Selector('#app div');
        this.login_button = Selector('.btn-primary')
        this.expected_version = '0.1.88'

        // Username in top banner (e.g. "User user1@bceid-business")
        this.ui_shown_username = Selector('#roadsafety-header > div > div > div.mt-auto.small')
        // Grey message box (e.g. "Welcome! It looks like you haven't used this app before.")
        //this.logged_in_welcome_message = Selector('#app div')
        this.logged_in_welcome_message = Selector('#app > div.card-body > div:nth-child(1) > div > div')
        this.logged_in_footer = Selector ('#app > div.card-body > div.card-footer.bg-transparent.border-0.text-muted.small')
        this.unlock_prompt = Selector('#app > div.card-body > div:nth-child(1) > div > div > span.small')
        this.unlock_link = Selector('#app > div.card-body > div:nth-child(1) > div > div > span.small > span')
        this.apply_form = Selector('.form-inline')
        
        this.keycloak_username = Selector('#keycloak_username')
        this.apply_button = Selector('#app button').withText('Apply')

        this.page_body_small_text = Selector('#app > div.card-body > div:nth-child(1) > div > div > span.small')
        this.page_body_muted_text = Selector('#app > div.card-body > div:nth-child(1) > div > div > div')
    }
}

export default DfttfMainPage