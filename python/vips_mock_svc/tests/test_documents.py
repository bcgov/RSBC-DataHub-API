
def test_unauthorized_user_cannot_get_documents(as_guest):
    resp = as_guest.get("/v1/documents/456/123",
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 401


def test_authorized_user_can_get_document_url(as_guest, auth_header):
    resp = as_guest.get("/v1/documents/456/123?url=1",
                        follow_redirects=True,
                        headers=auth_header,
                        content_type="application/json")
    assert resp.status_code == 200
    assert {'document_id': 'string'} == resp.json


def test_authorized_user_can_get_base64_document_string(as_guest, auth_header):
    resp = as_guest.get("/v1/documents/456/123?b64=1",
                        follow_redirects=True,
                        headers=auth_header,
                        content_type="application/json")
    assert resp.status_code == 200
    assert {'document_id': 'base64-string'} == resp.json


def test_authorized_user_that_does_not_specify_document_type_get_400(as_guest, auth_header):
    resp = as_guest.get("/v1/documents/456/123",
                        follow_redirects=True,
                        headers=auth_header,
                        content_type="application/json")
    assert resp.status_code == 400


def test_authorized_user_can_get_all_documents(as_guest, auth_header):
    resp = as_guest.get("/v1/documents/list/123",
                        follow_redirects=True,
                        headers=auth_header,
                        content_type="application/json")
    assert resp.status_code == 200
    assert 2 == len(resp.json)
    assert "addToFileDtm" in resp.json[0]


def test_authorized_can_create_a_new_document(as_guest, auth_header):
    resp = as_guest.post("/v1/documents/list/123",
                         json={
                             "type_code": "string",
                             "mime_type": "string",
                             "mime_sub_type": "string",
                             "auth_guid": "string",
                             "file_object": "string",
                             "pageCount": 0
                         },
                         follow_redirects=True,
                         headers=auth_header,
                         content_type="application/json")
    assert resp.status_code == 201


def test_creating_a_new_document_without_required_fields_returns_400(as_guest, auth_header):
    resp = as_guest.post("/v1/documents/list/123",
                         json={
                             "mime_type": "string",
                             "mime_sub_type": "string",
                             "auth_guid": "string",
                             "file_object": "string",
                             "pageCount": 0
                         },
                         follow_redirects=True,
                         headers=auth_header,
                         content_type="application/json")
    assert resp.status_code == 400
    assert resp.json == {'message': {'type_code': ['required field']}}


def test_authorized_can_create_a_document_association(as_guest, auth_header):
    resp = as_guest.post("/v1/documents/association/notice/456/123",
                         json={
                             "noticeNo": "string",
                             "noticeTypeCd": "string"
                         },
                         follow_redirects=True,
                         headers=auth_header,
                         content_type="application/json")
    assert resp.status_code == 201
    assert {"respCd": 0, "respMsg": "string"} == resp.json


def test_authorized_cannot_create_a_document_association_without_required_fields(as_guest, auth_header):
    resp = as_guest.post("/v1/documents/association/notice/456/123",
                         json={
                             "noticeTypeCd": "string"
                         },
                         follow_redirects=True,
                         headers=auth_header,
                         content_type="application/json")
    assert resp.status_code == 400
    assert {'message': {'noticeNo': ['required field']}} == resp.json
