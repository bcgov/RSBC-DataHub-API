
def test_unauthorized_user_cannot_get_df_payloads(as_guest):
    resp = as_guest.get("/v1/dfDocument/456/123",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 401


def test_authorized_user_can_get_df_payload(as_guest, auth_header):
    resp = as_guest.get("/v1/dfDocument/456/123",
                        follow_redirects=True,
                        headers=auth_header,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "impoundmentId" in resp.json
    assert "prohibitionId" in resp.json


def test_authorized_user_gets_404_if_notice_number_does_not_exist(as_guest, auth_header):
    resp = as_guest.get("/v1/dfDocument/000/123",
                        follow_redirects=True,
                        headers=auth_header,
                        content_type="application/json")
    assert resp.status_code == 404
