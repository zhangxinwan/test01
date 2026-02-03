import json
import os
import tempfile

import pytest

from app import create_app
from models import db


@pytest.fixture
def app(tmp_path):
    db_file = tmp_path / "test.db"
    config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_file}",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
    app = create_app(config)
    with app.app_context():
        db.create_all()
    yield app
    # cleanup
    try:
        os.remove(db_file)
    except Exception:
        pass


@pytest.fixture
def client(app):
    return app.test_client()


def test_crud_and_duplicates(client):
    # create Alice
    r = client.post('/users', json={'name': 'Alice', 'email': 'alice@example.com'})
    assert r.status_code == 201
    alice = r.get_json()
    assert alice['name'] == 'Alice'

    # create Bob
    r = client.post('/users', json={'name': 'Bob', 'email': 'bob@example.com'})
    assert r.status_code == 201

    # list
    r = client.get('/users')
    assert r.status_code == 200
    js = r.get_json()
    assert isinstance(js, list) and len(js) == 2

    # get alice
    r = client.get(f"/users/{alice['id']}")
    assert r.status_code == 200
    assert r.get_json()['email'] == 'alice@example.com'

    # duplicate email -> 409
    r = client.post('/users', json={'name': 'Alice2', 'email': 'alice@example.com'})
    assert r.status_code == 409

    # update
    r = client.put(f"/users/{alice['id']}", json={'name': 'Alice B'})
    assert r.status_code == 200
    assert r.get_json()['name'] == 'Alice B'

    # delete
    r = client.delete(f"/users/{alice['id']}")
    assert r.status_code == 204

    # get deleted -> 404
    r = client.get(f"/users/{alice['id']}")
    assert r.status_code == 404
