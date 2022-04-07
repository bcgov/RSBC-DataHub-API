import { Selector, t } from 'testcafe'

class LoginSsoSelectionPage {
    constructor() {
        this.bceid_login_button = Selector('#zocial-bceid-business')
        this.github_login_button = Selector('#zocial-github')
        this.idir_login_button = Selector('#zocial-idir')
    }

    async selectBceid() {
        await t
            .expect(this.bceid_login_button.exists, { timeout: 16000 }).ok()
            .click(this.bceid_login_button)
    }

    async selectGitHub() {
        await t
            .expect(this.github_login_button.exists, { timeout: 16000 }).ok()
            .click(this.github_login_button)
    }
    
    async selectIDIR() {
        await t
            .expect(this.idir_login_button.exists, { timeout: 16000 }).ok()
            .click(this.idir_login_button)
    }
}

export default LoginSsoSelectionPage