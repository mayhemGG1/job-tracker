from app import Application, db

def test_index_empty(auth_client):
    response = auth_client.get("/")
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Поки що порожньо" in text

def test_add_application(auth_client):
    response = auth_client.post(
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

def test_delete(auth_client, user):
    a = Application(company="Acme", position="Dev", user_id=user.id)
    db.session.add(a)
    db.session.commit()

    response = auth_client.post(f"/delete/{a.id}", follow_redirects=True)
    text = response.get_data(as_text=True)

    assert "Acme" not in text

def test_edit_application(auth_client, user):
    a = Application(company="Acme", position="Dev", status="applied", user_id=user.id)
    db.session.add(a)
    db.session.commit()

    auth_client.post(
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

def test_filter_by_status(auth_client, user):
    a = Application(company="Alpha", position="Dev", status="applied", user_id=user.id)
    b = Application(company="Beta", position="Dev", status="interview", user_id=user.id)
    db.session.add_all([a, b])
    db.session.commit()

    response = auth_client.get("/?status=interview")
    text = response.get_data(as_text=True)

    assert "Beta" in text
    assert "Alpha" not in text
