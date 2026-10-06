def test_index_empty(client):
    response = client.get("/")
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Поки що порожньо" in text

def test_add_application(client):
    response = client.post(
        "/add",
        data={
            "company": "Acme",
            "position": "Junior Python Dev",
            "status": "applied",
        },
        follow_redirects=True,
    )
    text = response.get_data(as_text=True)
    assert "Acme" in text

    