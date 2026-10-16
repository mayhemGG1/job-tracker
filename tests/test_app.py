from app import Application, db, User

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
    app_id = a.id

    response = auth_client.post(f"/delete/{a.id}")
    assert db.session.get(Application, app_id) is None
    

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


def test_index_requires_login(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_add_requires_login(client):
    response = client.get("/add")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_cannot_delete_foreign_application(auth_client):
    other = User(email="other@example.com")
    other.set_password("password123")
    db.session.add(other)
    db.session.commit()
    a = Application(company="Secret", position="Dev", user_id=other.id)
    db.session.add(a)
    db.session.commit()
    app_id = a.id

    response = auth_client.post(f"/delete/{app_id}")
    assert response.status_code == 404
    assert db.session.get(Application, app_id) is not None

def test_cannot_edit_foreign_application(auth_client):
    other = User(email="other@example.com")
    other.set_password("password123")
    db.session.add(other)
    db.session.commit()
    a = Application(company="secret", position="Dev", status="applied", user_id=other.id)
    db.session.add(a)
    db.session.commit()
    app_id = a.id

    response = auth_client.post(f"/edit/{app_id}", data={"company": "secret", "position": "dev", "status": "interview", "url": " ", "notes": " "})

    assert response.status_code == 404
    db.session.refresh(a)
    assert a.status == "applied"
    assert db.session.get(Application, app_id) is not None