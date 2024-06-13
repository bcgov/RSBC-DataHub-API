

def test_unauthorized_user_cannot_get_impoundments(as_guest):
    resp = as_guest.get("/v1/impoundments/123/123",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 401
    assert {'message': 'unauthorized'} == resp.json


def test_authorized_user_can_get_impoundments(as_guest, auth_header):
    resp = as_guest.get("/v1/impoundments/123/123",
                        follow_redirects=True,
                        headers=auth_header,
                        content_type="application/json")
    assert resp.status_code == 200
    assert "respMsg" in resp.json


def test_unauthorized_user_cannot_create_impoundments(as_guest):
    resp = as_guest.post("/v1/impoundments/123",
                         json={},
                         follow_redirects=True,
                         content_type="application/json")
    assert resp.status_code == 401


def test_authorized_user_can_create_impoundments(as_guest, auth_header):
    resp = as_guest.post("/v1/impoundments/123",
                         headers=auth_header,
                         json={
                             "respMsg": "123",
                             "result": {
                                 "dfId": 1234
                             }
                         },
                         follow_redirects=True,
                         content_type="application/json")
    assert resp.json == {"vipsImpoundmentId": 0, "dfId": 0, "respMsg": "string"}
    assert resp.status_code == 201


def test_creating_incomplete_impoundments_are_rejected_with_400_error(as_guest, auth_header):
    resp = as_guest.post("/v1/impoundments/123",
                         headers=auth_header,
                         json={"respMsg": "hello"},
                         follow_redirects=True,
                         content_type="application/json")
    assert resp.status_code == 400
    assert resp.json == {'message': {'result': ['required field']}}



