import fst_api as f
from fastapi.testclient import TestClient

client = TestClient(f.app)

def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": f.info}

def test_find():
    response = client.get('/chats/')
    assert response.status_code == 200
#    assert response.

def test_reload():
    response = client.get('/reload/')
    assert response.status_code == 200
    assert response.json() == {"message": "chats uploading now. You have to wait some time for search uploading files."}

def test_upload():
    response = client.post(
        '/upload/',
        json={'item': 'https://t.me/skazochnyy_les'}
        )
    assert response.status_code == 200
#    assert response.

def test_addlink_new():
    response = client.post(
        '/addlink/',
        json={'item': 'https://t.me/hp_main'}
        )
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}

def test_addlink_old():
    response = client.post(
        '/addlink/',
        json={'item': 'https://t.me/skazochnyy_les'}
        )
    assert response.status_code == 200
    assert response.json() == {"message": "This link already exist"}
