import fst_api as f
from fastapi.testclient import TestClient
import os

client = TestClient(f.app)

def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': f.info}

def test_find():
    response = client.get('/chats/')
    files = [file for file in os.walk('./Data')]
    assert response.status_code == 200
    assert response.text == files[0]

def test_reload():
    response = client.get('/reload/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Chats are uploading now. Please wait.'}

def test_upload():
    response = client.post(
        '/upload/',
        json = {'link': 'skazochnyy_les.csv'}
        )
    assert response.status_code == 200

def test_addlink_new():
    response = client.post(
        '/addlink/',
        json = {'link': 'https://t.me/hp_main'}
        )
    assert response.status_code == 200
    assert response.json() == {'message': 'OK'}

def test_addlink_old():
    response = client.post(
        '/addlink/',
        json = {'link': 'https://t.me/skazochnyy_les'}
        )
    assert response.status_code == 200
    assert response.json() == {'message': 'This link already exists'}
