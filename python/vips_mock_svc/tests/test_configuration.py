
def test_unauthorized_user_cannot_reach_configuration_endpoint(as_guest):
    resp = as_guest.get("/v1/configuration/123",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 401


def test_authorized_user_can_get_configuration(as_guest, auth_header):
    resp = as_guest.get("/v1/configuration/123",
                        follow_redirects=True,
                        headers=auth_header,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "configuration" in resp.json
