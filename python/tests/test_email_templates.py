from python.common.email import get_jinja2_env
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


def test_application_received():
    template = get_jinja2_env().get_template('application_received.html')
    full_name = 'Bob Smith'
    number = "201234567"
    subject = "Application received"
    date_received = "August 20, 2020"
    html = template.render(subject=subject,
                           full_name=full_name,
                           prohibition_number=number,
                           date_received=date_received)
    print(html)
    assert full_name in html
    assert subject in html
    assert number in html
    assert date_received in html
    assert "You must <strong>not</strong> drive" in html
    assert "we won't get your response" in html

