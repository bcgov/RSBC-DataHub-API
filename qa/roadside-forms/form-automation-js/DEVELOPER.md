# Form fill automation for Vue.js projects

This is a JavaScript project to automate the Digital Forms (12-hour, 24-hour, IRP, VI). It uses a local web server to serve scripts, a free Chrome extension to load the automation into your web browser when the form loads. Then you can press hotkeys or click buttons on the web page to fill out the form.

This automation was created to save time when working with roadside forms. Many form-filling features and extensions are unable to fill RSI's digital forms because Vue.js has custom (complicated) form objects.

For now, this works well on complex Vuex elements, and allows individual sections or the entire form to be filled out programmatically with JavaScript, using the browser's own rendering engine.

## How it works

The form is a single-page Vue app, and the [Requestly browser extension](https://requestly.io/) injects JavaScript onto the page after it loads. There are many ways to inject code onto a page using extensions (eg. [TamperMonkey](https://www.tampermonkey.net/)/[ViolentMonkey](https://violentmonkey.github.io/), [Autofill](https://chrome.google.com/webstore/detail/autofill/nlmmgnhgdeffjkdckmikfpnddkbbfkkk)) or proxies (eg. [Fiddler](https://www.telerik.com/fiddler), or [mitmproxy](https://mitmproxy.org/)). Requestly seems good because it has a nice interface and can also mock API calls. The code injected by Requestly sits on the local file system (checked out from git, but could be loaded raw from GitHub?) and is currently served by a [PowerShell local web server](https://github.com/MScholtes/WebServer).

This setup is ideal because it allows the automation to be used by a tester, developer, or product owner in a browser while manually working with the form, and also used in an automated system to run end-to-end regression test (eg. Cypress, TestCafe, Power Automate, maybe even Selenium WebDriver). Previously, I was maintaining two separate automations: one for human use, one for end-to-end testing.

The inspiration comes from my observation that modern test frameworks and tools run in the browser engine as JavaScript, rather than simulating user interface events with the WebDriver protocol.

## Model, view, controller

There are three JavaScript files injected onto the page when it loads:

1. A model: test objects, one object for each scenario. Each object is broken down by form section (e.g. driver section, vehicle section, registration section), with values for each field in a section.
2. A view: Buttons and labels overlaid on the page, giving a visual indication that the script has loaded, and allowing different actions to be triggered either with a click or hotkey.
3. A controller: code for simulating events for filling out the form.

## Automating Vuex element interactions

Different Vuex elements require different approaches. The following examples are simplified, but show how each web form element can be filled programmatically.

### Plain text fields

For a basic text field, you set the element value, then trigger an input event. For example:

```javascript
texfield = document.getElementById(field_id);
texfield.value  = "ABC123";
await texfield.dispatchEvent(new Event('input'));
```

### Radio buttons

Radio buttons don't need an event triggered. Clicking the button object is enough to make Vuex to update its model. For example:

```javascript
document.getElementById(field_id).click();
```

### Checkboxes

Checkboxes are toggles and like radio buttons, there is no need need to trigger an event after toggling. You need to check the state beforehand though, and toggle only when needed:

```javascript
checkbox = document.getElementsById(field_id);
if (checkbox.checked == false) 
{
   checkbox.click()
}
```

### Multiselects

These complex elements offer a selection of values from drop-down control, plus type-ahead selection and multiple selections. This was the most complex of the Vuex controls, and where I spent the most time experimenting and reverse-engineering.

```javascript
el = document.getElementById(field_id);

// Simulate click event on the disclosure control to reveal the values:
await el.dispatchEvent(new Event ('focus'));

pickableElements = el.parentElement.parentElement.parentElement.getElementsByClassName('multiselect__element');

// Iterate through multiselect options looking for the desired value
for (const i in pickableElements)
{
    if (pickableElements[i].innerText == value.toUpperCase())
    {
       pickableElements[i].getElementsByClassName('multiselect__option')[0].click();
       return;
    }
}
```

There's no need to send an update or input event after the click.

## Niceties

The following extras improve maintenance and usability.

### Form data

The form data is broken up into sections just like the form is, where each section has multiple elements (text boxes, radio buttons, multiselects, checkboxes). The test scenarios are organised into sections where the key is the page element id, and the value is the expected value. For example, in the section `drivers_information` below, we want the value of object  id `drivers_number` to be set to `1234567`:

```
var scenario1 = {
    drivers_information: {
        drivers_number:  "1234567",
        drivers_licence_jurisdiction: "British Columbia",
        last_name:       "Dogsneeze",
        first_name:      "Davey",
        dob:             "19990909",
        address1:        "77 Seventh St South",
        driver_phone:    "111-000-2222",
        city:            "Boston Bar",
        postal:          "V1V 2V2",
        province:        "British Columbia"
    },
    vehicle_information: {
        plate_number:   "AA057A",
        plate_province:  "ALBERTA",
        plate_year: "2022",
        plate_val_tag: "02",
        registration_number: "REG-12345",
        vehicle_type: "random",
        vehicle_year: "random",
        vehicle_make: "random",
        vehicle_color: "random",
        vin_number: "VIN012345679",
        puj_code: "ALBERTA",
        nsc_number: "NSC1234567890"
    }
}
```

As the sections are iterated, each object is inspected to determine if it's a checkbox, radio button, textfield, or multiselect. The value is set by calling a function to fill the appropriate control.

Breaking the fields up by section allows for sections to be filled individually. Multiple test records can be injected onto the page and mix-and-matched as needed.

### Basic UI

A very basic set of labels and buttons are overlaid on top of the web page like this:

```
// Add a label
let lbl = document.createElement("label");
lbl.innerHTML = labelText;

labelStyle = "top:" + topLocation + " !important;left:" + leftLocation + " !important;position:fixed;z-index: " + zIndex;
console.log("Adding label " + labelText + ": " + labelStyle);
lbl.style = labelStyle;
document.body.insertAdjacentElement("afterbegin", lbl);

// Add a button (to trigger autofill)
let btn = document.createElement("button");
btn.innerHTML = buttonName;

buttonStyle = "top:" + topLocation + " !important;left:" + leftLocation + " !important;position:fixed;z-index: " + zIndex;
console.log("Adding button " + buttonName + ": " + buttonStyle);
btn.style = buttonStyle;

btn.addEventListener('click', () => {
    FillFormSection(fieldStructure);
})
document.body.insertAdjacentElement("afterbegin", btn);
```

The page content is moved over by a 140 pixels to make room for the buttons and labels. The form is responsive, so it doesn't impact content, but the move has to be done after the page has rendered. To do this, I added an observer to trigger a DOM update after the page finishes rendering:

```javascript
// Select the entire DOM for observing:
const target = document.querySelector('body');

// Create a new observer instance to update the app container when it appears
const observer = new MutationObserver(function () {
    // Trigger when the 'app' element loads
    if (document.getElementById('app')) {
        document.getElementById('app').style.paddingLeft = "140px"
    }
});

// Set configuration object:
const config = {childList: true};

// Start the observer
observer.observe(target, config);
```

### Hot keys

As a convenience for humans, sections can be filled by pressing Alt+1, Alt+2, et cetera:

```javascript
// Set up hotkeys to fill form sections (Alt+1 to fill driver information, etc)
document.onkeyup = function () {
    var e = e || window.event; // for IE to cover IEs window event-object
    if (e.altKey && e.which == "1".charCodeAt(0)) {
        FillFormSection(form.drivers_information);
        return false;
    } else if (e.altKey && e.which == "2".charCodeAt(0)) {
        FillFormSection(form.vehicle_information);
        return false;
    }
}
```

There's also a hotkey to iterate through all the sections of the form and fill each one, plus another to iterate through the form and erase each entry.

### Dates in Vancouver time

When filling out the forms, times are entered in Vancouver time zone. If you're in a more easterly time zone (for example, Eastern GMT-0500) the form will fail validation if times are entered in your local time zone. This is implemented in the controller with the `convertTZ` function. Taken from [Stack Overflow](https://stackoverflow.com/a/54127122).

### Random and generated records

When a multiselect is used, you can easily pick a value at random. This can be useful to introduce variety to the test records.

At some point I will also introduce randomly-generated field values from [Change.js](https://chancejs.com/).

It's clear that I'm not a JavaScript expert or web developer. This solution is probably not the most elegant, but it gets the job done without fuss, and can be iterated upon.