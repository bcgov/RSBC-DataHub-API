

def test_unauthorized_cannot_get_prohibitions(as_guest):
    resp = as_guest.get("/v1/prohibitions/123/123",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 401
    assert {'message': 'unauthorized'} == resp.json


def test_authorized_can_get_prohibitions(as_guest, auth_header):
    resp = as_guest.get("/v1/prohibitions/123/123",
                        follow_redirects=True,
                        headers=auth_header,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "respMsg" in resp.json
    assert "result" in resp.json


def test_unauthorized_user_cannot_create_prohibitions(as_guest):
    resp = as_guest.post("/v1/prohibitions/123",
                         json={},
                         follow_redirects=True,
                         content_type="application/json")
    assert resp.status_code == 401


def test_authorized_user_can_create_prohibitions(as_guest, auth_header):
    resp = as_guest.post("/v1/prohibitions/123",
                         headers=auth_header,
                         json={
                             "respMsg": "123",
                             "result": {
                                 "dfId": 1234
                             }
                         },
                         follow_redirects=True,
                         content_type="application/json")
    assert resp.json == {"vipsProhibitionId": 0, "dfId": 0, "respMsg": "string"}
    assert resp.status_code == 201

