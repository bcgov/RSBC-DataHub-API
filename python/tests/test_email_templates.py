from python.common.email import get_jinja2_env


def test_admin_notice_method():
    template = get_jinja2_env().get_template('admin_notice.html')
    html = template.render(title="Error: Unknown event type", event_type='some_unknown_event_type')
    print(html)
    assert False
