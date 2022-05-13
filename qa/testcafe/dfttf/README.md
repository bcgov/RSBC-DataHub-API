# TestCafe script for the Digital Forms 12/24 hour prohibition web application

This project uses [TestCafe](https://testcafe.io/) to automate tests that fill out the Digital Form 12/24 hour prohibition web app. TestCafe seems to be a good way to automate tests for the web forms because it does not use Selenium WebDriver and this simplifies test creation and maintenance.

It's important to note here that the Digital Forms web application is not accessible from the internet. You must be connected to the IDIR VPN to access the forms. This complicates testing because the VPN blocks network access to virtual machines and WSL networks when you log on. If your TestCafe runs in WSL or a virtual machine, it will be unable to access the forms without the VPN, but the VPN blocks network access when connected. To get VPN access, TestCafe must be installed on your primary desktop along with the VPN client, or both TestCafe and the AnyConnect VPN client must be installed inside a VM. TestCafe will not be able to reach the Digital Forms if it's running in WSL, and installing AnyConnect inside WSL refuses to connect.

Before you can use this project, you must first:

1. [Install Node.js](https://nodejs.org/en/download/). The basic steps for this are:
    - Follow the steps from the Nodejs.org web site.
    - Update: `npm audit fix --force`
    - Install TestCafe with: `npm install -g testcafe`
    - Optional: install Prettier: ``
1. [Install TestCafe](https://testcafe.io/documentation/402635/getting-started#installing-testcafe).
1. Configure the URL and test user credentials.
    - If you're using Windows, copy `.env.ps1.template` to `.env.ps1` and configure review the variables. 
    - If you're using Linux, copy `.env-template` to `.env` and configure the variables. 
    There is an entry for both these files in `.gitignore` to prevent accidentally committing credentials. 
1. When you're ready to start the test:
    - On Windows, open a PowerShell window and run `.\run-tests.ps1` from the project root.
    - On Linux, open a terminal window and run `./run-tests.sh` from the project root.

## Working with TestCafe

The main configuration script is `.package.json`. That's where you configure the commands to run the TestCafe scripts. See the `scripts` section in .package.json.

TestCafe has project-specific settings in `.testcafe.json`. There should be no need to change this file.

The tests are all kept in the `tests/` folder. Tests are run in alphanumeric order.

## Other stuff

- Prettier is a Node.js plug-in to auto-format JavaScript after you save the source code. It frees you from having to think about how the source code is formatted, and is configured in `prettierrc`.
- The editor you use may pick up its settings from `.editorconfig`.
- There's a book on TestCafe available from Packt here: https://www.packtpub.com/buyitem/index/index/sku/9781800205963. It's not a great introduction, as it dryly walk through many options in the early chapters, but may be a useful reference and does provide useful tips on setting up TestCafe projects for the first time.
- There's a short video introduction to TestCafe on Udemy here: https://www.udemy.com/course/automated-testing-with-testcafe/learn/lecture/14583298#overview. I found this to be a better introduction to TestCafe than the book. It can be difficult to follow, and is missing a section on performance testing, but it does show lots of examples of someone setting up and running TestCafe, and includes recommendations for enhancements and best practices.
- There's a commercial product called [TestCafe Studio](https://www.devexpress.com/products/testcafestudio/) that has a free thirty-day trial. While TestCafe Studio promises to make record-and-playback tests easy to create and maintain, it appears to be very simplistic and may be unsuited for a regression testing with parameterised values. More investigation needed.
