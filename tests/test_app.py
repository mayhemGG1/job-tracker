from app import Application, db

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

def test_delete(client):
    a = Application(company="Acme", position="Dev")
    db.session.add(a)
    db.session.commit()

    response = client.post(f"/delete/{a.id}", follow_redirects=True)
    text = response.get_data(as_text=True)

    assert "Acme" not in text

def test_edit_application(client):
    a = Application(company="Acme", position="Dev", status="applied")
    db.session.add(a)
    db.session.commit()

    client.post(
        f"/edit/{a.id}",
        data={
            "company": "Acme",
            "position": "Dev",
            "status": "interview",
            "url": "",
            "notes": "",
        },
        follow_redirects=True,
    )
    db.session.refresh(a)
    assert a.status == "interview"

def test_filter_by_status(client):
    a = Application(company="Alpha", position="Dev", status="applied")
    b = Application(company="Beta", position="Dev", status="interview")
    db.session.add_all([a, b])
    db.session.commit()

    response = client.get("/?status=interview")
    text = response.get_data(as_text=True)

    assert "Beta" in text
    assert "Alpha" not in text
