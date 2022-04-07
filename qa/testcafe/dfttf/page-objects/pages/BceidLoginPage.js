import { Selector, t } from 'testcafe'

class BceidLoginPage {
    constructor() {
        this.usernameInput = Selector ('#user')
        this.passwordInput = Selector ('#password')
        this.submitButton = Selector ('.btn-primary')
    }

    async login(username, password) {
        await t
            .typeText(this.usernameInput, username, { paste: true, replace: true })
            .typeText(this.passwordInput, password, { paste: true, replace: true })
            .click(this.submitButton)
    }
}

export default BceidLoginPage