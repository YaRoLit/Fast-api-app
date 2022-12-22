import fst_api as f
from fastapi.testclient import TestClient

client = TestClient(f.app)

def test_root():
    info = '- /chats/ \
        - /reload/\
        - /upload/\
        - /addlink/\
        - body form == {"link": "**filename or chat_link**"}
    assert f.root == {"message": info}

def test_reload():
    assert f.reload == {"message": "chats uploading now. You have to wait some time for search uploading files."}

    
