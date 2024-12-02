
def test_search_endpoint_not_implemented(as_guest):
    resp = as_guest.get("/v1/search/123",
                        query_string={"noticeNo": "222"},
                        json={},
                        follow_redirects=True,
                        content_type="application/json")
    assert resp.status_code == 404
    # method no longer implemented

