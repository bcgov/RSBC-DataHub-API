from python.common.rsi_email import get_jinja2_env, get_email_content
import pytest


def test_admin_notice_method():
    template = get_jinja2_env().get_template('admin_notice.html')
    body = 'Here is something you should know.'
    title = "Error: Unknown event type"
    html = template.render(subject=title,
                           body=body)
    print(html)
    assert body in html
    assert title in html


def test_application_accepted():
    template = get_jinja2_env().get_template('IRP_application_accepted.html')
    full_name = 'Bob Smith'
    number = "201234567"
    subject = "Application received"
    html = template.render(subject=subject,
                           full_name=full_name,
                           prohibition_number=number)
    print(html)
    assert full_name in html
    assert subject in html
    assert number in html
    assert "Please do not respond to this email" in html


def test_schedule_review_email():
    template = get_jinja2_env().get_template('IRP_select_review_date.html')
    full_name = 'Bob Smith'
    number = "201234567"
    subject = "Re: Driving Prohibition Review - Select a Review Date {}".format(number)
    html = template.render(subject=subject,
                           full_name=full_name,
                           prohibition_number=number)
    print(html)
    assert "to select a review date" in html
    assert full_name in html
    assert subject in html
    assert number in html
    assert "Please do not respond to this email" in html


template_names = [
    ("IRP_last_name_mismatch.html", "Prohibition Number or Name Don't Match - Driving Prohibition 9999 Review"),
    ('template_does_not_exist.html', "Unknown template")
]


@pytest.mark.parametrize("template_name, subject_string", template_names)
def test_get_email_content(template_name, subject_string):
    content = get_email_content(template_name, '9999')
    assert content['subject'] == subject_string
