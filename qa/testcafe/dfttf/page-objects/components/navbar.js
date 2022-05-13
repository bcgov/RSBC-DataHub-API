import { Selector, t } from 'testcafe'

// Import in tests like this:
// --------------------------
// import Navbar from '../page-objects/components/Navbar'
// const navbar = new Navbar()
// Reference with 'navbar.signInButton'
// Call action in code:
// navbar.search('online bank')

class Navbar {
    constructor() {
        // Selectors
        this.searchBox = Selector('#searchTerm')
    }

    // Functions
    async search(text) {
        await t
            .typeText(this.searchBox, text, {paste: true, replace: true })
            .pressKey('enter')
    }
}

export default Navbar