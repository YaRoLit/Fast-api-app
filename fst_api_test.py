import fst_api as f
from fastapi.testclient import TestClient
import os

client = TestClient(f.app)

def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": f.info}

def test_find():
    response = client.get('/chats/')
    files = [file for file in os.walk('./Data')]
    assert response.status_code == 200
    assert response.text == files

def test_reload():
    response = client.get('/reload/')
    assert response.status_code == 200
    assert response.json() == {"message": "chats uploading now. You have to wait some time for search uploading files."}

def test_upload():
    response = client.post(
        '/upload/',
        json = {'link': 'https://t.me/skazochnyy_les'}
        )
    assert response.status_code == 200

def test_addlink_new():
    response = client.post(
        '/addlink/',
        json = {'link': 'https://t.me/hp_main'}
        )
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}

def test_addlink_old():
    response = client.post(
        '/addlink/',
        json = {'link': 'https://t.me/skazochnyy_les'}
        )
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}
